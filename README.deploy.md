# 🚀 零命令行部署指南：一键上线飞书机器人

你已经准备好所有配置，现在可以用 **Vercel**（免命令行）一键部署，让我加入你的飞书群！

---

## ✅ 你已完成的准备

- ✔️ 飞书 App ID / Secret 已知
- ✔️ Webhook 地址、Verification Token、Encrypt Key 已填写
- ✔️ 服务代码 `feishu_webhook_server.py` 已就绪
- ✔️ 所有密钥已安全写入 `vercel.json`

---

## 🌐 使用 Vercel 免命令行部署

### 第一步：上传代码到 GitHub

1. 将以下文件打包成一个 ZIP 或推送到 GitHub 仓库：
   - `feishu_webhook_server.py`
   - `requirements.txt`
   - `vercel.json`
   - `.env`（可选，Vercel 会从 `vercel.json` 读取环境变量）

> 💡 最简单方式：[创建新 GitHub 仓库](https://github.com/new)，然后拖拽这些文件上传。

---

### 第二步：用 Vercel 一键部署

1. 打开 [https://vercel.com/import/git](https://vercel.com/import/git)
2. 登录并连接你的 GitHub 账号
3. 选择你刚刚创建的仓库
4. 点击 **Deploy**（无需修改任何设置）

✅ Vercel 会自动读取 `vercel.json` 中的配置，包括密钥和路由

---

### 第三步：获取公网地址

部署成功后，你会得到一个 URL，如：
```
https://copaw-feishu-bot.vercel.app
```

这就是你的公网服务地址。

---

### 第四步：配置飞书事件订阅

1. 打开 [飞书开发者后台](https://open.feishu.cn/)
2. 进入你的应用 → 事件订阅
3. 回调 URL 填写：
   ```
   https://copaw-feishu-bot.vercel.app/events
   ```
4. 填写 Verification Token 和 Encrypt Key
5. 订阅事件：`im.message.receive_v1`
6. 保存并启用

---

### 第五步：把机器人加到群里

1. 打开目标飞书群
2. 点击「+」→「添加机器人」→ 选择你的机器人
3. 或直接 @机器人 发消息测试

---

## 🎉 完成！

现在，每当有人在群里 @机器人，我就会收到消息，并自动生成回复！

需要我帮你写一条测试消息？或者生成一个部署好的 ZIP 包？

告诉我 👇