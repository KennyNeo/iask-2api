<div align="center">

# ✨ iask-2api (真理·终章) ✨

<img src="https://img.shields.io/badge/version-6.0.0-blue.svg" alt="Version">
<img src="https://img.shields.io/badge/license-Apache_2.0-green.svg" alt="License">
<img src="https://img.shields.io/badge/status-stable-brightgreen.svg" alt="Status">
<img src="https://img.shields.io/badge/made_with-love_&_python-red.svg" alt="Made with Love & Python">
<img src="https://img.shields.io/badge/docker-ready-blue.svg?logo=docker" alt="Docker Ready">

**将 [iask.ai](https://iask.ai/) 转换为兼容 OpenAI 格式 API 的高性能匿名代理**

**"我们并非在创造新的智慧，而是在搭建桥梁，让已存在的智慧之光，照亮更多被隔绝的角落。"**

</div>

---

## 📜 目录

- [🌟 核心哲学](#-核心哲学)
- [🚀 快速开始](#-快速开始)
- [🎯 项目特性](#-项目特性)
- [🤖 技术架构](#-技术架构)
- [📈 项目现状与未来规划](#-项目现状与未来规划)
- [💡 开发者指南](#-开发者指南)
- [📄 开源协议](#-开源协议)

---

## 🌟 核心哲学

在这个信息爆炸的时代，我们每个人都像是漂浮在知识海洋中的孤岛。`iask-2api` 的诞生，源于一个纯粹而强大的信念：**打破壁垒，赋能创造**。

### 我们的价值观

- **开放 (Openness) 👐**：通过将 `iask.ai` 封装成标准的 OpenAI API，我们为无数现有的应用和开发者打开了一扇新的大门。
- **便捷 (Convenience) 🕊️**：复杂性应该留给代码，而不是用户。我们追求极致的"开箱即用"体验。
- **鼓励 (Encouragement) 💪**：我们希望激发你内心深处的创造欲和探索精神，让你相信"我来我也行"。

---

## 🚀 快速开始

### 前提条件
- 安装 [Docker](https://www.docker.com/get-started) 和 [Docker Compose](https://docs.docker.com/compose/install/)

### 三步部署

**1. 克隆项目**
```bash
git clone https://github.com/lzA6/iask-2api.git
cd iask-2api
```

**2. 配置环境变量**
```bash
cp .env.example .env
# 编辑 .env 文件，设置你的 API 密钥和端口
```

**3. 启动服务**
```bash
docker-compose up -d
```

### 验证部署
```bash
curl http://localhost:8088/v1/models -H "Authorization: Bearer your-super-secret-key"
```

如果返回 JSON 格式的模型列表，恭喜你部署成功！🎉

---

## 🎯 项目特性

### ✅ 核心优势

| 特性 | 描述 | 受益场景 |
|------|------|----------|
| **无缝集成** 🧩 | 将 iask.ai 转换为标准 OpenAI API 格式 | 兼容所有支持 OpenAI 的客户端和库 |
| **极致便捷** 💨 | Docker 一键部署，无需环境配置 | 小白用户友好，快速上手 |
| **匿名访问** 🕵️ | 无需登录或提供 Cookie | 保护用户隐私，简化配置 |
| **高性能流式响应** 💧 | 字符级增量流式输出 | 实时响应，体验媲美原生模型 |

### ⚠️ 局限性

| 限制 | 影响 | 解决方案 |
|------|------|----------|
| **前端依赖** 🕸️ | iask.ai 前端改版可能导致失效 | 需要及时更新选择器 |
| **资源消耗** 🐘 | 浏览器实例占用较多资源 | 建议适当配置服务器 |
| **潜在不稳定性** 🎲 | 可能遇到反爬虫机制 | 未来集成反反爬虫技术 |

---

## 🤖 技术架构

### 🏗️ 系统架构图

```mermaid
graph TB
    A[客户端] --> B{Nginx<br/>反向代理}
    B --> C[FastAPI<br/>Web框架]
    C --> D[iask-2api<br/>核心服务]
    D --> E[Playwright<br/>浏览器自动化]
    E --> F[iask.ai<br/>目标网站]
    
    D --> G[SSE流式响应]
    G --> C
    C --> B
    B --> A
    
    subgraph "核心处理流程"
        H[请求接收] --> I[认证验证]
        I --> J[参数解析]
        J --> K[浏览器模拟]
        K --> L[内容抓取]
        L --> M[实时清理]
        M --> N[流式返回]
    end
```

### 📁 项目结构

```
iask-2api/
├── 🐳 Dockerfile              # 容器化配置
├── 🐳 docker-compose.yml      # 服务编排
├── 🔧 nginx.conf              # Nginx 配置
├── 📄 main.py                 # FastAPI 应用入口
├── 📄 requirements.txt        # Python 依赖
├── 📄 .env.example            # 环境变量模板
└── 📂 app/                    # 核心代码
    ├── 📂 core/
    │   └── 📄 config.py       # 配置管理
    ├── 📂 providers/
    │   ├── 📄 base_provider.py # 抽象基类
    │   └── 📄 iask_provider.py # iask.ai 实现
    └── 📂 utils/
        └── 📄 sse_utils.py    # 流式响应工具
```

### 🔧 核心技术栈

| 技术组件 | 版本 | 用途 | 选择理由 |
|----------|------|------|----------|
| **FastAPI** | 0.104+ | Web API 框架 | 高性能，原生异步，自动文档 |
| **Playwright** | 1.40+ | 浏览器自动化 | 现代化 API，更好的异步支持 |
| **Docker** | 20.10+ | 容器化部署 | 环境一致性，简化部署 |
| **Nginx** | 1.24+ | 反向代理 | 高性能，流式传输优化 |

### 🎯 核心工作流程

1. **请求接收** 📥 - FastAPI 接收 OpenAI 格式请求
2. **认证验证** 🔐 - 验证 API Key 有效性
3. **浏览器启动** 🚀 - Playwright 启动无头浏览器
4. **页面访问** 🌐 - 访问 iask.ai 并提交查询
5. **实时监控** 👀 - 监听 DOM 变化，捕获增量内容
6. **内容清理** 🧹 - 移除广告，转换格式
7. **流式返回** 📤 - SSE 格式实时返回结果

### 💡 关键技术实现

#### 字符级流式输出
```python
async def stream_answer(self, question: str, model: str):
    """实现字符级增量流式输出"""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # 访问目标页面
        await page.goto(self._build_url(question, model))
        
        last_text = ""
        while True:
            # 实时获取最新内容
            current_text = await page.inner_html('#text')
            
            # 计算增量内容
            new_text = current_text[len(last_text):]
            if new_text:
                # 清理并返回增量
                cleaned = self._clean_text_chunk(new_text)
                yield cleaned
                last_text = current_text
            
            # 检查是否结束
            if await page.is_visible('#relatedQuestions'):
                break
            
            await asyncio.sleep(0.1)
```

#### Nginx 流式优化
```nginx
# 关键配置：关闭代理缓冲，实现真·流式
location / {
    proxy_pass http://iask_backend;
    proxy_buffering off;           # 🔑 关键配置
    proxy_cache off;
    chunked_transfer_encoding on;
}
```

---

## 📈 项目现状与未来规划

### ✅ 已实现功能 (v6.0.0)

- [x] **完整 API 兼容** - 支持 OpenAI `v1/chat/completions` 接口
- [x] **字符级流式响应** - 实时增量输出，体验优秀
- [x] **多模型支持** - 支持 iask.ai 各种搜索模式
- [x] **一键部署** - Docker Compose 完整解决方案
- [x] **安全认证** - API Key 保护机制
- [x] **智能清理** - 自动移除广告，优化格式

### 🚧 开发路线图

#### 短期目标 (v6.1.0)
- [ ] 增强错误处理和重试机制
- [ ] 添加健康检查端点
- [ ] 优化浏览器资源管理

#### 中期目标 (v7.0.0)  
- [ ] 多 Provider 支持 (Bing、Google 等)
- [ ] 负载均衡和实例池
- [ ] 请求限流和配额管理

#### 长期愿景
- [ ] 可视化监控面板
- [ ] 插件化架构
- [ ] 云原生部署支持

### 🐛 已知问题与解决方案

| 问题 | 影响程度 | 临时解决方案 | 长期规划 |
|------|----------|--------------|----------|
| 前端选择器变更 | 高 | 手动更新选择器 | 自适应选择器 |
| 验证码拦截 | 中 | 手动验证 | 集成验证码服务 |
| 高并发限制 | 中 | 增加资源 | 浏览器实例池 |

---

## 💡 开发者指南

### 🛠️ 快速开发设置

**1. 本地开发环境**
```bash
# 克隆项目
git clone https://github.com/lzA6/iask-2api.git
cd iask-2api

# 安装依赖
pip install -r requirements.txt

# 安装 Playwright 浏览器
playwright install chromium

# 启动开发服务器
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**2. 调试模式**
```bash
# 设置调试环境变量
export DEBUG=true
export API_MASTER_KEY=your-test-key

# 启动服务
python main.py
```

### 🔍 核心修改点指南

#### 修复前端选择器变更
```python
# 文件: app/providers/iask_provider.py
# 修改内容选择器
await page.wait_for_selector('#text', timeout=60000)  # 旧选择器
await page.wait_selector('.new-content-container', timeout=60000)  # 新选择器
```

#### 添加新的 Provider
```python
# 1. 创建新文件: app/providers/new_provider.py
class NewProvider(BaseProvider):
    async def chat_completion(self, request_data: dict):
        # 实现你的逻辑
        pass
    
    async def get_models(self):
        # 返回支持的模型列表
        return ["model1", "model2"]
```

### 🧪 测试与验证

**API 测试示例**
```bash
# 测试聊天补全
curl -X POST "http://localhost:8088/v1/chat/completions" \
  -H "Authorization: Bearer your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "general",
    "messages": [{"role": "user", "content": "你好，世界！"}],
    "stream": true
  }'
```

**健康检查**
```bash
curl "http://localhost:8088/health"
```

### 🔧 故障排除

| 问题现象 | 可能原因 | 解决方案 |
|----------|----------|----------|
| 启动失败，端口被占用 | 端口冲突 | 修改 `.env` 中的 `NGINX_PORT` |
| 浏览器启动失败 | 系统依赖缺失 | 确保 Docker 正常运行 |
| API 返回 401 | API Key 错误 | 检查 `Authorization` 头格式 |
| 流式响应卡顿 | Nginx 缓冲 | 确认 `proxy_buffering off` |

---

## 📄 开源协议

本项目采用 **Apache 2.0** 开源协议。

### 你可以自由地：
- ✅ **商用** - 将本项目用于商业目的
- ✅ **分发** - 复制和分发项目副本  
- ✅ **修改** - 修改源代码
- ✅ **私用** - 在个人项目中使用

### 你需要：
- 📝 **保留版权声明** - 在分发中包含原始许可声明
- 📝 **声明变更** - 在修改的文件中明确标注更改

### 典型使用场景
```python
# 在你的项目中这样使用
from iask2api import Client

client = Client(
    base_url="http://your-iask-2api-server",
    api_key="your-api-key"
)

# 就像使用 OpenAI 官方客户端一样
response = client.chat.completions.create(
    model="general",
    messages=[{"role": "user", "content": "你的问题"}]
)
```

---

<div align="center">

## 🎉 感谢使用 iask-2api！

**如果这个项目对你有帮助，请给我们一个 ⭐ Star！**

> "技术的价值不在于其本身的复杂，而在于它能够为多少人创造可能。"

**crafted with ❤️ and ☕ by the community, for the community.**

</div>

## 🔗 相关链接

- [项目地址](https://github.com/lzA6/iask-2api)
- [问题反馈](https://github.com/lzA6/iask-2api/issues)
- [更新日志](https://github.com/lzA6/iask-2api/releases)
- [讨论区](https://github.com/lzA6/iask-2api/discussions)

---

<div align="center">

*最后更新: 2024年12月*  
*愿你的每一次代码提交，都让这个世界变得更好一点点。*

</div>
