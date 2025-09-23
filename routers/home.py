from fastapi import APIRouter, Depends
from pymongo import MongoClient
from dotenv import load_dotenv
from db.models import User
from utils.auth import get_current_user
import os

load_dotenv()

router= APIRouter(prefix="")

mongo_url= os.getenv("MONGO_URL")
mongo_client = MongoClient(mongo_url)


@router.get("/dashboard")
async def user_data_dashboard(current_user: User = Depends(get_current_user)):
    if not current_user.is_verified:
        return "Verify your account to access the dashboard"
    my_platform_id= current_user.platform_id
    print(my_platform_id)
    return "XYZ"