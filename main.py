from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Path, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from starlette.staticfiles import StaticFiles
from starlette import status

# 載入 pymongo 套件
from pymongo import DESCENDING, MongoClient
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

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# return index.html
@app.get("/read_all_article", response_class=HTMLResponse)
async def read_all_article(request: Request, collection: Collection = Depends(get_collection)):
    # 查询所有文档
    all_documents = collection.find()
    return templates.TemplateResponse("index.html", {"request": request, "all_doc": all_documents})

# creat article
@app.post("/creat_article", status_code=status.HTTP_201_CREATED)
async def write_article(article_request: articleRequest,
                        collection: Collection = Depends(get_collection)):
    article_model = article_request.model_dump()
    collection.insert_one(arrange_article_id(article_model))


    def arrange_article_id(article: article):
        result = collection.find_one({}, sort=[("id", DESCENDING)])
        article['id'] = 1 if collection.count_documents({}) == 0 else result['id'] + 1
        return article

# edit article(update)
@app.put("/edit_article/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def edit_article(article_request: articleRequest,
                       article_id: int = Path(gt=0),
                       collection: Collection = Depends(get_collection)):
    target_found = collection.find_one({"id": article_id})
    if not target_found:
        raise HTTPException(status_code=404, detail='Item not found')
    update_data = {"$set": {"title": article_request.title,"content": article_request.content}}
    collection.update_one({"id": article_id}, update_data)

# delete article
@app.delete("/delete_article/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(article_request: articleRequest,
                       article_id: int = Path(gt=0),
                       collection: Collection = Depends(get_collection)):
    target_found = collection.find_one({"id": article_id})
    if not target_found:
        raise HTTPException(status_code=404, detail='Item not found')
    collection.delete_one({"id": article_id})

## html page
# index.html
@app.get("/", response_class=HTMLResponse)
async def index(request: Request, collection: Collection = Depends(get_collection)):
    # 查询所有文档
    all_documents = collection.find()
    return templates.TemplateResponse("index.html", {"request": request, "all_doc": all_documents})

# article.html
@app.get("/article/", response_class=HTMLResponse)
async def LaTeX(request: Request):
    return templates.TemplateResponse("LaTeX.html", {"request": request})

@app.get("/article/{article_id}", response_class=HTMLResponse)
async def get_article(request: Request,
                      article_id: int = Path(gt=0),
                      collection: Collection = Depends(get_collection)):
    
    article = collection.find_one({"id": article_id})
    if not article:
        raise HTTPException(status_code=404, detail='Item not found')
    return templates.TemplateResponse("article.html", 
                                      {"request": request, "article": article})