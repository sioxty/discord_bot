from fastapi import APIRouter, HTTPException,status
from ..database import User_data


router = APIRouter(prefix="/users/{user_id}/playlists")


@router.get("/")
async def get_playlists(user_id:int,):
    return {
        'user_id':user_id,
        
    }

@router.get('/{playlist_id}')
async def get_playlist(playlist_id):
    return {}

@router.post('/add')
async def add_playlist(data):
    if not data:
        raise HTTPException(status_code=400, detail="Bad Request: Invalid input.")
    return status.HTTP_201_CREATED

@router.get('/favorite_tracks')
async def get_favorite_tracks(user_id:int):
    user = User_data(user_id)
    return await user.get_favorite_tracks()
