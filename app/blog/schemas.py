from pydantic import BaseModel

class SendPost(BaseModel):
    id: int
    title: str
    content: str
    images: list[str]

class CreatePost(BaseModel):
    title: str
    content: str
    user_id: int
