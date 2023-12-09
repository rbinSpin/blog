from fastapi import Depends, FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from starlette.staticfiles import StaticFiles
from starlette import status

# 載入 pymongo 套件
from pymongo import MongoClient
from pymongo.collection import Collection
# MongoDB 雲端資料庫的網址
mongo_uri = "mongodb+srv://epuie:Ste410119@mycluster.lexggmc.mongodb.net/?retryWrites=true&w=majority"
# 選擇操作 article_system 資料庫
database_name = "article_system"

# Dependency to get the MongoDB database connection
def get_db():
    client = MongoClient(mongo_uri)
    db = client[database_name]
    return db

# Dependency to get the MongoDB collection
def get_collection(db: Collection = Depends(get_db)):
    collection = db["article"]
    return collection

class articleModel(BaseModel):
    title: str = Field(min_length=3)
    content: str

    class Config:
        json_schema_extra = {
            'example': {
                'title': '新文章',
                'content': '<p>Article written in HTML</p>'
            }
        }

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# return index.html
@app.get("/", response_class=HTMLResponse)
async def index(request: Request, collection: Collection = Depends(get_collection)):
    # 查询所有文档
    all_documents = collection.find()
    return templates.TemplateResponse("index.html", {"request": request, "all_doc": all_documents})

# return latex.html
@app.get("/article", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("LaTeX.html", {"request": request})

# write article
@app.post("/write_article", status_code=status.HTTP_201_CREATED)
async def write_article(request: Request, article_model: articleModel,
                        collection: Collection = Depends(get_collection)):
    article_model = article_model.model_dump()
    collection.insert_one(article_model)