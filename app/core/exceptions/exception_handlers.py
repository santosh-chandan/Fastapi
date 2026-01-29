from app.user.services import UserNotFound, UserAlreadyExist
from fastapi import Request
from fastapi.responses import JSONResponse

# handler accept params that aren’t used
    # This is required by FastAPI’s handler signature
    # FastAPI calls handlers like this internally: - handler(request, exception)
def user_not_found_handler(req: Request, exc: UserNotFound):
    return JSONResponse(
        status_code=404,
        content={"details": str(exc)}
    )

def user_already_exist(req: Request, exc: UserAlreadyExist):
    return JSONResponse(
        status_code=303,
        content={"details": str(exc)}
    )
