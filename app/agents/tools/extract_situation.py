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
            "description": "Извлечь элемент Situation (Ситуация) из стенограммы собеседования. Не выдумывайте ничего, используйте только предоставленную стенограмму собеседования.",
            "parameters": {
                "type": "object",
                "properties": {
                    "Situation": {"type": "string", "description": "Извлеченная ситуация из собеседования. Если ситуация не указана, не выдумывайте ее, просто укажите, что ситуация не описана."}
                },
                "required": ["Situation"],
                "additionalProperties": False
            },
            "strict": True,
        }

@function_tool
def extract_situation(messages: List[Message]) -> str:
    """
    Извлечь элемент Situation (Ситуация) из стенограммы собеседования. Не выдумывайте ничего, используйте только предоставленную стенограмму собеседования.

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