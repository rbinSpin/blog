import sys
sys.path.append("..")

from fastapi.templating import Jinja2Templates
from pymongo import DESCENDING
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status


from models import article, articleRequest
from database import get_collection
from pymongo.collection import Collection

router = APIRouter(
    prefix="/article",
    tags=["article"],
    responses={404: {"description": "Not found"}}
)

templates = Jinja2Templates(directory="templates")


# creat article
@router.post("/creat_article", status_code=status.HTTP_201_CREATED)
async def write_article(article_request: articleRequest,
                        collection: Collection = Depends(get_collection)):
    article_model = article_request.model_dump()
    collection.insert_one(arrange_article_id(article_model))


    def arrange_article_id(article: article):
        result = collection.find_one({}, sort=[("id", DESCENDING)])
        article['id'] = 1 if collection.count_documents({}) == 0 else result['id'] + 1
        return article

# edit article(update)
@router.put("/edit_article/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def edit_article(article_request: articleRequest,
                       article_id: int = Path(gt=0),
                       collection: Collection = Depends(get_collection)):
    target_found = collection.find_one({"id": article_id})
    if not target_found:
        raise HTTPException(status_code=404, detail='Item not found')
    update_data = {"$set": {"title": article_request.title,"content": article_request.content}}
    collection.update_one({"id": article_id}, update_data)

# delete article
@router.delete("/delete_article/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(article_request: articleRequest,
                       article_id: int = Path(gt=0),
                       collection: Collection = Depends(get_collection)):
    target_found = collection.find_one({"id": article_id})
    if not target_found:
        raise HTTPException(status_code=404, detail='Item not found')
    collection.delete_one({"id": article_id})