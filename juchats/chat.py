import asyncio
import json
import typing
from uuid import uuid4
import time

import httpx
import pydantic
import websockets
from loguru import logger
import redislite

from .configs import APIS, HEADERS
from .types import Mode


def get_headers(token: str):
    headers = HEADERS
    headers['jtoken'] = token
    return headers


class Juchats(object):
    _modes = None
    _redis = redislite.Redis('/tmp/juchats_redis.db')

    def __init__(self, token: str, model: str = "deepseek-chat"):
        self.token = token
        self.model = model
        self._header = get_headers(token)
        self._model_id = None
        self._dialog_id = None
        self._initialized = False

    async def initialize(self):
        if self._initialized:
            return

        available_models = await self.get_models()
        for mode in available_models:
            if mode.name == self.model:
                self._model_id = mode.id
                break
        else:
            print(available_models)
            for mode in available_models:
                print(mode.id, mode.name)
            raise ValueError(f"Model {self.model} not found")

        self._initialized = True

    async def _ensure_initialized(self):
        if not self._initialized:
            await self.initialize()

    async def get_models(self) -> typing.List[Mode]:
        # Try to get models from Redis cache
        cached_models = self._redis.get('models')
        if cached_models:
            logger.info("get models from cache")
            cached_data = json.loads(cached_models)
            if time.time() < cached_data['expiry']:
                return [Mode(**x) for x in cached_data['modes']]

        # If not in cache or expired, fetch from API
        async with httpx.AsyncClient() as client:
            response = await client.get(APIS.MODES, headers=self._header)
            data = response.json()['data']
            modes = []
            for item in data:
                modes.extend([Mode(**x) for x in item['modes']])

            # Cache the result in Redis with 1-hour expiry
            cache_data = {
                'modes': [mode.dict() for mode in modes],
                'expiry': time.time() + 3600  # 1 hour from now
            }
            self._redis.set('models', json.dumps(cache_data))

            return modes

    async def get_dialog_id(self) -> int:
        async with httpx.AsyncClient() as client:
            response = await client.post(APIS.DIALOGS,
                                         headers=self._header,
                                         json={})
            response.raise_for_status()
            data = response.json()['data']
            for x in data:
                if x['modeId'] == self._model_id:
                    return x['id']

            logger.info('create new dialog for model {}'.format(self.model))
            _type = await self.get_type()
            response = await client.post(APIS.CREATE_DIALOG,
                                         headers=self._header,
                                         json={
                                             'dialogType': 1,
                                             'name': self.model,
                                             'type': _type,
                                             'ttsLanguageTypeId': 0,
                                             'ttsType': 0,
                                             'modeId': self._model_id,
                                             'contextId': '',
                                         })
            response.raise_for_status()
            return int(response.json()['data'])

    async def get_model_id(self) -> int:
        return self._model_id

    async def get_type(self) -> int:
        return 10

    async def _process_sse_line(self, line: str) -> typing.Optional[dict]:
        """Process a single SSE line and return parsed JSON if valid."""
        if not line.strip():
            return None
            
        if line.startswith('data:'):
            data = line[5:].strip()  # Remove 'data:' prefix
            if data == '[DONE]':
                return None
            try:
                return json.loads(data)
            except json.JSONDecodeError:
                logger.error(f"Failed to parse JSON: {data}")
                return None
        return None

    async def chat(
        self,
        query: str,
        show_stream: bool = False,
    ):
        await self._ensure_initialized()
        dialog_id = await self.get_dialog_id()
        model_id = await self.get_model_id()
        
        request_id = str(uuid4())
        payload = {
            "prompt": query,
            "requestId": request_id,
            "modeId": model_id,
            "contextId": "",
            "dialogId": dialog_id,
            "languageTypeId": 0,
            "fileUuid": "",
            "tools": [
                # {
                #     "name": "Browsing",
                #     "id": "BROWSING"
                # }
            ]
        }

        async with httpx.AsyncClient() as client:
            async with client.stream('POST', APIS.CHAT, json=payload, headers=self._header) as response:
                text = ''
                async for line in response.aiter_lines():
                    data = await self._process_sse_line(line)
                    if not data:
                        continue
                        
                    content = data.get('data', {}).get('content', '')
                    if content:
                        text += content
                        if show_stream:
                            print(content, end="", flush=True)
                    if data.get('code') != 200:
                        logger.info(data)
                        break
                
                return text

    async def stream_chat(
        self,
        query: str,
    ):
        await self._ensure_initialized()
        dialog_id = await self.get_dialog_id()
        model_id = await self.get_model_id()
        
        request_id = str(uuid4())
        payload = {
            "prompt": query,
            "requestId": request_id,
            "modeId": model_id,
            "contextId": "",
            "dialogId": dialog_id,
            "languageTypeId": 0,
            "fileUuid": "",
            "tools": [
                # {
                #     "name": "Browsing",
                #     "id": "BROWSING"
                # }
            ]
        }

        async with httpx.AsyncClient() as client:
            async with client.stream('POST', APIS.CHAT, json=payload, headers=self._header) as response:
                async for line in response.aiter_lines():
                    data = await self._process_sse_line(line)
                    if not data:
                        continue
                        
                    content = data.get('data', {}).get('content', '')
                    if content:
                        yield content
                    if data.get('code') != 200:
                        logger.info(data)
                        break