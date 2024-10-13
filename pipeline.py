import requests
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
    os.environ.get('SUP_API_SEC')

who = {'9b0041c309fab2f2d507eed2a9051c94': 'Boaz', 'afd06dbb42d96f85c77c269f42347ca4': 'Derek', '7e74b03f1539f93cbb7d6a72016f32a8': 'Ryan'} 

@app.post("/matched")
async def register_pic(file: UploadFile):
    # Detect Face
    file_content = await file.read()

    # Prepare the data and files for the Face++ API
    files = {'image_file': (file.filename, file_content, file.content_type)}

    data = {
        'api_key': api_key,
        'api_secret': api_sec,
        'outer_id': 'FacedataX'
    }
    response = requests.post(face_search_url, data=data, files=files)
    if response.status_code == 200:
        result = response.json()
        results = result['results'][0]['face_token']

        # return {"matched_uid": str(who[str(results)])}
        name = str(who[str(results)])
        print(name)
        response = supabase.table("Profiles").select("*").execute()
        print(response)
        return response

    else:
        print("Error")
        print(response.text)
