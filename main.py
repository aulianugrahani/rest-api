
# import packages
from fastapi import FastAPI, HTTPException, Header ## huruf kecil semua nama package, kalau huruf gede kecilnya sesuai berarti class/kelas
from pydantic import BaseModel
import pandas as pd
post

# create FastAPI object
app = FastAPI()

# 
# password - api key
password="kopiluwakgabikinkembung"


class Profile(BaseModel):
    '''
    Profile class - used for making request body
    '''
    name: str
    location: str


@app.get('/')  # homepage, halamnan yang pertama kali dikunjungi, urlnya pasti \ aja
def getHome():
    '''
    endpoint 1 - home page
    '''

    return {
        "msg": "Hello world!"
    }


@app.get('/profiles')
def getProfiles():  ## isi semua profil yang ada di file csv
    '''
    endpoint 2 - get all profiles
    '''

    df = pd.read_csv('dataset.csv') ## baca isi data csv

    return {
        "data": df.to_dict(orient='records')  ## pakai orient records supaaya data yang ditampilkan lebih rapih
    }

# path/url parameter
@app.get('/profiles/{id}')
def getProfile(id: int):
    '''
    endpoint 3 - get profile by id     # tiap abis end point, masukkan baca data source (pd.read_)
    '''

    df = pd.read_csv('dataset.csv') ## baca isi data csv
    # filter data sesuai ID
    result = df.query(f"id == {id}")

    # ketika result kosong -> pesan eror

    if len(result) == 0:
        # tampilkan error
        raise HTTPException(status_code=404, detail="data not found!")
    # ketika result tidak kosong -> data
    return {
        "data": result.to_dict(orient='records')
    }



@app.delete('/profiles/{id}')       #methodnya pakai delete
def deleteProfile(id: int, api_key: str = Header(None)):         
    '''
    endpoint 4 - delete profile by id
    '''
    # cek password
    if (api_key == None) or api_key != password:
        #raise error
        raise HTTPException(status_code=401, detail="unauthorized access!")
    # baca isi data source
    df = pd.read_csv('dataset.csv') 
    
    #filter - exclude id yang bersangkutan
    result = df[df.id !=id]     # !-= artinya tidak sama dengan

    # replace dataset dengan yang baru 
    result.to_csv('dataset.csv', index=False)
    return {
        "data": result.to_dict(orient='records')
    }

@app.put('/profiles/{id}')
def updateProfile(id: int, profile: Profile):
    '''
    endpoint 5 - update profile by id
    '''

    # complete this endpoint
    pass


@app.post('/profiles/')
def createProfile(profile: Profile):
    '''
    endpoint 6 - create new profile
    '''
    # baca isi data source
    df = pd.read_csv('dataset.csv') 

    # buat data baru
    newDF = pd.DataFrame ({
        "id": [len(df) + 1], 
        "name": [profile.name],
        "location": [profile.location]
    })
    # pake concat, append, loc 
    # metode concat
    pd.concat([df, newDF])

    # replace dataset existing
    df.to_csv('dataset.csv', index=False)

    return {
        "msg" : "Data has created successfully"
    }
    
