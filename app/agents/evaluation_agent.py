from agents import Agent
from app.agents.tools.extract_situation import extract_situation
from app.agents.tools.extract_task import extract_task
from app.agents.tools.extract_action import extract_action
from app.agents.tools.extract_result import extract_result
from pydantic import BaseModel, Field


class HREvaluation(BaseModel):
    Situation: str = Field(
        ...,
        description="Опиши **Situation** ПО ВСЕМУ ДИАЛОГУ в критерии оценки из четырёх компонент STAR: подробная оценка, подробна критика и подробные рекомендации КАК НАДО БЫЛО БЫ СПРОСИТЬ. Обязательно уточни был ли раскрыт компонент:  ✅ (ЗЕЛЕНАЯ ГАЛОЧКА)| ❌ (КРАСНЫЙ КРЕСТИК)",
    )
    Task: str = Field(
        ...,
        description="Опиши **Task** ПО ВСЕМУ ДИАЛОГУ в критерии оценки из четырёх компонент STAR: подробная оценка, подробна критика и подробные рекомендации КАК НАДО БЫЛО БЫ СПРОСИТЬ. Обязательно уточни был ли раскрыт компонент:  ✅ (ЗЕЛЕНАЯ ГАЛОЧКА)| ❌ (КРАСНЫЙ КРЕСТИК)",
    )
    Action: str = Field(
        ...,
        description="Опиши **Action** ПО ВСЕМУ ДИАЛОГУ в критерии оценки из четырёх компонент STAR: подробная оценка, подробна критика и подробные рекомендации КАК НАДО БЫЛО БЫ СПРОСИТЬ. Обязательно уточни был ли раскрыт компонент:  ✅ (ЗЕЛЕНАЯ ГАЛОЧКА)| ❌ (КРАСНЫЙ КРЕСТИК)",
    )
    Result: str = Field(
        ...,
        description="Опиши **Result** ПО ВСЕМУ ДИАЛОГУ в критерии оценки из четырёх компонент STAR: подробная оценка, подробна критика и подробные рекомендации КАК НАДО БЫЛО БЫ СПРОСИТЬ. Обязательно уточни был ли раскрыт компонент:  ✅ (ЗЕЛЕНАЯ ГАЛОЧКА)| ❌ (КРАСНЫЙ КРЕСТИК)",
    )


def create_evaluation_agent(system_prompt: str) -> Agent:
    return Agent(
        name="HR STAR Evaluation",
        handoff_description="AI‑оценщик HR по методике STAR в Райффайзен Банке.",
        instructions=system_prompt,
        # tools=[extract_situation, extract_action, extract_task, extract_result],
        output_type=HREvaluation,
    )
