import uvicorn  # 异步web服务器
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException  # 快速Web框架
import requests  # 发送 HTTP 请求
import time  # 时间处理
import SparkApi
import schedule
import threading
from datetime import datetime, timedelta
import random  # 用于生成随机早安语句


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
appid = "a0cc3e1f"  # 替换为你的APPID
api_secret = "NGYyMzc5YTUwMjNiYjA1ZDY0MTk3Njhk"  # 替换为你的APISecret
api_key = "4afed56cb120bc5afee0c9798c783f79"  # 替换为你的APIKey
domain = "generalv3.5"
Spark_url = "wss://spark-api.xf-yun.com/v3.5/chat"

# 机器人的昵称
bot_nickname = "超级无敌奶龙大帝"


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


# 计算从2024年6月29日到现在的天数
def calculate_days_since_2024_06_29():
    target_date = datetime(2024, 6, 29)
    current_date = datetime.now()
    delta = current_date - target_date
    return delta.days


# 计算下一个百天纪念日
def calculate_next_hundred_day(current_days):
    next_hundred_day = ((current_days // 100) + 1) * 100 - current_days
    return next_hundred_day


# 计算距离下一个整年的天数
def calculate_days_to_next_year(current_days):
    years_passed = current_days // 365
    next_year_days = (years_passed + 1) * 365 - current_days
    return next_year_days, years_passed + 1


# 计算距离下一个生日的天数
def calculate_days_to_next_birthday(birthdate):
    current_date = datetime.now()
    next_birthday = datetime(current_date.year, birthdate.month, birthdate.day)
    if next_birthday < current_date:
        next_birthday = datetime(current_date.year + 1, birthdate.month, birthdate.day)
    days_to_next_birthday = (next_birthday - current_date).days
    return days_to_next_birthday


# 处理纪念日消息
def handle_jinianri_message():
    days_since_2024_06_29 = calculate_days_since_2024_06_29()
    next_hundred_day = calculate_next_hundred_day(days_since_2024_06_29)

    if days_since_2024_06_29 < 1000:
        message = f"在一起已经 {days_since_2024_06_29} 天了！\n距离我们在一起第{((days_since_2024_06_29 // 100 + 1) * 100)}天还有 {next_hundred_day} 天。"
    else:
        days_to_next_year, years_to_next_year = calculate_days_to_next_year(days_since_2024_06_29)
        message = f"在一起已经 {days_since_2024_06_29} 天了！\n距离我们在一起第{years_to_next_year}年还有 {days_to_next_year} 天。"

    # 计算距离下一个生日的天数
    chen_wanting_birthday = datetime(2004, 3, 3)
    liu_junkang_birthday = datetime(2004, 5, 3)
    days_to_chen_wanting_birthday = calculate_days_to_next_birthday(chen_wanting_birthday)
    days_to_liu_junkang_birthday = calculate_days_to_next_birthday(liu_junkang_birthday)

    message += f"\n距离陈琬婷的生日还有 {days_to_chen_wanting_birthday} 天。\n距离刘俊康的生日还有 {days_to_liu_junkang_birthday} 天。"

    return message  # 返回处理后的消息字符串

# 获取天气情况，新增location参数
def get_weather(location="武汉市江夏区"):
    # 使用Spark API询问特定地区的当前天气
    weather_question = f"请问{location}今天的天气如何？"
    weather_response = spark_api(weather_question)
    return weather_response


# 生成随机早安语句
def generate_morning_greeting():
    greetings = [
        "早安！新的一天，新的开始。",
        "早上好！愿你今天充满活力。",
        "早安！美好的一天从这里开始。",
        "早上好！愿你今天心情愉快。",
        "早安！愿你今天事事顺利。"
    ]
    return random.choice(greetings)


# 定义一个函数来执行定时任务
def send_scheduled_good_morning():
    user_id = "2958432473"  # 指定用户的ID
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    greeting = generate_morning_greeting()
    location = "武汉市江夏区"  # 指定查询天气的地点
    weather = get_weather(location)

    # 构建消息内容
    message = (
        f"{current_time}\n\n"
        f"{greeting}\n\n"
        f"{weather}\n\n"
    )

    # 添加纪念日信息
    message += handle_jinianri_message()

    # 发送消息
    huixin(user_id, message)

def send_scheduled_goodnight():
    user_id = "2958432473"  # 指定用户的ID
    message = "时间不早咯！该睡觉啦！"

    huixin(user_id, message)

# 使用schedule库来安排定时任务
def start_schedule():
    # 每天早上八点执行一次send_scheduled_good_morning函数
    schedule.every().day.at("08:00").do(send_scheduled_good_morning)
    # 每天晚上十一点执行一次send_scheduled_goodnight函数
    schedule.every().day.at("23:00").do(send_scheduled_goodnight)

    while True:
        schedule.run_pending()
        time.sleep(1)


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
        huixin(user_id, output)

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
        huixin(user_id, output)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)