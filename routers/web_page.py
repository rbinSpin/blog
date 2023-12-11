import sys
from fastapi.responses import HTMLResponse
sys.path.append("..")

from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, HTTPException, Path, Request
from database import get_collection
from pymongo.collection import Collection


router = APIRouter(
    prefix="/web_page",
    tags=["web_page"],
    responses={404: {"description": "Not found"}}
)

templates = Jinja2Templates(directory="templates")

# 文章列表頁面
@router.get("/", response_class=HTMLResponse)
async def index(request: Request, collection: Collection = Depends(get_collection)):
    # 查询所有文档
    all_documents = collection.find()
    return templates.TemplateResponse("index.html", {"request": request, "all_doc": all_documents})


# article.html
@router.get("/article/{article_id}", response_class=HTMLResponse)
async def get_article(request: Request,
                      article_id: int = Path(gt=0),
                      collection: Collection = Depends(get_collection)):
    
    article = collection.find_one({"id": article_id})
    if not article:
        raise HTTPException(status_code=404, detail='Item not found')
    return templates.TemplateResponse("article.html", 
                                      {"request": request, "article": article})