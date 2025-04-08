from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/playlists")


@router.get("/")
async def get_playlist():
    return {
        
    }

@router.get('/{playlist_id}')
async def get_playlist(playlist_id):
    return {}

@router.post('/add')
async def add_playlist(data):
    if not data:
        raise HTTPException(status_code=400, detail="Bad Request: Invalid input.")
    
    
    