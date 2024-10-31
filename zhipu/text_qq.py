import json

import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException
import requests
import time
from sseclient import SSEClient

app = FastAPI()

# API密钥和密钥
api_key = '4e2744fd61180342'
api_secret = '760e3e84b1e23d40b685df93ff6c8246'
assistant_id = "67188e7621bf6c257e2add6f"


# 获取访问令牌
def get_access_token(api_key, api_secret):
    url = "https://chatglm.cn/chatglm/assistant-api/v1/get_token"
    data = {"api_key": api_key, "api_secret": api_secret}
    response = requests.post(url, json=data)
    token_info = response.json()
    return token_info['result']['access_token']


# 初始化访问令牌
access_token = get_access_token(api_key, api_secret)


# 处理API响应
def handle_response(data_dict):
    message = data_dict.get("message")
    if message:
        content = message.get("content")
        if content:
            response_type = content.get("type")
            if response_type == "text":
                return content.get("text", "No text provided")
            elif response_type == "image":
                images = content.get("image", [])
                image_urls = ", ".join(image.get("image_url") for image in images)
                return image_urls
            elif response_type == "code":
                return content.get("code")
            elif response_type == "execution_output":
                return content.get("content")
            elif response_type == "system_error":
                return content.get("content")
            elif response_type == "tool_calls":
                return data_dict.get('tool_calls')
            elif response_type == "browser_result":
                content = json.loads(content.get("content", "{}"))
                return f"Browser Result - Title: {content.get('title')} URL: {content.get('url')}"
    return "No valid response"


# 发送消息给API
def send_message(assistant_id, access_token, prompt, conversation_id=None, file_list=None, meta_data=None):
    url = "https://chatglm.cn/chatglm/assistant-api/v1/stream"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "assistant_id": assistant_id,
        "prompt": prompt,
    }
    if conversation_id:
        data["conversation_id"] = conversation_id
    if file_list:
        data["file_list"] = file_list
    if meta_data:
        data["meta_data"] = meta_data

    # 发送请求并获取响应
    response = requests.post(url, json=data, headers=headers, stream=True)
    if response.status_code == 200:
        events = SSEClient(response.iter_lines())
        output = []
        for event in events:
            if event and event.data != "ping":
                data_dict = json.loads(event.data)
                output.append(handle_response(data_dict))
        return "\n".join(output)
    else:
        return f"Request failed with status code {response.status_code}"


# 发送私信
def huixin(user_id, data):
    print(f"Sending private message to user_id {user_id}: {data}")
    requests.post('http://localhost:3000/send_private_msg', json={'user_id': user_id, 'message': data})


# 发送群聊消息
def huiqun(group_id, data):
    print(f"Sending group message to group_id {group_id}: {data}")
    requests.post('http://localhost:3000/send_group_msg', json={'group_id': group_id, 'message': data})


# 处理消息
@app.post("/")
async def root(request: Request):
    try:
        data = await request.json()
        print(f"Received data: {data}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid JSON format")

    post_type = data.get("post_type")
    if post_type != "message":
        print(f"Ignoring non-message event: {post_type}")
        return {}

    self_id = data.get("self_id")
    user_id = data.get("user_id")
    group_id = data.get("group_id")
    epoch_time = data.get("time")
    standard_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))
    message_type = data.get("message_type")
    message_content = data.get("raw_message")

    if message_type == "private":
        response = send_message(assistant_id, access_token, prompt=message_content)
        huixin(user_id, response)
    elif message_type == "group":
        if "机器人昵称" in message_content:  # 替换为实际的机器人昵称
            clean_message = message_content.replace("机器人昵称", "").strip()
            response = send_message(assistant_id, access_token, prompt=clean_message)
            huiqun(group_id, response)
    else:
        output = (
            "程序:提示\n\n"
            f"自身ID:[{self_id}]\n"
            f"用户ID:[{user_id}]\n"
            f"接收时间:[{standard_time}]\n"
            f"消息内容:[消息类型不支持“{message_type}”]"
        )
    return {}


# WebSocket路由
@app.websocket("/onebot/v11/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connection accepted")
    try:
        while True:
            data = await websocket.receive_json()
            print(f"Received WebSocket data: {data}")
            await handle_websocket_data(websocket, data)
    except WebSocketDisconnect:
        print("WebSocket connection closed")


async def handle_websocket_data(websocket: WebSocket, data: dict):
    post_type = data.get("post_type")
    if post_type != "message":
        print(f"Ignoring non-message event: {post_type}")
        return

    self_id = data.get("self_id")
    user_id = data.get("user_id")
    group_id = data.get("group_id")
    epoch_time = data.get("time")
    standard_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))
    message_type = data.get("message_type")
    message_content = data.get("raw_message")

    if message_type == "private":
        response = send_message(assistant_id, access_token, prompt=message_content)
        huixin(user_id, response)
    elif message_type == "group":
        if "机器人昵称" in message_content:  # 替换为实际的机器人昵称
            clean_message = message_content.replace("机器人昵称", "").strip()
            response = send_message(assistant_id, access_token, prompt=clean_message)
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