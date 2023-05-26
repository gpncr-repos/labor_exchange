import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr, Field
from decimal import Decimal

class CreateJobRequest(BaseModel):
    title: str = Field(..., description='Название вакансии')
    description: str = Field(..., description='Описание вакансии')
    salary_from: Decimal = Field(..., description='Зарплата от', gt=0)
    salary_to: Decimal = Field(..., description='Зарплата до', gt=0)
    is_active: bool = Field(False, description='Активна ли вакансия')

    class Config:
        orm_mode = True


class CreateJobResponse(BaseModel):
    id: int = Field(..., description='Идентификатор вакансии')
    info: str = Field(..., description='Информация')
    class Config:
        orm_mode = True

class DeleteJobResponse(BaseModel):
    id: int = Field(..., description='Идентификатор вакансии')
    info: str = Field(..., description='Информация')
    class Config:
        orm_mode = True

class UpdateJobResponse(BaseModel):
    id: int = Field(..., description='Идентификатор вакансии')
    info: str = Field(..., description='Информация')
    class Config:
        orm_mode = True

class GetJobResponse(BaseModel):
    id: int = Field(..., description='Идентификатор вакансии')
    title: str = Field(..., description='Название вакансии')
    description: str = Field(..., description='Описание вакансии')
    salary_from: Decimal = Field(..., description='Зарплата от', gt=0)
    salary_to: Decimal = Field(..., description='Зарплата до', gt=0)
    is_active: bool = Field(..., description='Активна ли вакансия')
    created_at: datetime.datetime = Field(..., description='Дата создания. ISO8601')

    class Config:
        orm_mode = True


class CreateResponseRequest(BaseModel):
    message: str = Field(..., description='Сопроводительное письмо')

    class Config:
        orm_mode = True


class GetResponseUserResponse(BaseModel):
    email:str = Field(..., description='Email')
    name:str = Field(..., description='Имя пользователя')

class GetResponseResponse(BaseModel):
    message: str = Field(..., description='Сопроводительное письмо')
    user: GetResponseUserResponse = Field(..., description='Пользователь')

    class Config:
        orm_mode = True

class CreateResponseResponse(BaseModel):
    id: int = Field(..., description='Идентификатор вакансии')
    info: str = Field(..., description='Информация')
    class Config:
        orm_mode = True