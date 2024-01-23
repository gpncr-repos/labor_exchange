from fastapi import HTTPException, status


def check_is_company(is_company: bool, message: str):
    if not is_company:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=message)


def check_is_owner(job_user_id: int, current_user_id: int, message: str):
    if job_user_id != current_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=message)
