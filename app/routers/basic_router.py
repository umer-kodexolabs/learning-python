from fastapi import (
    APIRouter,
    Header,
    HTTPException,
    status,
    Response,
    Request,
    Cookie,
    Form,
    UploadFile,
    File,
)
from pydantic import BaseModel, EmailStr
from typing import Annotated
from app.utils import success_response, error_response
import os

router = APIRouter(prefix="/basic", tags=["basic"])


class UserFormData(BaseModel):
    username: str
    email: EmailStr
    password: str


UPLOAD_DIR = "files"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Create the directory if it doesn't exist


@router.post("/upload_file")
async def upload_file(file: Annotated[UploadFile, File()]):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    print("file_location", file_location)
    with open(file_location, "wb") as f:
        content = await file.read()
        f.write(content)

    return success_response(
        status_code=status.HTTP_200_OK,
        data=file.filename,
        message="File uploaded successfully",
    )


@router.post("/form_data")
def post_form_data(payload: Annotated[UserFormData, Form()]):
    return {"payload": payload}


@router.get("/bearer_token")
def get_bearer_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header",
        )

    token = authorization.split("Bearer ")[1]

    return {"token": token}


@router.get("/set_cookie")
def set_cookie_and_headers(response: Response):
    response.set_cookie(
        key="my_cookie", value="cookie_value", httponly=True, max_age=3600
    )
    response.headers["X-Custom-Header"] = "CustomValue"
    response.headers["X-App-Version"] = "1.0.0"

    return {"message": "Cookies and headers set successfully"}


@router.get("/get_cookie")
def get_cookie_and_headers(
    my_cookie: str = Cookie(default=None),
    x_custom_header: str = Header(default=None),
    x_app_version: str = Header(default=None),
    Authorization: str = Header(default=None),
):
    return {
        "cookie": my_cookie,
        "x_custom_header": x_custom_header,
        "x_app_version": x_app_version,
        "auth": Authorization,
    }


@router.get("/test")
def test_query(
    req: Request,
    limit: int = None,
    page: int = None,
    is_new: bool = False,
):
    p = {limit, page}
    print("Python", type(p))
    try:
        json_body = req.json()
        print("req", req)
        print("page", page)
        print("is_new", is_new)
        ab = {"limit": type(limit), "page": type(page), "is_new": type(is_new)}

        obj = {limit, page, is_new}

        print("Query params1...", (ab))
        if limit is not None:
            print(f"We have limit: {limit}")

        if page is not None:
            print(f"We have page: {page}")

        # data = {page, limit}
        data = {
            "page": page,
            "limit": limit,
            "method": req.method,
            "url": str(req.url),
            "headers": dict(req.headers),
            "query_params": dict(req.query_params),
            "client": req.client.host if req.client else None,
        }

        response = success_response(
            status_code=status.HTTP_200_OK, data=data, message="Here is your response"
        )
        response.set_cookie(
            key="token",
            value="123",
        )

        return response

    except Exception as err:
        print("Errro", err)
        return error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Internal server error",
            error=str(err),
        )
