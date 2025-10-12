# Dockerfile
# 使用官方的 Python slim 镜像作为基础
FROM python:3.11-slim-bookworm

# 设置环境变量，优化 Python 运行
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 设置工作目录
WORKDIR /app

# 步骤 1: 安装系统依赖，包括 Playwright 需要的库
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# 步骤 2: 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 步骤 3: 创建一个非 root 用户来运行应用
RUN useradd --create-home appuser

# 步骤 4: 为 appuser 安装 Playwright 浏览器
# 设置浏览器安装路径为 appuser 的 home 目录，这样 appuser 就能找到它
ENV PLAYWRIGHT_BROWSERS_PATH=/home/appuser/.cache/ms-playwright
# 以 root 身份执行安装，但文件会写入到上面指定的 appuser 目录
RUN playwright install chromium
# 安装浏览器运行所需的系统级依赖（这需要 root 权限）
RUN playwright install-deps chromium

# 步骤 5: 复制所有应用代码，并将所有权交给 appuser
COPY . .
RUN chown -R appuser:appuser /app

# 步骤 6: 切换到 appuser 用户
USER appuser

# 暴露 FastAPI 应用运行的端口
EXPOSE 8000

# 启动应用的命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
