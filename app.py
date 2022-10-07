import os
from supabase import create_client, Client

from flask import Flask, request

app = Flask(__name__)
SUPABASE_PROJECT_URL: str = os.getenv('SUPABASE_PROJECT_URL')
SUPABASE_API_KEY: str = os.getenv('SUPABASE_API_KEY')
supabase: Client = create_client(SUPABASE_PROJECT_URL, SUPABASE_API_KEY)
@app.route('/')
def default():
    return "Hello World"

@app.route('/supabase/login', methods=['POST'])
def login():
    data = request.json
    print(data['email'])
    user = supabase.auth.sign_in(email=data['email'], password=data['password'])
    print(user)
    return "logged in"

@app.route('/supabase/insert')
def insert():
    data = supabase.table("building_dimensions").insert({"length":20, "width": 30}).execute()
    print(data.data)
    return data.data

@app.route('/supabase/select')
def select():
    data = supabase.table("building_dimensions").select("*").eq("id","73145d5a-78ef-4b5e-9809-a7041f62df1d").execute()
    print(data.data)
    return data.data

@app.route('/supabase/update')
def update():
    return "Supabase UPDATE"

@app.route('/supabase/delete')
def delete():
    return "Supabase DELETE"

@app.route('/supabase/calculate-area/<buildingId>')
def calculateArea(buildingId):
    data = request.json
    user = supabase.auth.api.get_user(jwt=data['token'])
    if not user: 
        return 'You needed to be logged in'
    fetchedData = supabase.table("building_dimensions").select("*").eq("id", buildingId).execute()
    buildingData = fetchedData.data[0]
    print(buildingData)
    area = buildingData['length'] * buildingData['width']
    areaData = {
        "area": area,
        "building": buildingData['id']
    }
    insertedAreaData = supabase.table("building_areas").insert(areaData).execute()
    return insertedAreaData.data
    

if __name__ == '__main__':
    app.run(debug=True)