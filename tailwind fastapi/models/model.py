from pydantic import BaseModel, ConfigDict


    
class User(BaseModel):
    id: int
    username: str
    password: str


class Tag (BaseModel):
    id: int
    name:str
    model_config = ConfigDict(from_attributes=True)
    
class Entry(BaseModel):
    id: int
    date: str
    tittle : str
    content: str
    userId: int
    tags: list[Tag]
    model_config = ConfigDict(from_attributes=True)
    