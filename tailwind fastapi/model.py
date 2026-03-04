from pydantic import BaseModel


class Entry(BaseModel):
    id: int
    date: str
    tittle : str
    content: str
    #user_id: int
    
class User(BaseModel):
    id: int
    username: str
    password: str
    


