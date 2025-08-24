from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.services.gigachat import generate_response_with_system_prompt
from app.settings import settings

router = APIRouter(prefix='/gigachat', tags=['gigachat'])


@router.post("/question")
async def analysis_logs(request: Request) -> JSONResponse:
    body = await request.body()
    response = generate_response_with_system_prompt(
        user_message=body,
        system_prompt=settings.logs_prompt_template,
    )
    return JSONResponse(content={"message": response})
