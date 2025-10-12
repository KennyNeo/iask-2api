# --- 文件路径: app/providers/base_provider.py ---

from abc import ABC, abstractmethod
from typing import Union
from fastapi import Request
from fastapi.responses import StreamingResponse, JSONResponse

class BaseProvider(ABC):
    @abstractmethod
    async def chat_completion(
        self,
        request: Request
    ) -> Union[StreamingResponse, JSONResponse]:
        """
        处理聊天补全请求。
        接收完整的 Request 对象以访问所有需要的信息。
        """
        pass

    @abstractmethod
    async def get_models(self) -> JSONResponse:
        """
        获取模型列表。
        """
        pass

