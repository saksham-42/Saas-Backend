from fastapi import FastAPI, HTTPException, APIRouter
from schemas import User_response, User_create, Update_user
from typing import Optional

router = APIRouter(
    prefix = "/users",
    tags = ["users"]
)

users = {
    1 : {
        "name" : "Ryan", 
        "age" : "21", 
        "email" : "ryan@gmail.com"
    },
    2 : {
        "name" : "Marcel",
        "age" : "25",
        "email" : "mar_cel_1@gmail.com"
    }
}

@router.get("/")
def get_all_users(skip: int = 0, limit: int = 10):
    user_list = list(users.values())
    return user_list[skip : skip + limit]

@router.get("/get-user/{user_id}")
def get_user(user_id : int):
    if user_id not in users:
        raise HTTPException(status_code = 404, detail="User doesn't exist")
    return users[user_id]

@router.get("/search")
def search_users(name : str):
    results = {uid : u for uid, u in users.items()
               if name.lower() in u["name"].lower()}
    if not results:
        raise HTTPException(status_code=404, detail= " No users found")
    return results

@router.post("/add-users/{user_id}")
def add_user(user_id : int, user : User_create):
    if user_id in users:
        raise HTTPException(status_code=400, detail="User already exists")
    users[user_id] = user
    return users[user_id]
    
@router.put("/update-user/{user_id}")
def update_users(user_id : int, user : Update_user):
    if user_id not in users:
        raise HTTPException(status_code= 404, detail="User doesn't exist")
    if user.name is not None:
        users[user_id].name = user.name
    if user.age is not None:
        users[user_id].age = user.age
    if user.email is not None:
        users[user_id].email = user.email

    return users[user_id]

@router.delete("/delete-user/{user_id}")
def delete_user(user_id : int):
    if user_id not in users:
        raise HTTPException(status_code= 404, detail="The user doesn't exist")
    del users[user_id]
    return {"Success" : "User successfully deleted"}