<div align="center">
<figure style="text-align: center; radius:10pt">
    <img src="https://s3.bmp.ovh/imgs/2024/07/29/b6995f3a712d6586.png" width=139pt radius=10pt>
</figure>

![visitors](https://visitor-badge.laobi.icu/badge?page_id=ultrasev.juchats&left_color=green&right_color=red) [![GitHub](https://img.shields.io/github/stars/ultrasev/juchats?style=social)](https://github.com/ultrasev/juchats)

</div>

# [Juchats](https://dlj.one/RNFYxz9) API 封装

[English](README_EN.md) | [中文](README.md)

C 大产品 [hermchats](https://hermchats.com) 的 API 封装，可以无缝集成到代码中，用于数据分析、清洗或者对话生成都还不错。支持 GPT-4、o1-mini、Claude Sonnet、deepseek 等一众模型。 Hermchats 新模型上的很快，像 `o1-mini` 这样的模型，官方上线后，Hermchats 很快就会支持。

针对不同模型，免费用户每天都有几十次到上千次不等的使用次数，比如，每天可以使用 claude-sonnet-3.5 进行 30 轮对话，用 deepseek 进行 10000 次对话，非常良心的网站，有需要的可以付费支持一下 [hermchats](https://hermchats.com)。

# 安装

```bash
pip3 install juchats
```

# 使用方法

首先，从 [Juchats](https://dlj.one/RNFYxz9) 官方网站获取令牌（jtoken），并将其放入 `.env` 文件中。
令牌获取方式就很简单了，浏览器上开 F12，刷新一下界面，随便找一个带有 hermchats.com 的链接，从 Cookie 中找到 `jtoken` 字段，复制即可。

```bash
JTOKEN=your_token
```

# 示例

## 异步对话生成

使用 `deepseek-chat` 模型，以异步方式进行对话生成。

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


''' 输出
3.11 大，因为 3.11 > 3.9
'''
```

## 结构化 JSON 输出

```python
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

''' 输出
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
```

## 参数设置

### 模型选择

Juchats 支持多种模型，您可以在创建 Juchats 实例时指定模型，完整的模型列表可以参考下面。

```python
juchats = Juchats(token, model='gpt-4')
```

### 流式输出

要启用流式输出，请在调用 `chat` 方法时设置 `show_stream=True`，不然会返回一个字符串。

```python
await juchats.chat("你好，请介绍一下你自己。", show_stream=True)
```

# 可用模型

Backend model name 是代码中使用的模型名称，front name 是在 Juchats 网站上显示的模型名称。前者是给代码用的，后者是给用户看的。

![models](https://apionpages.cufo.cc/api/juchatmodels)

## 获取实时可用模型

动态获取 Juchats API 最新可用的模型。

```python
import os
from juchats.chat import Juchats
from dotenv import load_dotenv

load_dotenv()
token = os.getenv('JTOKEN')

juchats = Juchats(token, model='ol-mini')
print(
    asyncio.run(juchats.get_models())
)
```

# 注意事项

- **速率限制**：API 支持每秒最多 3 次查询（QPS），减少调用频率。
- **模型选择**：指定模型时，使用 backend model name。

## 贡献

欢迎贡献！请随时提交问题或拉取请求。

## 许可证

本项目采用 MIT 许可证。详情请参阅 [LICENSE](LICENSE) 文件。
