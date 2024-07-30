<div align="center">
<figure style="text-align: center; radius:10pt">
    <img src="https://s3.bmp.ovh/imgs/2024/07/29/b6995f3a712d6586.png" width=239pt radius=10pt>
</figure>

<a href='https://follow-your-click.github.io/'><img src='https://img.shields.io/badge/Project-Page-Green'></a> ![visitors](https://visitor-badge.laobi.icu/badge?page_id=ultrasev.juchats&left_color=green&right_color=red) [![GitHub](https://img.shields.io/github/stars/ultrasev/juchats?style=social)](https://github.com/ultrasev/juchats)

</div>

# [Juchats](https://dlj.one/RNFYxz9) API wrapper

`juchats` lib is a Python library designed for interacting with the Juchats API, enabling seamless integration of chat functionalities into your applications. By utilizing this library, developers can leverage the power of advanced models like GPT-4, Claude Mezzo, and deepseek to perform various chat-related tasks.

# Installation

```bash
pip3 install juchats
```

# Usage

First, obtain your token from from [Juchats](https://dlj.one/RNFYxz9) official website, and place it into a `.env` file.

```bash
JTOKEN=your_token
```

## Basic Chat Interaction

This example demonstrates a simple chat interaction where we ask the model to compare two floating-point numbers.

```python
import os
from juchats.chat import Juchats
from dotenv import load_dotenv
import asyncio
load_dotenv()

async def api():
    token = os.getenv('JTOKEN')
    juchats = Juchats(token, model='deepseek-chat')

    async with juchats:
        await juchats.chat("3.11, 3.9 两个浮点数谁大？具体分析一下，给出你的原因", show_stream=True)

if __name__ == '__main__':
    asyncio.run(api())


''' Output
3.11 大，因为 3.11 > 3.9
'''
```

## Structured JSON output

This example demonstrates how to obtain structured JSON output from the chat API.

````python
import os
from juchats.chat import Juchats
from dotenv import load_dotenv
import asyncio
load_dotenv()

async def api():
    token = os.getenv('JTOKEN')
    juchats = Juchats(token, model='deepseek-chat')
    prompt = "每个月有多少天？以 JSON 格式给出答案，例如：{\"January\": 31, \"February\": 28, ...}"
    async with juchats:
        text = await juchats.chat(prompt)
        print(text)

''' Output
```json
{
    "January": 31,
    "February": 28,
    "March": 31,
    "April": 30,
    "May": 31,
    "June": 30,
    "July": 31,
    "August": 31,
    "September": 30,
    "October": 31,
    "November": 30,
    "December": 31
}
'''
````

# Available Models

By 2024-07-25, the available models (may be outdated) are:

| Model ID | Backend Model Name                 | Front Model Name         |
| -------- | ---------------------------------- | ------------------------ |
| 5        | claude-3-haiku-20240307            | Claude Mezzo             |
| 6        | claude-3-opus-20240229             | Claude3 Opus             |
| 7        | mistralai/mixtral-8x22b-instruct   | Mixtral Forte            |
| 9        | gpt-4-turbo-2024-04-09             | GPT Mezzo                |
| 10       | gpt-4-turbo-2024-04-09             | GPT Forte                |
| 11       | dall-e-3                           | DALL · E3                |
| 12       | meta-llama/llama-3-70b-instruct    | Llama3 70B               |
| 13       | google/gemini-pro-1.5              | Gemini 1.5 Pro           |
| 14       | deepseek-chat                      | Deepseek                 |
| 15       | google/gemini-flash-1.5            | Gemini-flash             |
| 16       | gpt-4o-2024-05-13                  | GPT4o                    |
| 17       | claude-3-opus-20240229             | Claude3 Opus(100K)       |
| 18       | Stable Image Ultra                 | Stable Diffusion 3 Ultra |
| 19       | claude-3-5-sonnet-20240620         | Claude 3.5 Sonnet        |
| 20       | gpt-4o-mini-2024-07-18             | GPT4o-mini               |
| 21       | meta-llama/llama-3.1-405b-instruct | Llama3.1 405B            |

## Get real time available models

Dynamically retrieve the latest available models from the Juchats API.

```python
import os
from juchats.chat import Juchats
from dotenv import load_dotenv
import asyncio
load_dotenv()
token = os.getenv('JTOKEN')
juchats = Juchats(token, model='gpt-4o-2024-05-13')
print(
    asyncio.run(juchats.get_models())
)
```

# Note

- **Streaming**: Set `show_stream=True` to display the chat response in real-time. Use `show_stream=False` to disable it.
- **Model Selection**: Specify the backend model name with the `model` parameter. Refer to the available models table above for options.
- **API Token**: Obtain your token from [Juchats](https://dlj.one/RNFYxz9) and use it to authenticate requests.
- **Rate Limiting**: The API supports up to 3 queries per second (QPS). For higher limits, consider using the Deepseek API or OpenAI API.
