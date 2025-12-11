from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from services.db import get_redis
from pydantic_extra_types.phone_numbers import PhoneNumber, PhoneNumberValidator
from typing import Annotated, Union

E164NumberType = Annotated[
        Union[str, PhoneNumber], PhoneNumberValidator(number_format="E164")
    ]


class AdressForm(BaseModel):
    phone: E164NumberType
    adress: str
    

app = FastAPI()

@app.get('/redis')
async def get_redis_data(
    redis = Depends(get_redis)
):  
    server_info = redis.info()
    v = await server_info
    db_info = redis.info('keyspace')
    k = await db_info
    return {
        'Версия Redis' : v['redis_version'],
        'Количество ключей в db0': k.get('db0', {}).get('keys', 0) 
    }

@app.get('/adress', response_model=AdressForm)
async def get_adress(
    phone: E164NumberType,
    redis = Depends(get_redis)
):      
    adress = await redis.get(phone)
    
    if not adress:
        raise HTTPException(404, detail=f'phone: {phone} not found')
    return {'phone': phone, 'adress': adress}


@app.post('/adress', response_model=AdressForm)
async def post_address(
    q: AdressForm,
    redis = Depends(get_redis)
):
    if await redis.exists(q.phone):
        raise HTTPException(409, detail=f'phone: {q.phone} already in db')
    
    await redis.set(q.phone, q.adress)
    return {'adress': q.adress, 'phone': q.phone}
 
 
@app.patch('/adress', response_model=AdressForm)
async def update_adress(
    q: AdressForm,
    redis = Depends(get_redis)
): 
    if await redis.exists(q.phone):
        await redis.set(q.phone, q.adress) 
    else:
        raise HTTPException(404, detail=f'phone: {q.phone} not found')
    return {'adress': q.adress, 'phone': q.phone}


@app.delete('/adress', status_code=204)
async def delete_adress(
    phone: E164NumberType,
    redis = Depends(get_redis)
):  
    if not await redis.exists(phone):
        raise HTTPException(404, detail=f'phone: {phone} not found')    
    await redis.delete(phone)
    
    return {'phone': phone}