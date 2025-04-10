from fastapi import APIRouter
from . import playlist,user  # Import the user module (using relative import)

router = APIRouter()  # Create a router instance

@router.get("/")
async def root():
    return {"message": "Hello World"}
    

# router.include_router(playlist.router) 
router.include_router(user.router) 