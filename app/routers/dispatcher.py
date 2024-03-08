from fastapi import Request
from controllers.user_controller import UserController

async def get_controller(request: Request):
    # default controller for further evolution in app code we can use request to determine the controller 
    return UserController()