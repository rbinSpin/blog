from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette import status
from models import article
from routers import article, web_page

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return RedirectResponse(url="/web_page", status_code=status.HTTP_302_FOUND)

app.include_router(article.router)
app.include_router(web_page.router)

