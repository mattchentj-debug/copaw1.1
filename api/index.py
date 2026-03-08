from fastapi import FastAPI
from mangum import Mangum

# 导入你的主应用
from feishu_webhook_server import app  # 确保 feishu_webhook_server.py 在根目录或可导入路径

# Mangum 适配器，用于 ASGI 应用在 Serverless 环境运行
def handler(event, context):
    return app(event, context)

# 如果你用 Mangum
handler = Mangum(app)
