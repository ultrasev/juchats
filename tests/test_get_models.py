import pytest
from juchats.chat import Juchats
import os
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def juchats_client():
    token = os.getenv('JTOKEN')
    assert token is not None, "JTOKEN is not set"
    return Juchats(token)


@pytest.mark.asyncio
async def test_get_models(juchats_client):
    models = await juchats_client.get_models()

    assert models is not None, "Models should not be None"
    assert len(models) > 0, "There should be at least one model"

    for model in models:
        assert model.showName.strip(), "Model should have a non-empty showName"
        assert model.id, "Model should have a non-empty id"
        assert model.name, "Model should have a non-empty name"
        assert isinstance(model.maxToken, int), "maxToken should be an integer"
        assert isinstance(model.searchFlag,
                          int), "searchFlag should be an integer"
