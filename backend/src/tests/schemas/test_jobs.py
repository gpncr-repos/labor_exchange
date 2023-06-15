import pytest
from pydantic import ValidationError

from schemas import JobInSchema


@pytest.mark.asyncio
async def test_CreateJobNegativeSalary_RaisesValidationError():
    with pytest.raises(ValidationError):
        job = JobInSchema(
            title='Отрицательная зарплата',
            description='Зарплата должна быть положительной',
            salary_from=-1000,
            salary_to=-500
        )


@pytest.mark.asyncio
async def test_CreateJobFromBiggerTo_RaisesValidationError():
    with pytest.raises(ValidationError):
        job = JobInSchema(
            title='Неправильный диапазон зарплаты',
            description='Нижняя граница больше верхней границы',
            salary_from=1000,
            salary_to=500
        )