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
                    "message": "Job get",
                    "Job id": 1,
                    "Job Title": "President",
                    "Job discription": "Sir",
                    "Job salary from": 100000,
                    "Job salary to": 200000,
                    "Job active": True,
                    "Job created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
}

responses_post_jobs = {
    **responses,
    200: {
        "description": "job create",
        "content": {
            "application/json": {
                "example": {
                    "message": "Job create",
                    "Job id": 1,
                    "Job Title": "President",
                    "Job discription": "Sir",
                    "Job salary from": 100000,
                    "Job salary to": 200000,
                    "Job created_at": "2024-08-06T20:41:48.521Z",
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
                    "message": "Job update",
                    "Job id": 1,
                    "Job Title": "President",
                    "Job discription": "Sir",
                    "Job salary from": 100000,
                    "Job salary to": 200000,
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
                    "message": "Job delete",
                    "Job id": 1,
                    "Job Title": "President",
                    "Job discription": "Sir",
                    "Job salary from": 100000,
                    "Job salary to": 200000,
                }
            }
        },
    },
}
