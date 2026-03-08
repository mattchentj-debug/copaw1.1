"""
发送测试消息到你的 Vercel 部署地址
用于验证飞书 Webhook 服务是否正常工作
"""

import requests
import json

# ✅ 替换为你的实际部署地址
VERCEL_URL = "https://copaw-feishu-bot.vercel.app/events"

# 测试用的消息体（模拟飞书回调）
with open("test_message.json", "r") as f:
    test_event = json.load(f)

print("🚀 正在发送测试消息...")
print(f"🎯 目标地址: {VERCEL_URL}")

try:
    resp = requests.post(VERCEL_URL, json=test_event, timeout=10)
    print(f"✅ 状态码: {resp.status_code}")
    print(f"📝 响应内容: {resp.text}")
    
    if resp.status_code == 200:
        print("🎉 恭喜！服务已正确响应，说明部署成功！")
    else:
        print("❌ 服务返回错误，请检查日志")
        
except Exception as e:
    print(f"🔴 请求失败: {e}")
    print("💡 可能原因：URL 错误、服务未上线、网络问题")

print("\n📌 下一步：")
print("1. 登录飞书开发者后台")
print("2. 配置事件订阅回调地址为该 URL")
print("3. 在群聊中 @机器人 测试真实消息")