import pytest
from juchats.chat import Juchats
import os
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def juchats_client():
    token = os.getenv('JTOKEN')
    assert token is not None, "JTOKEN is not set"
    return Juchats(token, model='deepseek-chat')


@pytest.mark.asyncio
async def test_chat(juchats_client):
    text = await juchats_client.chat("你好，请介绍一下你自己。")
    assert text is not None, "Text should not be None"

@pytest.mark.asyncio
async def test_chat_stream(juchats_client):
    query = "请用三句话介绍人工智能。"
    responses = []
    async for chunk in juchats_client.stream_chat(query):
        assert isinstance(chunk, str), "Each chunk should be a string"
        responses.append(chunk)

    full_response = ''.join(responses)

    assert len(responses) > 1, "Stream should return multiple chunks"
    assert len(full_response) > 0, "Full response should not be empty"
    assert "人工智能" in full_response, "Response should contain relevant content"
