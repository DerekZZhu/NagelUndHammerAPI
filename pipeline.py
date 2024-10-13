import requests
import base64
from fastapi import FastAPI, UploadFile, WebSocket, WebSocketDisconnect, Form
from supabase import create_client, Client
import os

api_key = os.environ.get('API_KEY')
api_sec = os.environ.get('API_SEC')

face_search_url = "https://api-us.faceplusplus.com/facepp/v3/search"
detect_face_url = "https://api-us.faceplusplus.com/facepp/v3/detect"

app = FastAPI()
supabase: Client = create_client(
    os.environ.get('SUP_API_KEY'), 
    os.environ.get('SUP_API_SEC'))

who = {'9b0041c309fab2f2d507eed2a9051c94': 'Boaz', 'afd06dbb42d96f85c77c269f42347ca4': 'Derek', '7e74b03f1539f93cbb7d6a72016f32a8': 'Ryan'} 

@app.post("/matched")
async def register_pic(data: dict):
    image_bytes = bytes(data['image_array'])
    encoded_image = base64.b64encode(image_bytes).decode('utf-8')

    data = {
        'api_key': api_key,
        'api_secret': api_sec,
        'outer_id': 'FacedataX',
        'image_base64': encoded_image
    }
    
    response = requests.post(face_search_url, data=data)
    if response.status_code == 200:
        result = response.json()
        results = result['results'][0]['face_token']

        # return {"matched_uid": str(who[str(results)])}
        name = str(who[str(results)])
        print(name)
        response = supabase.table("Profiles").select("*").eq("username", name).execute()
        print(response)
        return response

    else:
        print("Error")
        print(response.text)

@app.get("/album")
async def album(username: str):
    try:
        response = supabase.storage.from_(username).list()
        return {"files": response}
    except Exception as e:
        return {"error": str(e)}
