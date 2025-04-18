from app.model.ttt import TTT
from agents import function_tool

from typing import List
from pydantic import BaseModel

ttt = TTT()

class Message(BaseModel):
    role: str
    content: str

extract_situation_json = {
            "type": "function",
            "name": "extract_situation",
            "description": "Опиши **Situation** в критерии оценки из четырёх компонент STAR: подробная оценка, подробна критика и подробные рекомендации. Обязательно уточни был ли раскрыт компонент: ✅ | ❌",
            "parameters": {
                "type": "object",
                "properties": {
                    "Situation": {"type": "string", "description": "Извлеченная ситуация из собеседования."}
                },
                "required": ["Situation"],
                "additionalProperties": False
            },
            "strict": True,
        }

@function_tool
def extract_situation(messages: List[Message]) -> str:
    """
    Опиши **Situation** в критерии оценки из четырёх компонент STAR: подробная оценка, подробна критика и подробные рекомендации. Обязательно уточни был ли раскрыт компонент: ✅ | ❌

    Args:
        messages (list): Список сообщений из стенограммы собеседования. Каждое сообщение - словарь, содержащий 'role' и 'content'.

    Return:
        str: Извлеченная ситуация из собеседования. Если ситуация не указана, возвращается сообщение, что ситуация не описана.
    """

    response = ttt.generate_response_with_function(
        messages=messages,
        functions=[extract_situation_json]
    )
    print("Response from extract_situation:", response)
    return response