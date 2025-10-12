# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional, Dict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra="ignore"
    )

    APP_NAME: str = "iask-2api"
    APP_VERSION: str = "6.0.0"
    DESCRIPTION: str = "一个将 iask.ai 转换为兼容 OpenAI 格式 API 的高性能匿名代理 (真理·终章)。"

    API_MASTER_KEY: Optional[str] = None
    
    API_REQUEST_TIMEOUT: int = 180
    NGINX_PORT: int = 8088

    # --- 模型配置 ---
    DEFAULT_MODEL: str = "通用问答 (适合日常问题)"
    
    # 模型详细信息字典
    MODEL_DETAILS: Dict[str, Dict[str, str]] = {
        "question": {
            "display_id": "通用问答 (适合日常问题)",
            "description": "适用于各种日常问题和知识查询，提供快速、准确的答案。"
        },
        "academic": {
            "display_id": "学术研究 (适合深度分析)",
            "description": "专注于学术领域的深度分析，适合论文写作、文献综述和专业知识探索。"
        },
        "thinking": {
            "display_id": "深度思考 (适合复杂推理)",
            "description": "模拟人类的深度思考过程，逐步分解问题，适合复杂逻辑推理和决策。"
        },
        "forums": {
            "display_id": "论坛观点 (适合多方视角)",
            "description": "聚合和提炼各大论坛社区的讨论观点，提供多元化的参考信息和公众意见。"
        },
        "wiki": {
            "display_id": "维基百科 (适合事实查询)",
            "description": "基于维基百科等知识库，提供高度结构化、准确的事实信息和历史背景。"
        }
    }

    # 从 MODEL_DETAILS 动态生成模型列表
    @property
    def KNOWN_MODELS(self) -> List[str]:
        return list(self.MODEL_DETAILS.keys())

    # 创建从友好ID到原始ID的映射，用于内部转换
    @property
    def DISPLAY_ID_TO_SIMPLE_ID(self) -> Dict[str, str]:
        return {details["display_id"]: simple_id for simple_id, details in self.MODEL_DETAILS.items()}

settings = Settings()
