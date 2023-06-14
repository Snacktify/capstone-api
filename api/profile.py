from fastapi import APIRouter, Depends, HTTPException, Cookie
from api.auth import decode_access_token, verify_token
from pydantic import BaseModel
import mysql.connector

from api.config import USER_CONFIG

router = APIRouter()

class UpdateProfileRequest(BaseModel):
    full_name: str
    username: str
    new_email: str
    phone_number: str


def get_db_connection():
    return mysql.connector.connect(**USER_CONFIG)


async def get_current_user(access_token: str = Cookie(None)):
    if not access_token:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

    decoded_token = decode_access_token(access_token)
    return decoded_token


@router.put("/update-profile")
def update_profile(
    request: UpdateProfileRequest,
    current_user: dict = Depends(get_current_user),
):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s", (current_user.get("sub"),))
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
                current_user.get("sub"),
            ),
        )

        connection.commit()
        cursor.close()
        connection.close()
        return {"message": "Profile updated successfully"}

    cursor.close()
    connection.close()
    raise HTTPException(status_code=401, detail="User not found")
