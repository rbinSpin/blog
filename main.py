from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette import status
from models import article
from routers import article, web_page

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(article.router)
app.include_router(web_page.router)

# redirect to /web_page
@app.get("/", response_class=HTMLResponse)
async def return_to_index():
    return RedirectResponse(url="/web_page", status_code=status.HTTP_302_FOUND)

