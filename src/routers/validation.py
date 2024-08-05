from fastapi.responses import JSONResponse


class Validation_for_routers:
    @staticmethod
    def empty_base(router_name: str):
        return JSONResponse(
            status_code=422,
            content={"message": "{router} is empty".format(router=router_name)},
        )

    @staticmethod
    def element_not_found(router_name: str):
        return JSONResponse(
            status_code=422,
            content={"message": "{router} not found in database".format(router=router_name)},
        )

    @staticmethod
    def element_not_current_user_for(router_name: str, action_name: str):
        return JSONResponse(
            status_code=422,
            content={
                "message": "it is not your {router} to {action}".format(
                    router=router_name, action=action_name
                )
            },
        )

    @staticmethod
    def job_is_not_active():
        return JSONResponse(status_code=422, content={"message": "Job is not active"})
