responses = {
    204: {"description": "Zero rezult"},
    403: {"description": "You have not power here"},
    422: {"description": "Some proplem with validation"},
}
responses_get_responses = {
    **responses,
    200: {
        "description": "Get response\\es",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "user_id": 1,
                    "job_id": 1,
                    "message": "dreem work",
                    "created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
}

responses_post_responses = {
    **responses,
    201: {
        "description": "response create",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "user_id": 1,
                    "job_id": 1,
                    "message": "dreem work",
                    "created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
    200: {
        "description": "response create",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "user_id": 1,
                    "job_id": 1,
                    "message": "dreem work",
                    "created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
}

responses_update_responses = {
    **responses,
    200: {
        "description": "response updated",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "user_id": 1,
                    "job_id": 1,
                    "message": "dreem work",
                    "created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
}
responses_delete_responses = {
    **responses,
    200: {
        "description": "response delete",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "user_id": 1,
                    "job_id": 1,
                    "message": "dreem work",
                    "created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
}
