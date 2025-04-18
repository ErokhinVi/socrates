from agents import Agent
from app.agents.tools.lie_answer import lie_answer

def create_interviewee_agent(system_prompt: str) -> Agent:
    return Agent(
        name="Агент кандидата на работу",
        handoff_description="Ты кандидат, который отвечает на вопросы на основе персоны и проверяемого навыка",
        instructions=system_prompt,
        tools=[lie_answer],
    )