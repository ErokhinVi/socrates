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
            "description": "Извлечь элемент Action (Действия) из стенограммы собеседования. Не выдумывайте ничего, используйте только предоставленную стенограмму собеседования.",
            "parameters": {
                "type": "object",
                "properties": {
                    "Action": {"type": "string", "description": "Извлеченные действия из собеседования. Если действия не указаны, не выдумывайте их, просто укажите, что действия не описаны."}
                },
                "required": ["Action"],
                "additionalProperties": False
            },
            "strict": True,
        }

@function_tool
def extract_action(messages: List[Message]) -> str:
    """
    Извлечь элемент Action (Действия) из стенограммы собеседования. Не выдумывайте ничего, используйте только предоставленную стенограмму собеседования.

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