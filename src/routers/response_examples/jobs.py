responses = {
    204: {"description": "Zero rezult"},
    403: {"description": "You have not power here"},
    422: {"description": "Some proplem with validation"},
}
responses_get_jobs = {
    **responses,
    200: {
        "description": "Get job",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "user_id": 1,
                    "title": "President",
                    "discription": "Sir",
                    "salary_from": 100000,
                    "salary_to": 200000,
                    "is_active": True,
                    "created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
}

responses_post_jobs = {
    **responses,
    201: {
        "description": "job create",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "user_id": 1,
                    "title": "President",
                    "discription": "Sir",
                    "salary_from": 100000,
                    "salary_to": 200000,
                    "is_active": True,
                    "created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
    200: {
        "description": "job create",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "user_id": 1,
                    "title": "President",
                    "discription": "Sir",
                    "salary_from": 100000,
                    "salary_to": 200000,
                    "is_active": True,
                    "created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
}

responses_update_jobs = {
    **responses,
    200: {
        "description": "job updated",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "user_id": 1,
                    "title": "President",
                    "discription": "Sir",
                    "salary_from": 100000,
                    "salary_to": 200000,
                    "is_active": True,
                    "created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
}
responses_delete_jobs = {
    **responses,
    200: {
        "description": "job delete",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "user_id": 1,
                    "title": "President",
                    "discription": "Sir",
                    "salary_from": 100000,
                    "salary_to": 200000,
                    "is_active": True,
                    "created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
}
