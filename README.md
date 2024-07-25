# Juchats API wrapper.

Example:

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
        await juchats.chat("3.11 3.9 两个浮点数谁大？具体分析一下，给出你的原因。",
                                  show_stream=True)


if __name__ == '__main__':
    asyncio.run(api())
```
