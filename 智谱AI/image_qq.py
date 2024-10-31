import uvicorn  # 异步web服务器
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException  # 快速Web框架
import time  # 时间处理
import requests  # 发送 HTTP 请求
from datetime import datetime  # 调用时间模块
from zhipu_api import send_message, access_token ,assistant_id # 导入zhipu_api.py中的函数和访问令牌
import re  # 正则表达式

app = FastAPI()

def convert_to_standard_time(epoch_time):
    # 将时间戳转换为标准时间格式
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))

def extract_images(text):
    # 使用正则表达式提取 [图片说明](图片链接) 格式的图片
    pattern = r'\[(.*?)\]\((.*?)\)'
    matches = re.findall(pattern, text)
    return matches
'''
@app.post("/")
async def root(request: Request):
    try:
        data = await request.json()  # 获取事件数据
        print(f"Received data: {data}")  # 添加日志输出，查看接收到的数据
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid JSON format")

    self_id = data.get("self_id")
    user_id = data.get("user_id")
    group_id = data.get("group_id")  # 新增：获取群组ID
    epoch_time = data.get("time")
    # 将时间戳转换为标准时间格式
    standard_time = convert_to_standard_time(epoch_time)
    # 提取键type
    message_type = data.get("message_type")
    message_content = data.get("raw_message")

    if message_type == "private":
        # 私聊消息处理
        output = (
            "程序:测试返回\n\n"
            f"自身ID:[{self_id}]\n"
            f"用户ID:[{user_id}]\n"
            f"接收时间:[{standard_time}]\n"
            f"消息内容:[{message_content}]"
        )
        huixin(user_id, output)

        # 检查消息内容是否包含"时间"和"当前"
        if "时间" in message_content and "当前" in message_content:
            # 获取时间
            timestamp_1 = datetime.now().strftime("%Y.%m.%d")
            timestamp_2 = datetime.now().strftime("%H:%M:%S:%f")
            # 截取前面的12个字符，包括毫秒部分
            timestamp_3 = timestamp_2[:12]

            output = (
                "程序:测试时间返回\n\n"
                f"[{timestamp_1}{timestamp_3}]"
            )
            huixin(user_id, output)

    elif message_type == "group":
        # 群聊消息处理
        output = (
            "程序:测试返回\n\n"
            f"自身ID:[{self_id}]\n"
            f"群组ID:[{group_id}]\n"
            f"用户ID:[{user_id}]\n"
            f"接收时间:[{standard_time}]\n"
            f"消息内容:[{message_content}]"
        )
        huiqun(group_id, output)

        # 检查消息内容是否包含"时间"和"当前"
        if "时间" in message_content and "当前" in message_content:
            # 获取时间
            timestamp_1 = datetime.now().strftime("%Y.%m.%d")
            timestamp_2 = datetime.now().strftime("%H:%M:%S:%f")
            # 截取前面的12个字符，包括毫秒部分
            timestamp_3 = timestamp_2[:12]

            output = (
                "程序:测试时间返回\n\n"
                f"[{timestamp_1}{timestamp_3}]"
            )
            huiqun(group_id, output)

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
'''

# 发送私信
def huixin(user_id, data):
    print(f"Sending private message to user_id {user_id}: {data}")  # 添加日志输出，查看发送的消息
    requests.post('http://localhost:3000/send_private_msg', json={
        'user_id': user_id,  # 动态传入user_id
        'message': [{
            'type': 'text',
            'data': {
                'text': data
            }
        }]
    })

# 发送群聊消息
def huiqun(group_id, data):
    print(f"Sending group message to group_id {group_id}: {data}")  # 添加日志输出，查看发送的消息
    requests.post('http://localhost:3000/send_group_msg', json={
        'group_id': group_id,  # 动态传入group_id
        'message': [{
            'type': 'text',
            'data': {
                'text': data
            }
        }]
    })

# 发送图片
def send_image(user_id, image_urls):
    for image_url in image_urls:
        requests.post('http://localhost:3000/send_private_msg', json={
            'user_id': user_id,
            'message': [{
                'type': 'image',
                'data': {
                    'file': image_url
                }
            }]
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
    self_id = data.get("self_id")
    user_id = data.get("user_id")
    group_id = data.get("group_id")  # 新增：获取群组ID
    epoch_time = data.get("time")
    # 将时间戳转换为标准时间格式
    standard_time = convert_to_standard_time(epoch_time)
    # 提取键type
    message_type = data.get("message_type")
    message_content = data.get("raw_message")

    if message_type == "private":
        # 私聊消息处理
        response_generator = send_message(assistant_id, access_token, message_content)
        if isinstance(response_generator, str):
            # 处理图片链接
            matches = extract_images(response_generator)
            if matches:
                # 去掉图片链接的部分
                for match in matches:
                    response_generator = response_generator.replace(f"![{match[0]}]({match[1]})", "")
            huixin(user_id, response_generator)
            if matches:
                for match in matches:
                    send_image(user_id, [match[1]])
        elif isinstance(response_generator, list):  # 假设返回的是图片URL列表
            send_image(user_id, response_generator)

    elif message_type == "group":
        if "CQ:at,qq={bot_qq}" in message_content:
            message_content.replace("[CQ:at,qq={bot_qq},name={bot_name}]", "")
            # 群聊消息处理
            response_generator = send_message(assistant_id, access_token, message_content)
            if isinstance(response_generator, str):
                # 处理图片链接
                matches = extract_images(response_generator)
                if matches:
                    # 去掉图片链接的部分
                    for match in matches:
                        response_generator = response_generator.replace(f"[{match[0]}]({match[1]})", "")
                huiqun(group_id, response_generator)
                if matches:
                    for match in matches:
                        requests.post('http://localhost:3000/send_group_msg', json={
                            'group_id': group_id,
                            'message': [{
                                'type': 'image',
                                'data': {
                                    'file': match[1]
                                }
                            }]
                        })
            elif isinstance(response_generator, list):  # 假设返回的是图片URL列表
                for image_url in response_generator:
                    requests.post('http://localhost:3000/send_group_msg', json={
                        'group_id': group_id,
                        'message': [{
                            'type': 'image',
                            'data': {
                                'file': image_url
                            }
                        }]
                    })

    else:
        output = (
            "程序:提示\n\n"
            f"自身ID:[{self_id}]\n"
            f"用户ID:[{user_id}]\n"
            f"接收时间:[{standard_time}]\n"
            f"消息内容:[消息类型不支持“{message_type}”]"
        )
        # huixin(user_id, output)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
