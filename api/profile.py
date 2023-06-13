from fastapi import APIRouter, Depends, HTTPException, Header
from api.auth import verify_token
from pydantic import BaseModel
import mysql.connector

from api.config import DATABASE_CONFIG

router = APIRouter()


class UpdateProfileRequest(BaseModel):
    full_name: str
    username: str
    new_email: str
    phone_number: str


def get_db_connection():
    return mysql.connector.connect(**DATABASE_CONFIG)


@router.put("/update-profile")
def update_profile(
    request: UpdateProfileRequest,
    authorization: str = Header(None),
    token: dict = Depends(verify_token)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    # Access token is available as `token` variable
    access_token = authorization.split(" ")[1]
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s", (token.get("sub"),))
    existing_profile = cursor.fetchone()
    if existing_profile:
        update_query = "UPDATE users SET full_name = %s, username = %s, email = %s, phone_number = %s WHERE email = %s"
        cursor.execute(
            update_query,
            (
                request.full_name,
                request.username,
                request.new_email,
                request.phone_number,
                token.get("sub"),
            ),
        )

        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "Profile updated successfully"}

    cursor.close()
    connection.close()
    raise HTTPException(status_code=401, detail="User not found")
