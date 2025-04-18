from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
import base64
import json
import os

from app.model.ttt import TTT
from app.model.stt import STT
from app.model.tts import TTS
from app.agents.prompts.utils import load_prompts
from pprint import pp
from agents import Runner
# осздаем своего агента
from app.agents.filed_description_agent import create_filed_description_agent

# Используем директорию /tmp для временных файлов (доступна для записи всем пользователям)
# TEMP_DIR = "/tmp/ai-interview-temp"
TEMP_DIR = "/tmp/ai-field-description-temp"
os.makedirs(TEMP_DIR, exist_ok=True)

router = APIRouter()

ttt = TTT()
stt = STT()
tts = TTS()
# сюда добавляем наш промпт - еще не готов!!!
prompts = load_prompts("describe_professional_field.yaml")

# Вебсокет-эндпоинт для интервью

# Вот тут нужно сделать не для интрвью, а для описания!!!!
@router.websocket("/ws/interview") 
# async def websocket_interview(ws: WebSocket, persona: str = Query("Junior Python Developer"), skill: str = Query("Python programming")):
async def websocket_filed_description(ws: WebSocket, persona: str = Query("Junior Python Developer")):
    await ws.accept()  # Принимаем подключение
    # системный промпт для агента на основе выбранной персоны и навыка
    # меняем под наш промпт!!!!
    system_prompt = prompts["describe_professional_field"].format(persona=persona)
    # agent = create_interviewee_agent(system_prompt)  # агент для интервью
    # создаем своего агента!!!
    agent = create_filed_description_agent(system_prompt)  # агент для интервью
    try:
        while True:
            data = await ws.receive_text()  # сообщение от клиента
            json_data = json.loads(data)
            # if json_data["type"] == "text":  # текст
            #     user_input = json_data.get("message", "")
            #     is_audio = False
            user_input = json_data.get("message", "")
            # elif json_data["type"] == "audio":  # аудио
            #     audio_bytes = base64.b64decode(json_data["audio"])
            #     temp_audio_path = os.path.join(TEMP_DIR, "temp_audio.wav")
            #     with open(temp_audio_path, "wb") as f:
            #         f.write(audio_bytes)  # Сохраняем аудио во временный файл
            #     user_input = stt.transcribe_from_path(temp_audio_path)  # Распознаём речь
            #     is_audio = True
            # Формируем историю сообщений для передачи агенту
            messages = [ttt.create_chat_message(msg["role"], msg["content"]) for msg in json_data.get("history", [])]
            messages.append(ttt.create_chat_message("user", user_input))  # Добавляем текущее сообщение пользователя
            # Получаем ответ от агента
            response = await Runner.run(agent, messages)
            # response = await Runner.run(agent, user_input, context={"messages": messages}) # Вариант с контекстом
            agent_text = response.final_output  # Текстовый ответ агента
            # if is_audio:
            #     # Генерируем аудиофайл с ответом агента
            #     tts_response = tts.generate_speech(agent_text, tone=prompts["persona_voice_tone_prompt"])
            #     agent_audio = base64.b64encode(tts_response.content).decode('utf-8')
            #     # Отправляем клиенту текст и аудио
            #     await ws.send_json({"type": "voice", "content": agent_text, "user_text": user_input, "audio": agent_audio})
            # elif not is_audio:
                # Отправляем клиенту только текст
                # await ws.send_json({"type": "text", "content": agent_text})
            await ws.send_json({"type": "text", "content": agent_text})
            
    except WebSocketDisconnect:
        pass