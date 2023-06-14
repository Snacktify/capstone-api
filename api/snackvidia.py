from fastapi import HTTPException, APIRouter
from pydantic import BaseModel
from typing import List, Any
import mysql.connector

router = APIRouter()

# Model for data in the snack table
class snack(BaseModel):
    nama_snack: Any
    deskripsi: Any
    rating: Any
    asal_daerah: Any
    harga: Any

# Integration to MySQL databases
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="snacktify"
)
mycursor = mydb.cursor()

# Endpoint to get all snack data
@router.get("/snackvidia", response_model=List[snack])
def get_snacks():
    mycursor.execute("SELECT * FROM snack")
    result = mycursor.fetchall()
    snacks = []
    if len(result) == 0:
        return {"message": "No Snack Data"}
    for row in result:
        objekSnack = snack(nama_snack=row[0], deskripsi=row[1], rating=row[2], asal_daerah=row[3], harga=row[4])
        snacks.append(objekSnack)
    return snacks

# Endpoint to get snack data based on snack name
@router.get("/snackvidia/{nama_snack}", response_model=snack)
def get_snack(nama_snack: str):
    mycursor.execute("SELECT * FROM snack WHERE nama_snack = %s", (nama_snack,))
    result = mycursor.fetchone()
    if result:
        objekSnack = snack(nama_snack=result[0], deskripsi=result[1], rating=result[2], asal_daerah=result[3], harga=result[4])
        return objekSnack
    else:
        raise HTTPException(status_code=404, detail="Snack not found")

# Endpoint to add new snack data
@router.post("/snackvidia", response_model=snack)
def add_snack(objekSnack: snack):
    try:
        query = "INSERT INTO snack (nama_snack, deskripsi, rating, asal_daerah, harga) VALUES (%s, %s, %s, %s, %s)"
        values = (objekSnack.nama_snack, objekSnack.deskripsi, objekSnack.rating, objekSnack.asal_daerah, objekSnack.harga)
        mycursor.execute(query, values)
        mydb.commit()
        return objekSnack
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

# Endpoint to modify snack data
@router.put("/snackvidia/{nama_snack}", response_model=snack)
def update_snack(nama_snack: str, snack_data: snack):
    query = "UPDATE snack SET nama_snack = %s, deskripsi = %s, rating = %s, asal_daerah = %s, harga = %s WHERE nama_snack = %s"
    values = (snack_data.nama_snack, snack_data.deskripsi, snack_data.rating, snack_data.asal_daerah, snack_data.harga, nama_snack)
    mycursor.execute(query, values)
    if mycursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Snack not found")
    mydb.commit()
    raise HTTPException(status_code=200, detail="Snack updated")

# Endpoint to delete snack data based on snack name
@router.delete("/snackvidia/{nama_snack}")
def delete_snack(nama_snack: str):
    query = "DELETE FROM snack WHERE nama_snack = %s"
    values = (nama_snack,)
    mycursor.execute(query, values)
    if mycursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Snack not found")
    mydb.commit()
    return {"message": "Snack deleted"}
