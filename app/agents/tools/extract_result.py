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
            "description": "Опиши **Result** в критерии оценки из четырёх компонент STAR: подробная оценка, подробна критика и подробные рекомендации. Обязательно уточни был ли раскрыт компонент: ✅ | ❌",
            "parameters": {
                "type": "object",
                "properties": {
                    "Result": {"type": "string", "description": "Извлеченный результат из собеседования. "}
                },
                "required": ["Result"],
                "additionalProperties": False
            },
            "strict": True,
        }

@function_tool
def extract_result(messages: List[Message]) -> str:
    """
    Опиши **Result** в критерии оценки из четырёх компонент STAR: подробная оценка, подробна критика и подробные рекомендации. Обязательно уточни был ли раскрыт компонент: ✅ | ❌

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