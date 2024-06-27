from models import *
from fastapi import APIRouter, HTTPException
from db import *
from typing import List
from werkzeug.security import generate_password_hash

app = APIRouter()


@app.get("/users/", response_model=List[UserOut])
async def read_users(skip: int = 0, limit: int = 10):
    query = users.select().offset(skip).limit(limit)
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=UserOut)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
    

@app.post("/users/", response_model=UserOut)
async def create_user(user: UserCreate):
    password = generate_password_hash(user.password)
    query = users.insert().values(username=user.username, surname=user.surname, email=user.email, password=password)
    user_id = await database.execute(query)
    return {**user.dict(), "id": user_id}


@app.put("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: int, user: UserCreate):
    password = generate_password_hash(new_user.password)
    query = users.update().where(users.c.id == user_id).values(username=user.username, surname=user.surname, email=user.email,
                                                               password=password)
    await database.execute(query)
    return {**user.dict(), "id": user_id}


@app.delete("/users/{user_id}", response_model=UserOut)
async def delete_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    user = await database.fetch_one(query)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    delete_query = users.delete().where(users.c.id == user_id)
    await database.execute(delete_query)
    return {"message": f"user id={user_id} deleted"}




@app.get("/excursions/", response_model=List[excursionOut])
async def read_excursions(skip: int = 0, limit: int = 10):
    query = excursions.select().offset(skip).limit(limit)
    return await database.fetch_all(query)


@app.get("/excursions/{excursion_id}", response_model=excursionOut)
async def read_excursion(excursion_id: int):
    query = excursions.select().where(excursions.c.id == excursion_id)
    excursion = await database.fetch_one(query)
    if excursion is None:
        raise HTTPException(status_code=404, detail="excursion not found")
    return excursion
    

@app.post("/excursions/", response_model=excursionOut)
async def create_excursion(excursion: excursionCreate):
    query = excursions.insert().values(name=excursion.name, description=excursion.description, price=excursion.price)
    excursion_id = await database.execute(query)
    return {**excursion.dict(), "id": excursion_id}


@app.put("/excursions/{excursion_id}", response_model=excursionOut)
async def update_excursion(excursion_id: int, excursion: excursionCreate):
    query = excursions.update().where(excursions.c.id == excursion_id).values(name=excursion.name,
                                                                        description=excursion.description,
                                                                        price=excursion.price)
    await database.execute(query)
    return {**excursion.dict(), "id": excursion_id}


@app.delete("/excursions/{excursion_id}", response_model=excursionOut)
async def delete_excursion(excursion_id: int):
    query = excursions.select().where(excursions.c.id == excursion_id)
    excursion = await database.fetch_one(query)
    if excursion is None:
        raise HTTPException(status_code=404, detail="excursion not found")
    delete_query = excursions.delete().where(excursions.c.id == excursion_id)
    await database.execute(delete_query)
    return excursion




@app.get("/orders/", response_model=List[OrderOut])
async def read_orders(skip: int = 0, limit: int = 10):
    query = orders.select().offset(skip).limit(limit)
    return await database.fetch_all(query)


@app.get("/orders/{order_id}", response_model=OrderOut)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    order = await database.fetch_one(query)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
    

@app.post("/orders/", response_model=OrderOut)
async def create_order(order: OrderCreate):
    query = orders.insert().values(
        user_id=order.user_id,
        excursion_id=order.excursion_id,
        order_date=datetime.now(),  
        status="Booking"  
    )
    order_id = await database.execute(query)
    return {**order.dict(), "id": order_id, "order_date": datetime.now(), "status": "Booking"}


@app.put("/orders/{order_id}", response_model=OrderOut)
async def update_order(order_id: int, order: OrderCreate):
    query = orders.update().where(orders.c.id == order_id).values(
        user_id=order.user_id,
        excursion_id=order.excursion_id,
        order_date=datetime.now(),  
        status=order.status  
    )
    await database.execute(query)
    updated_order = await database.fetch_one(orders.select().where(orders.c.id == order_id))
    return updated_order


@app.delete("/orders/{order_id}", response_model=OrderOut)
async def delete_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    order = await database.fetch_one(query)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    delete_query = orders.delete().where(orders.c.id == order_id)
    await database.execute(delete_query)
    return order