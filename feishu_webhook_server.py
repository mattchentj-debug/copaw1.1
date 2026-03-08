"""
飞书机器人 Webhook 接收服务器 (FastAPI)

用途：部署在公网服务器上，接收飞书群消息事件，并转发给本地智能体处理。
支持文本消息和 @提及触发。

部署建议：
- 使用 Vercel, Fly.io 或 AWS Lambda 等平台部署
- 设置环境变量 FEISHU_VERIFICATION_TOKEN 和 BOT_SECRET_KEY（用于验证签名）
- 在飞书开发者后台配置事件订阅回调 URL: https://<your-domain>/events

安装依赖：
    pip install fastapi uvicorn python-dotenv
    # 若需签名验证（推荐），还需：
    pip install cryptography

启动命令：
    uvicorn feishu_webhook_server:app --host 0.0.0.0 --port $PORT
"""

import os
import json
import hashlib
import hmac
from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件中的环境变量

app = FastAPI()

# ==================== 配置 ====================
# 建议通过环境变量设置，不要硬编码
VERIFICATION_TOKEN = os.getenv("FEISHU_VERIFICATION_TOKEN")  # 事件订阅的 verification token
ENCRYPT_KEY = os.getenv("FEISHU_ENCRYPT_KEY")  # 如果启用了加密

# 智能体处理函数（模拟）
async def process_message(event: Dict[str, Any]) -> str:
    """将消息交给 Copaw Agent 处理，返回回复文本"""
    msg_type = event.get("msg_type")
    content_str = event.get("content", "{}")
    
    try:
        content = json.loads(content_str)
    except Exception:
        content = {"text": content_str}

    text = content.get("text", "")
    sender_id = event.get("sender_id", {}).get("user_id", "unknown")
    
    # TODO: 此处可集成调用本地 Copaw Agent 的 API 或消息队列
    # 当前返回模拟响应
    response = f"收到你的消息啦！你说：{text}\n—— Copaw Agent 自动回复 @ {datetime.now().strftime('%H:%M')}, SenderID={sender_id}"
    
    return response


@app.post("/events")
async def handle_event(request: Request):
    body = await request.json()

    # 1. 验证请求来源（Verification Token）
    if body.get("token") != VERIFICATION_TOKEN:
        raise HTTPException(status_code=403, detail="Invalid verification token")

    # 2. 处理不同类型事件
    event_type = body.get("type")

    if event_type == "url_verification":
        # 飞书首次配置时会发送此事件，需回 echostr
        return {"challenge": body["challenge"]}
    
    elif event_type == "event_callback":
        event = body.get("event", {})
        msg_type = event.get("msg_type")
        chat_id = event.get("chat_id")

        # 只处理文本消息
        if msg_type == "text":
            # 提取内容并交由智能体处理
            reply_text = await process_message(event)
            
            # 调用飞书 API 发送回复（这里需要异步 HTTP 客户端）
            # 实际使用中应使用 httpx 或 requests + access_token
            # 示例伪代码如下：
            '''
            headers = {"Authorization": "Bearer <access_token>"}
            data = {
                "chat_id": chat_id,
                "msg_type": "text",
                "content": {"text": reply_text}
            }
            requests.post("https://open.feishu.cn/open-apis/im/v1/messages", json=data, headers=headers)
            '''
            print(f"[REPLY] To Chat: {chat_id} -> {reply_text}")

                    # 发送回复到飞书群
            import requests
            response_data = {
                "msg_type": "text",
                "content": {"text": reply_text}
            }
            webhook_url = os.getenv("FEISHU_BOT_WEBHOOK_URL")
            if webhook_url:
                try:
                    resp = requests.post(webhook_url, json=response_data)
                    print(f"[SENT] Status: {resp.status_code}, Response: {resp.text}")
                except Exception as e:
                    print(f"[ERROR] Failed to send message: {e}")
            else:
                print("[WARN] No webhook URL set")

        return {"status": "success"}

    else:
        return {"status": "ignored", "type": event_type}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
