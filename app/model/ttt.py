from typing import List, Dict, Union, Any
from app.core.openai import client
import json


class TTT:
    def __init__(self, model: str = "gpt-4.1-mini"):
        self.client = client
        self.model = model

    def generate_response(self, messages: List[Dict[str, str]]) -> str:
        """
        Generate text response
        """
        try:
            response = self.client.responses.create(
                model=self.model,
                input=messages
            )
            return response.output_text

        except Exception as e:
            return f"Error generating response: {str(e)}"

    def generate_response_with_function(self, messages: List[Dict[str, str]], functions: List[Dict] = None) -> Union[str, Dict]:
        """
        Generate text response with function call
        """
        try:
            params = {
                "model": self.model,
                "input": messages,
                "tools": functions,
                "tool_choice": "required"
            }
            response = self.client.responses.create(**params)
            tool_call = response.output[0]
            print("Tool call:", tool_call)
            args = json.loads(tool_call.arguments)
            return args
            
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def create_chat_message(self, role: str, content: str) -> Dict[str, str]:
        """
        Create chat message with role and content
        """
        return {
            "role": role,
            "content": content
        }