#api/routes.py
from fastapi import APIRouter

from agent.agent import Agent
from api.schemas import ChatRequest, ChatResponse

router = APIRouter()

agent = Agent()


@router.get("/health")
def health():

    return {
        "status": "ok"
    }


@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(request: ChatRequest):

    answer = agent.run(
        request.question
    )

    return ChatResponse(
        success=True,
        answer=answer
    )