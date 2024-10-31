import uvicorn  # 异步web服务器
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException  # 快速Web框架
import requests  # 发送 HTTP 请求
import time  # 时间处理

app = FastAPI()

# Coze API所需参数
coze_api_url = "https://api.coze.cn/open_api/v2/chat"
coze_api_token = "pat_agSEJHtfyWwVVHSbJxSO71zdyMvRc6htrvaTYdWsBVYecKHicpcNq4BuQ1k9939X"
coze_bot_id = "7427760647322451968"

# 机器人的昵称
bot_nickname = "超级无敌奶龙大帝"

# Coze API封装类
class Coze_API:
    def __init__(self, api_url, api_token, bot_id):
        self.api_url = api_url
        self.api_token = api_token
        self.bot_id = bot_id

    def send_request(self, conversation_id, user_id, query, stream=False):
        headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Host": "api.coze.cn",
            "Connection": "keep-alive"
        }
        data = {
            "conversation_id": str(conversation_id),  # 确保 conversation_id 是字符串
            "bot_id": str(self.bot_id),  # 确保 bot_id 是字符串
            "user": str(user_id),  # 确保 user_id 是字符串
            "query": str(query),  # 确保 query 是字符串
            "stream": stream
        }
        print(f"Sending request to {self.api_url} with data: {data}")  # 添加日志输出，查看请求数据
        response = requests.post(self.api_url, headers=headers, json=data)
        print(f"Response status code: {response.status_code}")  # 添加日志输出，查看响应状态码
        if response.status_code == 200:
            response_data = response.json()
            print(f"Response data: {response_data}")  # 添加日志输出，查看响应数据
            if response_data.get("code") == 0:  # 检查是否有错误代码
                messages = response_data.get("messages", [])
                for message in messages:
                    if message.get("type") == "answer":
                        return message.get("content", "")
                return "未找到有效回答"
            else:
                error_msg = response_data.get("msg", "未知错误")
                print(f"API error: {error_msg}")
                return f"API 错误: {error_msg}"
        else:
            print(f"Request failed, status code: {response.status_code}, response: {response.text}")  # 添加日志输出，查看失败原因
            return f"请求失败，状态码: {response.status_code}"

# 实例化Coze API
coze_api = Coze_API(coze_api_url, coze_api_token, coze_bot_id)

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

@app.post("/")
async def root(request: Request):
    try:
        data = await request.json()  # 获取事件数据
        print(f"Received data: {data}")  # 添加日志输出，查看接收到的数据
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid JSON format")

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
        response = coze_api.send_request("123", user_id, message_content)
        huixin(user_id, response)

    elif message_type == "group":
        # 群聊消息处理
        if bot_nickname in message_content:
            # 移除机器人的昵称，防止重复响应
            clean_message = message_content.replace(bot_nickname, "").strip()
            response = coze_api.send_request("123", user_id, clean_message)
            huiqun(group_id, response)

    else:
        output = (
            "程序:提示\n\n"
            f"自身ID:[{self_id}]\n"
            f"用户ID:[{user_id}]\n"
            f"接收时间:[{standard_time}]\n"
            f"消息内容:[消息类型不支持“{message_type}”]"
        )
        huixin(user_id, output)

    return {}

# WebSocket路由
@app.websocket("/onebot/v11/ws/")
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
        response = coze_api.send_request("123", user_id, message_content)
        huixin(user_id, response)

    elif message_type == "group":
        # 群聊消息处理
        if bot_nickname in message_content:
            # 移除机器人的昵称，防止重复响应
            clean_message = message_content.replace(bot_nickname, "").strip()
            response = coze_api.send_request("123", user_id, clean_message)
            huiqun(group_id, response)

    else:
        output = (
            "程序:提示\n\n"
            f"自身ID:[{self_id}]\n"
            f"用户ID:[{user_id}]\n"
            f"接收时间:[{standard_time}]\n"
            f"消息内容:[消息类型不支持“{message_type}”]"
        )
        huixin(user_id, output)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)