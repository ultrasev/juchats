import pydantic
import typing

class Mode(pydantic.BaseModel):
    id: int
    type: int
    name: str
    showName: str
    maxToken: int
    searchFlag: int
    remark: typing.Optional[str]
