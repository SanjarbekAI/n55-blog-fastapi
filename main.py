from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.routers import users, posts

app = FastAPI()

app.include_router(router=users.router)
app.include_router(router=posts.router)


@app.get('/', include_in_schema=False)
async def root():
    return RedirectResponse('docs/')
