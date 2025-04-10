
from fastapi import APIRouter, HTTPException
from ..Types import UserModel
from ..database import UserRepository


router = APIRouter(prefix="/users")

users = []

@router.get('')
async def get_users():
    return {
        'count':len(users),
        'users':users
    }
    

@router.get("/")
async def get_user(user_id:int,):
    responce = search_id(user_id) 
    if responce:
        return responce
    raise HTTPException(status_code=404, detail="User not found")
    

@router.post('/')
async def add_user(user: UserModel):
    repo = UserRepository(user.user_id)
    await repo.add_user()
    return user

def search_id(_id:int):
    for user in users:
        if user.user_id == _id:
            return user