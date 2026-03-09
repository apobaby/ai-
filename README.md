# AI虚拟试衣 + 数字模特生成（ChatGPT Only）

本项目实现：
- 数字模特生成
- 衣服上传
- AI虚拟试衣
- 姿态生成
- 历史记录查询

> **AI限制**：仅接入 OpenAI ChatGPT API（`OPENAI_MODEL` 默认 `gpt-4.1`），不接入任何其他AI模型/服务。

## 技术栈

- Frontend: Next.js + React + TailwindCSS + TypeScript
- Backend: Python + FastAPI
- AI: OpenAI API (ChatGPT)
- DB: PostgreSQL
- Deploy: Docker / Docker Compose

## 项目结构

```text
project/
  frontend/
    pages/
    components/
    services/
  backend/
    main.py
    routes/
    models/
    services/
      openai_service.py
      image_generator.py
```


## 关键修复（保证可运行）

- 已修复 OpenAI 图片生成调用：统一走 ChatGPT Responses API 的 `image_generation` 工具。
- 已修复试衣/姿态生成的参考图输入：后端会读取本地已上传图片并以 base64 传给 ChatGPT，而不是只传 URL 文本。
- 已增加本地开发数据库默认值：默认使用 SQLite（`sqlite:///./virtual_tryon.db`）便于开箱即用；Docker 下仍使用 PostgreSQL。

## OpenAI API Key 配置

1. 复制配置：

```bash
cp .env.example .env
```

2. 在 `.env` 中填写：

```env
OPENAI_API_KEY=your_openai_api_key
```

## 本地运行（Docker）

```bash
docker compose up --build
```

启动后：
- 前端: http://localhost:3000
- 后端: http://localhost:8000
- API文档: http://localhost:8000/docs

## 非Docker运行

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export OPENAI_API_KEY=your_openai_api_key
export DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/virtual_tryon  # 可选，不设置则默认 SQLite
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm install
NEXT_PUBLIC_API_BASE=http://localhost:8000 npm run dev
```

## API说明

### 1) POST `/generate-avatar`

FormData:
- `user_image` (file)
- `height` (number)
- `weight` (number)
- `gender` (string)

返回:
```json
{ "avatar_image_url": "string", "avatar_id": 1 }
```

### 2) POST `/upload-clothes`

FormData:
- `clothes_image` (file)

返回:
```json
{ "clothes_image_url": "string", "clothes_id": 1 }
```

### 3) POST `/try-on`

JSON:
```json
{
  "avatar_image_url": "string",
  "clothes_image_url": "string"
}
```

返回:
```json
{ "result_image_url": "string" }
```

### 4) POST `/generate-pose`

JSON:
```json
{
  "avatar_image_url": "string",
  "pose_type": "standing|walking|side view"
}
```

返回:
```json
{ "pose_image_url": "string" }
```

### 5) GET `/history`
返回试衣历史列表。

## 数据表

- `users(id, created_at)`
- `avatars(id, user_id, image_url, height, weight, gender, created_at)`
- `clothes(id, image_url, created_at)`
- `try_on_results(id, avatar_id, clothes_id, result_url, created_at)`

## 部署

生产部署可直接基于 `docker-compose.yml` 或拆分部署：
- PostgreSQL 独立托管
- Backend (FastAPI) 容器化
- Frontend (Next.js) 容器化
