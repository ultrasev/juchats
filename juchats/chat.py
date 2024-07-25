import asyncio
import json
import typing
from uuid import uuid4

import httpx
import pydantic
import websockets
from loguru import logger

from .configs import APIS, HEADERS
from .types import Mode
from .models import models

def get_headers(token: str):
    headers = HEADERS
    headers['jtoken'] = token
    return headers

class Juchats(object):
    _modes = None

    def __init__(self, token: str, model: str = "gpt-4o-2024-05-13"):
        self.token = token
        self.model = model
        self._header = get_headers(token)
        self._model_id = None
        self._dialog_id = None

    async def __aenter__(self):
        self._modes = [Mode(**x) for x in models]
        for mode in self._modes:
            if mode.name == self.model:
                self._model_id = mode.id
                break
        else:
            self.help_with_modes()
            raise ValueError(f"Model {self.model} not found")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

    def help_with_modes(self):
        print("Available modes are:")
        for mode in self._modes:
            print(f"{mode.id}: {mode.name}")

    async def modes(self) -> typing.List[Mode]:
        async with httpx.AsyncClient() as client:
            response = await client.get(APIS.MODES, headers=self._header)
            data = response.json()['data']
            modes = []
            for item in data:
                modes.extend([Mode(**x) for x in item['modes']])
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

    async def chat(
        self,
        query: str,
        show_stream: bool = False,
    ):
        dialog_id = await self.get_dialog_id()
        model_id = await self.get_model_id()
        _type = await self.get_type()
        print(f"dialog_id: {dialog_id}, model_id: {model_id}")
        async with websockets.connect(APIS.WSS.format(self.token),
                                      extra_headers=self._header) as ws:
            message = {
                "contextId": '',
                "dialogId": dialog_id,
                "event": 1,
                "fileUuid": "",
                "languageTypeId": 0,
                "modeId": model_id,
                "prompt": query,
                "requestId": str(uuid4()),
                "type": _type,
            }

            await ws.send(json.dumps(message))

            try:
                text = ''
                while True:
                    response = await ws.recv()
                    if '[DONE]' in response:
                        return text
                    js = json.loads(response)
                    content = js.get('data', {}).get('content')
                    if content:
                        text += content
                        if show_stream:
                            print(content, end="", flush=True)
                    if int(js.get('code', 200)) != 200:
                        logger.info(js)
                        return text
            except websockets.ConnectionClosed:
                logger.error("Connection closed by the server.")
            except Exception as e:
                logger.error(f"Error occurred: {e}")
