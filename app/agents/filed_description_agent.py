from agents import Agent
from app.agents.tools.lie_answer import lie_answer

def create_filed_description_agent(system_prompt: str) -> Agent:
    return Agent(
        name="Агент описания профессии",
        handoff_description="Ты инструктор по профессиям, ты помогаешь hr специалистам разобраться в тонкостях профессий для лучшего понимания образа потенциального кандидата и требований к нему",
        instructions=system_prompt,
        tools=[lie_answer],
    )