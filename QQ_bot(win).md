# 基于QQNT架构的机器人配置手册

[QQ机器人文档](https://bot.q.qq.com/wiki/develop/api-v2/openapi/emoji/model.html#EmojiType)

[LLonebot快速上手](https://llob.napneko.com/zh-CN/develop/quick-start)

帮助中心：[CQ码/CQ Code](https://docs.go-cqhttp.org/cqcode)、[事件](https://docs.go-cqhttp.org/event)

离谱问题我一定要写在前面

![image-20241030211017262](C:\Users\86139\AppData\Roaming\Typora\typora-user-images\image-20241030211017262.png)

问题：403 拒绝连接

![image-20241030211035504](C:\Users\86139\AppData\Roaming\Typora\typora-user-images\image-20241030211035504.png)

![image-20241030211042827](C:\Users\86139\AppData\Roaming\Typora\typora-user-images\image-20241030211042827.png)

解决办法就是把‘/’删了

## 软件与插件安装

### 1、QQ最新版（即NT架构版）

### 2、PyCharm/VsCode

我使用的是Python 3.11

软件包安装：

Tip：如果请求超时就用镜像网址或者翻墙，下载报错先关闭当前终端重开。

网络波动检查网络或者等。

### 3、[LiteLoaderQQNT](https://github.com/Mzdyl/LiteLoaderQQNT_Install/releases)

一键安装

![image-20241030211259168](C:\Users\86139\AppData\Roaming\Typora\typora-user-images\image-20241030211259168.png)

![image-20241030211309118](C:\Users\86139\AppData\Roaming\Typora\typora-user-images\image-20241030211309118.png)

### 4、[LLOneBot](https://github.com/LLOneBot/LLOneBot/releases/tag/v4.0.13)（一般会在上一步自动安装）

下载 LLOneBot 最新版本 解压放到 plugins 目录下，然后重启 QQ 即可

## 对接配置

### 配置[Koishi](https://koishi.chat/zh-CN/manual/usage/market.html)

~~(好像可以不安装这个，如果不用的话，或者说是选一个)~~

**1. 在 Koishi 插件市场搜索并安装 adapter-onebot**[​](https://llonebot.github.io/zh-CN/guide/configuration#_1-%E5%9C%A8-koishi-%E6%8F%92%E4%BB%B6%E5%B8%82%E5%9C%BA%E6%90%9C%E7%B4%A2%E5%B9%B6%E5%AE%89%E8%A3%85-adapter-onebot)

![image-20241031111242295](C:\Users\86139\AppData\Roaming\Typora\typora-user-images\image-20241031111242295.png)

**2. 配置 adapter-onebot**[​](https://llonebot.github.io/zh-CN/guide/configuration#_2-%E9%85%8D%E7%BD%AE-adapter-onebot)

这里以 WS 反向连接为例

填写 selfId 为你的机器人的 QQ 号

token 可以为空，需与 LLOneBot 配置的 token 一致

protocol 选择 ws-reverse

其他配置保持默认即可，保存配置然后启用插件

**3. 配置完成后，LLOneBot 添加 WS 反向地址**[​](https://llonebot.github.io/zh-CN/guide/configuration#_3-%E9%85%8D%E7%BD%AE%E5%AE%8C%E6%88%90%E5%90%8E-llonebot-%E6%B7%BB%E5%8A%A0-ws-%E5%8F%8D%E5%90%91%E5%9C%B0%E5%9D%80)

adapter-onebot 的 WS 反向地址为 ws://127.0.0.1:5140/onebot

### 配置[Nonebot](https://nonebot.dev/docs/quick-start)

安装脚手架​

​		确保你已经安装了 Python 3.9 及以上版本，然后在命令行中执行以下命令：

安装 pipx

```bash
python -m pip install --user pipx

python -m pipx ensurepath
```

​		如果在此步骤的输出中出现了“open a new terminal”或者“re-login”字样，那么请关闭当前终端并重新打开一个新的终端。

安装脚手架

```bash
pipx install nb-cli
```

如果当前识别不了pipx指令就关闭当前窗口，新建一个即可解决。

​		安装完成后，你可以在命令行使用 nb 命令来使用脚手架。如果出现无法找到命令的情况（例如出现“Command not found”字样），请参考 pipx 文档 检查你的环境变量。

#### [创建项目](https://nonebot.dev/docs/quick-start#创建项目)

使用脚手架来创建一个项目：

```bash
nb create
```

这一指令将会执行创建项目的流程，你将会看到一些询问：

1. ##### 项目模板

   ```bash
   [?] 选择一个要使用的模板: bootstrap (初学者或用户)
   ```

   这里我们选择 `bootstrap` 模板，它是一个简单的项目模板，能够安装商店插件。如果你需要**自行编写插件**，这里请选择 `simple` 模板。

2. ##### 项目名称

   ```bash
   [?] 项目名称: awesome-bot
   ```

   这里我们以 `awesome-bot` 为例，作为项目名称。你可以根据自己的需要来命名。

3. ##### 其他选项 请注意，多选项使用**空格**选中或取消，**回车**确认。

   ```bash
   [?] 要使用哪些驱动器? FastAPI (FastAPI 驱动器)
   [?] 要使用哪些适配器? Console (基于终端的交互式适配器)
   [?] 立即安装依赖? (Y/n) Yes
   [?] 创建虚拟环境? (Y/n) Yes
   ```

   这里我们选择了创建虚拟环境，nb-cli 在之后的操作中将会自动使用这个虚拟环境。如果你不需要自动创建虚拟环境或者已经创建了其他虚拟环境，nb-cli 将会安装依赖至当前激活的 Python 虚拟环境。

4. ##### 选择内置插件

   ```bash
   [?] 要使用哪些内置插件? echo
   ```

   这里我们选择 `echo` 插件作为示例。这是一个简单的复读回显插件，可以用于测试你的机器人是否正常运行。

#### [运行项目](https://nonebot.dev/docs/quick-start#运行项目)

在项目创建完成后，你可以在**项目目录**中使用以下命令来运行项目：

```bash
nb run
```

​		你现在应该已经运行起来了你的第一个 NoneBot 项目了！请注意，生成的项目中使用了 `FastAPI` 驱动器和 `Console` 适配器，你之后可以自行修改配置或安装其他适配器。

#### [尝试使用](https://nonebot.dev/docs/quick-start#尝试使用)

​		在项目运行起来后，`Console` 适配器会在你的终端启动交互模式，你可以直接在输入框中输入 `/echo hello world` 来测试你的机器人是否正常运行。

## QQ接收与发送消息

```python
import uvicorn  # 异步web服务器
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, HTTPException  # 快速Web框架
import time  # 时间处理
import requests  # 发送 HTTP 请求
from datetime import datetime  # 调用时间模块

app = FastAPI()

def convert_to_standard_time(epoch_time):
    # 将时间戳转换为标准时间格式
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(epoch_time))

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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
```



## API选择与注册

[讯飞星火大模型](https://xinghuo.xfyun.cn/sparkapi?ch=bytg-api01&msclkid=92b8e323883c124631ba843ca652d9b8)

[扣子(豆包)](https://www.coze.cn/open)

[通义千问](https://help.aliyun.com/zh/model-studio/developer-reference/?spm=a2c4g.11186623.0.0.2cdb2562NuNqCs)

[智谱清言](https://open.bigmodel.cn/)

[文心一言](https://console.bce.baidu.com/qianfan/overview)