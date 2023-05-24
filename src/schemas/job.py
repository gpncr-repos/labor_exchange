import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, validator, constr, Field


class CreateJobRequest(BaseModel):
    title: str = Field(..., description='Название вакансии')
    description: str = Field(..., description='Описание вакансии')
    salary_from: float = Field(..., description='Зарплата от')
    salary_to: float = Field(..., description='Зарплата до')
    is_active: bool = Field(False, description='Активна ли вакансия')

    class Config:
        orm_mode = True


class CreateJobResponse(BaseModel):
    id: Optional[str] = Field(..., description='Идентификатор вакансии')
    title: str = Field(..., description='Название вакансии')
    is_active: bool = Field(..., description='Активна ли вакансия')
    created_at: datetime.datetime = Field(..., description='Дата создания')

    class Config:
        orm_mode = True


class GetJobResponse(BaseModel):
    id: Optional[str] = Field(..., description='Идентификатор вакансии')
    title: str = Field(..., description='Название вакансии')
    description: str = Field(..., description='Описание вакансии')
    salary_from: str = Field(..., description='Зарплата от')
    salary_to: str = Field(..., description='Зарплата до')
    is_active: bool = Field(..., description='Активна ли вакансия')
    created_at: datetime.datetime = Field(..., description='Дата создания')

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