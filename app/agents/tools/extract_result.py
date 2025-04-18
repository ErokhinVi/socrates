from app.model.ttt import TTT

from agents import function_tool

from typing import List
from pydantic import BaseModel

ttt = TTT()

class Message(BaseModel):
    role: str
    content: str

extract_result_json = {
            "type": "function",
            "name": "extract_result",
            "description": "Извлечь элемент Result (Результат) из стенограммы собеседования. Не выдумывайте ничего, используйте только предоставленную стенограмму собеседования.",
            "parameters": {
                "type": "object",
                "properties": {
                    "Result": {"type": "string", "description": "Извлеченный результат из собеседования. Если результат не указан, не выдумывайте его, просто укажите, что результат не описан."}
                },
                "required": ["Result"],
                "additionalProperties": False
            },
            "strict": True,
        }

@function_tool
def extract_result(messages: List[Message]) -> str:
    """
    Извлечь элемент Result (Результат) из стенограммы собеседования. Не выдумывайте ничего, используйте только предоставленную стенограмму собеседования.

    Args:
        messages (list): Список сообщений из стенограммы собеседования. Каждое сообщение - словарь, содержащий 'role' и 'content'.

    Return:
        str: Извлеченный результат из собеседования. Если результат не указан, возвращается сообщение, что результат не описан.
    """

    response = ttt.generate_response_with_function(
        messages=messages,
        functions=[extract_result_json]
    )
    print("Response from extract_result:", response)
    return response