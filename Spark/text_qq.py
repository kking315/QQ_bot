import uvicorn  # 异步web服务器
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException  # 快速Web框架
import requests  # 发送 HTTP 请求
import time  # 时间处理
import SparkApi
import schedule
import threading


# 定义一个异步上下文管理器函数
async def lifespan_handler(app):
    # 应用启动时执行的代码
    thread = threading.Thread(target=start_schedule)
    thread.daemon = True  # 设置为守护线程，这样当主线程结束时它也会被终止
    thread.start()
    print("Application startup complete.")
    yield
    # 应用关闭时执行的代码
    print("Application shutdown complete.")


# 注册生命周期事件处理器
app = FastAPI(lifespan=lifespan_handler)

# Spark API所需参数
appid = "******"  # 替换为你的APPID
api_secret = "******"  # 替换为你的APISecret
api_key = "******"  # 替换为你的APIKey
domain = "generalv3.5"
Spark_url = "wss://spark-api.xf-yun.com/v3.5/chat"

# Spark API调用封装
def spark_api(question):
    text = [{"role": "user", "content": question}]
    SparkApi.answer = ""
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, text)
    return SparkApi.answer


# 发送私信
def huixin(user_id, data):
    print(f"Sending private message to user_id {user_id}: {data}")  # 添加日志输出，查看发送的消息
    requests.post('http://localhost:3000/send_private_msg', json={
        'user_id': user_id,  # 动态传入user_id
        'message': data
    })


# 发送群聊消息
def huiqun(group_id, data):
    print(f"Sending group message to group_id {group_id}: {data}")  # 添加日志输出，查看发送的消息
    requests.post('http://localhost:3000/send_group_msg', json={
        'group_id': group_id,  # 动态传入group_id
        'message': data
    })

# WebSocket路由
@app.websocket("/onebot/v11/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection accepted")
    try:
        while True:
            data = await websocket.receive_json()
            print(f"Received WebSocket data: {data}")
            # 处理接收到的数据
            await handle_websocket_data(websocket, data)
    except WebSocketDisconnect:
        print("WebSocket connection closed")


async def handle_websocket_data(websocket: WebSocket, data: dict):
    post_type = data.get("post_type")
    if post_type != "message":
        print(f"Ignoring non-message event: {post_type}")
        return {}

    self_id = data.get("self_id")
    user_id = data.get("user_id")
    group_id = data.get("group_id")  # 新增：获取群组ID
    epoch_time = data.get("time")
    # 将时间戳转换为标准时间格式
    standard_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))
    # 提取键type
    message_type = data.get("message_type")
    message_content = data.get("raw_message")

    if message_type == "private":
        # 私聊消息处理
        if "纪念日" in message_content:
            huixin(user_id, handle_jinianri_message())
        else:
            response = spark_api(message_content)
            huixin(user_id, response)

    elif message_type == "group":
        # 群聊消息处理
        if bot_nickname in message_content:
            # 移除机器人的昵称，防止重复响应
            clean_message = message_content.replace(bot_nickname, "").strip()
            if "纪念日" in clean_message:
                huiqun(group_id, handle_jinianri_message())
            else:
                response = spark_api(clean_message)
                huiqun(group_id, response)

    else:
        output = (
            "程序:提示\n\n"
            f"自身ID:[{self_id}]\n"
            f"用户ID:[{user_id}]\n"
            f"接收时间:[{standard_time}]\n"
            f"消息内容:[消息类型不支持“{message_type}”]"
        )
        #huixin(user_id, output)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
