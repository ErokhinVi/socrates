from app.model.ttt import TTT
from agents import function_tool

from typing import List
from pydantic import BaseModel

ttt = TTT()

class Message(BaseModel):
    role: str
    content: str

extract_task_json = {
            "type": "function",
            "name": "extract_task",
            "description": "Извлечь элемент Task (Задача) из стенограммы собеседования. Не выдумывайте ничего, используйте только предоставленную стенограмму собеседования.",
            "parameters": {
                "type": "object",
                "properties": {
                    "Task": {"type": "string", "description": "Извлеченная задача из собеседования. Если задача не указана, не выдумывайте ее, просто укажите, что задача не описана."}
                },
                "required": ["Task"],
                "additionalProperties": False
            },
            "strict": True,
        }


@function_tool
def extract_task(messages: List[Message]) -> str:
    """
    Извлечь элемент Task (Задача) из стенограммы собеседования. Не выдумывайте ничего, используйте только предоставленную стенограмму собеседования.

    Args:
        messages (list): Список сообщений из стенограммы собеседования. Каждое сообщение - словарь, содержащий 'role' и 'content'.

    Return:
        str: Извлеченная задача из собеседования. Если задача не указана, возвращается сообщение, что задача не описана.
    """

    response = ttt.generate_response_with_function(
        messages=messages,
        functions=[extract_task_json],
    )
    print("Response from extract_task:", response)
    return response