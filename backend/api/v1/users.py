from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.config import settings
from db.session import get_db
from schemas.user import UserResponse
from api.dependencies import get_current_user
import uuid
from models.user import User

router = APIRouter()


@router.get("/users/me", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_current_user_info(db: Session = Depends(get_db)):
    """
    Get the current logged-in user's information.
    """
    # Assuming you have a function to get the current user from the request
    current_user = get_current_user()
    return current_user


@router.get(
    "/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
async def get_user_by_id(user_id: uuid, db: Session = Depends(get_db)):
    """
    Get user information by user ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    return user


@router.get("/users", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_users(db: Session = Depends(get_db)):
    """
    Get a list of all users.
    """
    users = db.query(User).all()
    return users


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: uuid, db: Session = Depends(get_db)):
    """
    Delete a user by user ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )
    db.delete(user)
    db.commit()
    return None


@router.put(
    "/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK
)
async def update_user(
    user_id: uuid, user_update: UserResponse, db: Session = Depends(get_db)
):
    """
    Update a user's information by user ID.
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    # Update user fields
    user.full_name = user_update.full_name
    user.email = user_update.email
    user.phone = user_update.phone
    user.address = user_update.address
    

    db.commit()
    db.refresh(user)
    return user
