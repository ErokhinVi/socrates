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
            "description": "Опиши **Task** в критерии оценки из четырёх компонент STAR: подробная оценка, подробна критика и подробные рекомендации. Обязательно уточни был ли раскрыт компонент: ✅ | ❌",
            "parameters": {
                "type": "object",
                "properties": {
                    "Task": {"type": "string", "description": "Извлеченная задача из собеседования. "}
                },
                "required": ["Task"],
                "additionalProperties": False
            },
            "strict": True, 
        }


@function_tool
def extract_task(messages: List[Message]) -> str:
    """
    Опиши **Task** в критерии оценки из четырёх компонент STAR: подробная оценка, подробна критика и подробные рекомендации. Обязательно уточни был ли раскрыт компонент: ✅ | ❌

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