import json
import requests

# API密钥和密钥秘密
api_key = '4e2744fd61180342'
api_secret = '760e3e84b1e23d40b685df93ff6c8246'
assistant_id = "67188e7621bf6c257e2add6f"

def get_access_token(api_key, api_secret):
    url = "https://chatglm.cn/chatglm/assistant-api/v1/get_token"
    data = {
        "api_key": api_key,
        "api_secret": api_secret
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        token_info = response.json()
        return token_info['result']['access_token']
    else:
        raise Exception(f"Failed to get access token: {response.status_code} - {response.text}")

def handle_response(data_dict):
    message = data_dict.get("message")
    if message:
        content = message.get("content")
        if content:
            response_type = content.get("type")
            if response_type == "text":
                text = content.get("text", "No text provided")
                return f"{text}"

            elif response_type == "image":
                images = content.get("image", [])
                image_urls = ", ".join(image.get("image_url") for image in images)
                return f"{image_urls}"

            elif response_type == "code":
                return f"{content.get('code')}"

            elif response_type == "execution_output":
                return f"{content.get('content')}"

            elif response_type == "system_error":
                return f"{content.get('content')}"

            elif response_type == "tool_calls":
                tool_calls = content.get("tool_calls")
                if isinstance(tool_calls, str):
                    # 尝试将字符串解析为JSON
                    try:
                        tool_calls = json.loads(tool_calls)
                    except json.JSONDecodeError:
                        # 如果解析失败，直接返回字符串
                        return f"Tool Calls: {tool_calls}"

                # 处理解析后的数据
                if isinstance(tool_calls, list):
                    tool_call_details = []
                    for tool_call in tool_calls:
                        if isinstance(tool_call, dict):
                            name = tool_call.get("name")
                            arguments = tool_call.get("arguments")
                            tool_call_details.append(f"Name: {name}, Arguments: {arguments}")
                        else:
                            tool_call_details.append(f"Invalid tool call: {tool_call}")
                    return f"Tool Calls: {', '.join(tool_call_details)}"
                else:
                    return f"Invalid tool calls format: {tool_calls}"

            elif response_type == "browser_result":
                browser_result = json.loads(content.get("content", "{}"))
                return f"Browser Result - Title: {browser_result.get('title')} URL: {browser_result.get('url')}"

            elif response_type == "function_result":
                function_result = content.get("content")
                if isinstance(function_result, str):
                    try:
                        function_result = json.loads(function_result)
                    except json.JSONDecodeError:
                        return f"Function Result: {function_result}"

                if isinstance(function_result, list):
                    function_results = []
                    for result in function_result:
                        if isinstance(result, dict):
                            status = result.get("status")
                            message = result.get("message")
                            result_content = result.get("result")
                            rid = result.get("rid")
                            if status == 0:
                                function_results.append(f"Function call successful, result: {result_content}, request ID: {rid}")
                            else:
                                function_results.append(f"Function call failed, error message: {message}, request ID: {rid}")
                        else:
                            function_results.append(f"Invalid function result: {result}")
                    return f"Function Results: {', '.join(function_results)}"
                elif isinstance(function_result, dict):
                    status = function_result.get("status")
                    message = function_result.get("message")
                    result_content = function_result.get("result")
                    rid = function_result.get("rid")
                    if status == 0:
                        return f"Function call successful, result: {result_content}, request ID: {rid}"
                    else:
                        return f"Function call failed, error message: {message}, request ID: {rid}"
                else:
                    return f"Invalid function result format: {function_result}"

            elif response_type == "rag_slices":
                rag_slices = content.get("content", [])
                return f"RAG Slices: {rag_slices}"

            else:
                return "Unknown message type"

    return "Invalid message"

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

    with requests.post(url, json=data, headers=headers, stream=True) as response:
        if response.status_code == 200:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    if decoded_line.startswith('data:'):
                        data_dict = json.loads(decoded_line[5:])
                        output = handle_response(data_dict)
        else:
            return "Request failed", response.status_code
        print(output)
        return output

# 获取访问令牌
token = get_access_token(api_key, api_secret)
access_token = token

if __name__ == '__main__' :
    prompt = "帮我找一张奶龙的图片"
    result = send_message(assistant_id, access_token, prompt)