# --- 文件路径: app/utils/sse_utils.py ---

import json
import time
from typing import Dict, Any, Optional

DONE_CHUNK = b"data: [DONE]\n\n"

def create_sse_data(data: Dict[str, Any]) -> bytes:
    """将字典编码为 SSE data 行，确保非 ASCII 字符正确处理。"""
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n".encode('utf-8')

def create_chat_completion_chunk(
    request_id: str,
    model: str,
    content: str,
    finish_reason: Optional[str] = None
) -> Dict[str, Any]:
    """为增量流（delta）创建标准的 OpenAI 格式数据块。"""
    return {
        "id": request_id,
        "object": "chat.completion.chunk",
        "created": int(time.time()),
        "model": model,
        "choices": [
            {
                "index": 0,
                "delta": {"content": content} if content is not None else {},
                "finish_reason": finish_reason,
                "logprobs": None,
            }
        ],
    }
