from pydantic import BaseModel


class article:
    id: int
    title: str
    content: str
    # published_date: int

    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content

class articleRequest(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        json_schema_extra = {
            'example': {
                'id': 1,
                'title': '新文章',
                'content': '<p>Article written in HTML</p>'
            }
        }