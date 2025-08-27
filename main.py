from fastapi import FastAPI
from routers import users#, home
from db.models import Base,engine
from utils.auth import SECRET_KEY
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
import sqladmin
import shutil
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

app = FastAPI()


app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="session_cookie",
    max_age=1800000000000  # 30 minutes in seconds
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#app.add_middleware(HTTPSRedirectMiddleware)


static_path = Path("static")
static_path.mkdir(exist_ok=True)

# Path to sqladmin's statics directory
sqladmin_static_path = os.path.join(os.path.dirname(sqladmin.__file__), "statics")

# Copy files from sqladmin/statics to your static/ dir
for item in os.listdir(sqladmin_static_path):
    src = os.path.join(sqladmin_static_path, item)
    dest = os.path.join(static_path, item)
    if os.path.isdir(src):
        shutil.copytree(src, dest, dirs_exist_ok=True)
    else:
        shutil.copy2(src, dest)

# Mount your static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

media_path = Path("media")
media_path.mkdir(exist_ok=True)
app.mount("/media", StaticFiles(directory="media"), name="media")


# Tables are now managed by Alembic migrations
# Use: alembic upgrade head to create/update database schema
# Base.metadata.create_all(bind=engine)

#app.include_router(home.router)
app.include_router(users.router)

from sqladmin import Admin
from db.admin import UserAdmin #, ProfileAdmin

admin = Admin(app, engine)

# Register admin models
admin.add_view(UserAdmin)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)