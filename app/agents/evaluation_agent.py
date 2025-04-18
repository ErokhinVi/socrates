from agents import Agent
from app.agents.tools.extract_situation import extract_situation
from app.agents.tools.extract_task import extract_task
from app.agents.tools.extract_action import extract_action
from app.agents.tools.extract_result import extract_result
from pydantic import BaseModel, Field


class HREvaluation(BaseModel):
    Situation: str = Field(
        ...,
        description="Оценка и комментарий по компоненту Situation: указывает, создаёт ли рекрутер контекст ситуации"
    )
    Task: str = Field(
        ...,
        description="Оценка и комментарий по компоненту Task: уточняет ли рекрутер конкретную задачу кандидата"
    )
    Action: str = Field(
        ...,
        description="Оценка и комментарий по компоненту Action: стимулирует ли рекрутер кандидата описать свои действия"
    )
    Result: str = Field(
        ...,
        description="Оценка и комментарий по компоненту Result: затрагивает ли рекрутер результаты и выводы кандидата"
    )


def create_evaluation_agent(system_prompt: str) -> Agent:
    return Agent(
        name="Evaluation Agent",
        handoff_description="Оценка сообщений с использованием метода STAR.",
        instructions=system_prompt,
        tools=[extract_situation, extract_action, extract_task, extract_result],
        output_type=HREvaluation,
    )
