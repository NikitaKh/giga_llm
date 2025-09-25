from fastapi import APIRouter, Form, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from app.services.gigachat import generate_response_with_system_prompt
from app.settings import settings
from app.routers import get_current_user, User

router = APIRouter(prefix='/gigachat', tags=['gigachat'])


@router.post("/question")
async def analysis_logs(question: str =  Form(...), current_user: User = Depends(get_current_user)) -> JSONResponse:
    if current_user.get('role', None) != 'admin':
        raise HTTPException(status.HTTP_403_FORBIDDEN, 'Insufficient privileges')
    response = generate_response_with_system_prompt(
        user_message=question,
        system_prompt=settings.logs_prompt_template,
    )
    return JSONResponse(content={"message": response})
