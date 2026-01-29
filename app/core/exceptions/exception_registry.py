# app/core/exception_registry.py
from fastapi import FastAPI
from app.core.exceptions.exceptions import UserNotFound, UserAlreadyExist
from app.core.exceptions.exception_handlers import (
    user_not_found_handler,
    user_already_exist,
)

# call it in main.py and pass app as reference then it would register all exceptions thene.
def register_exception_handlers(app: FastAPI):
    app.add_exception_handler(UserNotFound, user_not_found_handler)
    app.add_exception_handler(UserAlreadyExist, user_already_exist)
