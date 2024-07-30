# [Juchats](https://dlj.one/RNFYxz9) API wrapper

<img src='https://s3.bmp.ovh/imgs/2024/07/29/b6995f3a712d6586.png' width=132>

# Installation

```bash
pip3 install juchats
```

# Example

First, you need to get the token from [Juchats](https://dlj.one/RNFYxz9). And put it in the `.env` file.

```bash
JTOKEN=your_token
```

## Chat

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
        await juchats.chat("3.11 3.9 两个浮点数谁大？具体分析一下，给出你的原因", show_stream=True)

if __name__ == '__main__':
    asyncio.run(api())


''' Output
3.11 大，因为 3.11 > 3.9
'''
```

## Structured output

```python
import os
from juchats.chat import Juchats
from dotenv import load_dotenv
import asyncio
load_dotenv()

async def api():
    token = os.getenv('JTOKEN')
    juchats = Juchats(token, model='deepseek-chat')
    prompt = "3.11 3.9 两个浮点数谁大？具体分析一下，给出你的原因。以 json 格式输出。示例 {\"a\": 3.11, \"b\": 3.9, \"result\": \"a\"}"
    async with juchats:
        text = await juchats.chat(prompt)
        print(text)

''' Output
{
    "a": 3.11,
    "b": 3.9,
    "result": "a"
}
'''
```

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

- `show_stream=True` will show the stream of the chat, `show_stream=False` will not show the stream of the chat.
- `model` is the backend model name, you can find it from the table above.
- `token` is the token of the chat, you can get it from [Juchats](https://dlj.one/RNFYxz9).
- QPS limit: $n \leq 3$ QPS, if you need more, please use deepseek API or OpenAI API.
