from app.model.ttt import TTT

from agents import function_tool

from typing import List
from pydantic import BaseModel

ttt = TTT()

class Message(BaseModel):
    role: str
    content: str

extract_action_json = {
            "type": "function",
            "name": "extract_action",
            "description": "Опиши **Action** в критерии оценки из четырёх компонент STAR: подробная оценка, подробна критика и подробные рекомендации. Обязательно уточни был ли раскрыт компонент: ✅ | ❌",
            "parameters": {
                "type": "object",
                "properties": {
                    "Action": {"type": "string", "description": "Извлеченные действия из собеседования."}
                },
                "required": ["Action"],
                "additionalProperties": False
            },
            "strict": True,
        }

@function_tool
def extract_action(messages: List[Message]) -> str:
    """
    Опиши **Action** в критерии оценки из четырёх компонент STAR: подробная оценка, подробна критика и подробные рекомендации. Обязательно уточни был ли раскрыт компонент: ✅ | ❌

    Args:
        messages (list): Список сообщений из стенограммы собеседования. Каждое сообщение - словарь, содержащий 'role' и 'content'.

    Return:
        str: Извлеченные действия из собеседования. Если действия не указаны, возвращается сообщение, что действия не описаны.
    """

    response = ttt.generate_response_with_function(
        messages=messages,
        functions=[extract_action_json]
    )
    print("Response from extract_action:", response)
    return response