from agents import Agent
from app.agents.tools.extract_situation import extract_situation
from app.agents.tools.extract_task import extract_task
from app.agents.tools.extract_action import extract_action
from app.agents.tools.extract_result import extract_result
from pydantic import BaseModel, Field


class HREvaluation(BaseModel):
    Situation: str = Field(
        ...,
        description="**Situation**: оценка, критика и рекомендации: насколько HR задавал вопросы, помогающие кандидату описать контекст ситуации.",
    )
    Task: str = Field(
        ...,
        description="**Task**: оценка, критика и рекомендации: насколько HR уточнял конкретную задачу, стоявшую перед кандидатом.",
    )
    Action: str = Field(
        ...,
        description="**Action**: оценка, критика и рекомендации: насколько HR побудил кандидата подробно описать свои действия.",
    )
    Result: str = Field(
        ...,
        description="**Result**: оценка, критика и рекомендации: насколько HR выяснил результаты, выводы и степень влияния действий кандидата.",
    )


def create_evaluation_agent(system_prompt: str) -> Agent:
    return Agent(
        name="Evaluation Agent",
        handoff_description="Оценка сообщений с использованием метода STAR.",
        instructions=system_prompt,
        tools=[extract_situation, extract_action, extract_task, extract_result],
        output_type=HREvaluation,
    )
