# app/providers/iask_provider.py
import logging
import uuid
import asyncio
import json
import re
from typing import Dict, Any, AsyncGenerator
from urllib.parse import urlencode

from playwright.async_api import async_playwright, Page
from fastapi.responses import StreamingResponse
import html2text

from app.core.config import settings
from app.providers.base_provider import BaseProvider
from app.utils.sse_utils import create_sse_data, create_chat_completion_chunk, DONE_CHUNK

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class IaskProvider(BaseProvider):
    """
    iAsk.ai 的内容提供者。
    使用 Playwright 实现干净的、字符级增量流式响应。
    """
    def __init__(self):
        # --- 可配置参数 ---
        self.max_retries = 3           # 最大重试次数
        self.retry_delay = 5           # 重试间隔（秒）
        self.total_timeout = 180       # 总超时时间（秒）
        self.stale_timeout = 15        # 内容静止超时时间（秒）
        self.poll_interval = 0.2       # 轮询间隔（秒）
        
        # --- 内容清理正则表达式 ---
        # 匹配并移除开头的 "According to www.iAsk.Ai - Ask AI:"
        self.intro_pattern = re.compile(r'^According to www\.iAsk\.Ai - Ask AI:\s*', re.IGNORECASE)
        # 匹配并移除思考前缀
        self.thinking_pattern = re.compile(r'^(思考|Thinking)[:：]\s*', re.IGNORECASE)
        # 匹配并移除结尾的版权信息
        self.copyright_pattern = re.compile(r'\s*Answer Provided by.*?Ask AI\.?\s*$', re.IGNORECASE | re.DOTALL)
        
        # 【格式化核心】
        # 1. 确保引用标记前后有空格
        self.citation_space_pattern = re.compile(r'(\S)(\[\d+\])')
        # 2. 智能段落分隔：在引用标记后跟一个大写字母开头的新句子时，插入换行
        # 【修复点】将中文引号替换为标准英文引号，避免编码问题
        self.paragraph_pattern = re.compile(r'(\]\.\s+)(["\']?[\u4e00-\u9fffA-Z])')
        # 3. 清理多余的换行符，保留最多两个连续换行
        self.newline_pattern = re.compile(r'\n{3,}')

        logger.info("IaskProvider (Playwright-based with Ultimate Clean Streaming) 已初始化。")

        # --- 精细配置 html2text ---
        self.h = html2text.HTML2Text()
        self.h.ignore_links = False
        self.h.ignore_images = False
        self.h.ignore_emphasis = False
        self.h.body_width = 0  # 不自动换行
        self.h.protect_links = True # 保护链接不被意外断开
        self.h.wrap_links = False
        self.h.skip_internal_links = True
        self.h.inline_links = True
        self.h.images_to_alt = False # 保留图片链接，而不是只替换为alt文本
        self.h.unicode_snob = True # 使用Unicode字符

    def _clean_text_chunk(self, text_chunk: str) -> str:
        """
        使用正则表达式清理文本片段，移除引导语、版权信息、思考前缀，并优化格式。
        """
        # 1. 移除开头的引导语
        cleaned_chunk = self.intro_pattern.sub('', text_chunk)
        # 2. 移除思考前缀
        cleaned_chunk = self.thinking_pattern.sub('', cleaned_chunk)
        # 3. 移除结尾的版权信息
        cleaned_chunk = self.copyright_pattern.sub('', cleaned_chunk)
        
        # 4. 格式优化
        # 确保引用标记前后有空格
        cleaned_chunk = self.citation_space_pattern.sub(r'\1 \2', cleaned_chunk)
        # 智能段落分隔
        cleaned_chunk = self.paragraph_pattern.sub(r'\1\n\n\2', cleaned_chunk)
        # 清理多余的换行符
        cleaned_chunk = self.newline_pattern.sub('\n\n', cleaned_chunk)
        
        # 5. 去除首尾可能的空白
        return cleaned_chunk.strip()

    async def stream_answer(self, prompt: str, model: str) -> AsyncGenerator[str, None]:
        params = {
            'q': prompt,
            'mode': model,
            'options[detail_level]': 'comprehensive',
            'source': 'organic'
        }
        initial_url = f"https://iask.ai/q?{urlencode(params)}"
        
        logger.info(f"步骤 1: 使用Playwright开始流式访问 URL: {initial_url}")

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            try:
                await page.goto(initial_url)
                await page.wait_for_selector('#text', timeout=20000)
                logger.info("答案容器 (#text) 已出现，开始字符级增量流式监听...")

                # --- “双保险”结束策略 ---
                async def wait_for_related_questions():
                    try:
                        await page.wait_for_selector('#relatedQuestions', timeout=self.total_timeout * 1000)
                        return True
                    except Exception:
                        return False
                
                completion_task = asyncio.create_task(wait_for_related_questions())

                # 主循环：字符级增量流式读取
                last_full_text = ""
                no_change_timer = 0
                total_timer = 0
                
                while not completion_task.done() and no_change_timer < self.stale_timeout and total_timer < self.total_timeout:
                    try:
                        await asyncio.sleep(self.poll_interval)
                        total_timer += self.poll_interval

                        # 1. 获取当前全部HTML并转换为全部文本
                        current_html = await page.inner_html('#text')
                        current_full_text = self.h.handle(current_html).strip()
                        
                        # 2. 计算新增的文本（增量部分）
                        if len(current_full_text) > len(last_full_text):
                            # 有新内容，重置静止计时器
                            no_change_timer = 0
                            new_text_chunk = current_full_text[len(last_full_text):]
                            last_full_text = current_full_text
                            
                            # 3. 清理文本片段
                            cleaned_chunk = self._clean_text_chunk(new_text_chunk)
                            
                            if cleaned_chunk:
                                logger.info(f"流式发送片段，长度: {len(cleaned_chunk)}")
                                yield cleaned_chunk
                        else:
                            # 内容无变化，增加静止计时器
                            no_change_timer += self.poll_interval
                            logger.info(f"内容无变化，静止计时: {no_change_timer:.1f}s / {self.stale_timeout}s")

                    except Exception as e:
                        logger.error(f"流式读取内容时出错: {e}")
                        yield f"\n\n错误：{e}"
                        break
                
                # --- 循环结束，判断原因 ---
                if completion_task.done() and completion_task.result():
                    logger.info("流式结束原因：检测到 'People Also Ask' 区域，答案已完全生成。")
                elif no_change_timer >= self.stale_timeout:
                    logger.info(f"流式结束原因：内容已静止超过 {self.stale_timeout} 秒。")
                elif total_timer >= self.total_timeout:
                    logger.warning(f"流式结束原因：达到总超时时间 {self.total_timeout} 秒。")
                else:
                    logger.warning("流式结束原因：未知异常。")

                # 最后再检查一次，确保没有遗漏
                final_html = await page.inner_html('#text')
                final_full_text = self.h.handle(final_html).strip()
                if len(final_full_text) > len(last_full_text):
                    final_chunk = final_full_text[len(last_full_text):]
                    cleaned_final_chunk = self._clean_text_chunk(final_chunk)
                    if cleaned_final_chunk:
                        yield cleaned_final_chunk

            except Exception as e:
                logger.error(f"流式处理流程中发生顶层错误: {e}", exc_info=True)
                yield f"错误：{e}"
            finally:
                await browser.close()

    async def chat_completion(self, request_data: Dict[str, Any]) -> StreamingResponse:
        async def stream_generator() -> AsyncGenerator[bytes, None]:
            request_id = f"chatcmpl-{uuid.uuid4()}"
            # 从请求中获取模型名称（可能是友好ID）
            model_name_from_request = request_data.get("model", settings.DEFAULT_MODEL)
            
            # 【修复点】将友好ID转换为原始ID，并设置一个安全的回退值
            # 如果找不到请求中的模型，则回退到配置文件中设置的默认模型的原始ID
            default_simple_model = settings.DISPLAY_ID_TO_SIMPLE_ID.get(settings.DEFAULT_MODEL)
            simple_model_name = settings.DISPLAY_ID_TO_SIMPLE_ID.get(model_name_from_request, default_simple_model)
            
            logger.info(f"接收到模型 '{model_name_from_request}'，已转换为内部ID '{simple_model_name}'")

            question = request_data["messages"][-1]["content"]
            
            try:
                async for markdown_chunk in self.stream_answer(question, simple_model_name):
                    chunk = create_chat_completion_chunk(request_id, model_name_from_request, markdown_chunk)
                    yield create_sse_data(chunk)
                
            except Exception as e:
                logger.error(f"处理流程中发生顶层错误: {e}", exc_info=True)
                error_message = f"获取答案失败: {e}"
                error_chunk = create_chat_completion_chunk(request_id, model_name_from_request, error_message, "stop")
                yield create_sse_data(error_chunk)
            finally:
                yield DONE_CHUNK

        return StreamingResponse(stream_generator(), media_type="text/event-stream")

    async def get_models(self) -> Dict[str, Any]:
        import time
        return {
            "object": "list",
            "data": [
                {
                    "id": details["display_id"],
                    "object": "model",
                    "created": int(time.time()),
                    "owned_by": "iask-2api"
                }
                for details in settings.MODEL_DETAILS.values()
            ]
        }
