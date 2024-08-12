responses = {
    204: {"description": "Zero rezult"},
    403: {"description": "You have not power here"},
    422: {"description": "Some proplem with validation"},
}

responses_get_user = {
    **responses,
    200: {
        "description": "Get user",
        "content": {
            "application/json": {
                "example": {
                    "id": 1,
                    "name": "Vasilii",
                    "email": "Alibabaevich@bandit.cement",
                    "is_company": True,
                    "created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
}

responses_post_user = {
    **responses,
    200: {
        "description": "User create",
        "content": {
            "application/json": {
                "example": {
                    "message": "User created",
                    "user name": "Vasilii",
                    "user email": "Alibabaevich@bandit.cement",
                    "created_at": "2024-08-06T20:41:48.521Z",
                }
            }
        },
    },
}

responses_update_user = {
    **responses,
    200: {
        "description": "User updated",
        "content": {
            "application/json": {
                "example": {
                    "message": "User updated",
                    "user name": "Alex",
                    "user email": "Belii@bandit.docent",
                    "user is_company": True,
                }
            }
        },
    },
}

responses_delete_user = {
    **responses,
    200: {
        "description": "User delete",
        "content": {
            "application/json": {
                "example": {
                    "message": "User delete",
                    "user name": "Djady",
                    "user email": "Obi@van.cenoby",
                }
            }
        },
    },
}
