from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query
from typing import List, Dict, Union, Any
import base64
import json
import os

from app.model.ttt import TTT
from app.model.stt import STT
from app.model.tts import TTS
from app.agents.prompts.utils import load_prompts
from agents import Runner
from app.agents.interviewee_agent import create_interviewee_agent
from app.agents.evaluation_agent import create_evaluation_agent

# временная директория (в контейнерах Heroku/Render /tmp всегда доступна на запись)
TEMP_DIR: str = "/tmp/ai-interview-temp"
os.makedirs(TEMP_DIR, exist_ok=True)

router = APIRouter()

ttt = TTT()
stt = STT()
tts = TTS()

interviewee_prompts: Dict[str, str] = load_prompts("persona_system_prompt.yaml")
evaluation_prompts: Dict[str, str] = load_prompts("evaluation_system_prompt.yaml")


async def run_star_evaluation(agent, history: str) -> Dict[str, str]:
    """
    Запускает агента‑оценщика и возвращает dict
    с ключами Situation / Task / Action / Result.
    """
    response = await Runner.run(agent, history)
    return response.final_output_as(cls=dict)


@router.websocket("/ws/interview")
async def websocket_interview(
    ws: WebSocket,
    persona: str = Query("Junior Python Developer"),
    skill: str = Query("Python programming"),
) -> None:
    """
    Основной WebSocket‑эндпоинт для интервью.
    """
    await ws.accept()

    system_prompt: str = interviewee_prompts["persona_system_prompt"].format(
        persona=persona, skill=skill
    )
    interviewee_agent = create_interviewee_agent(system_prompt)
    star_agent = create_evaluation_agent(evaluation_prompts["evaluation_system_prompt"])

    messages: List[Dict[str, Union[str, Dict[str, str]]]] = []

    try:
        # ---------- блок уточняющих вопросов ----------
        response = await Runner.run(
            interviewee_agent,
            "Задай уточняющие вопросы по переданному контексту",
        )
        clarifying_text: str = "Уточняющие вопросы:\n\n" + response.final_output.strip()
        messages.append(ttt.create_chat_message("assistant", clarifying_text))
        await ws.send_json({"type": "text", "content": clarifying_text})

        # ---------- основной цикл интервью ----------
        while True:
            raw: str = await ws.receive_text()
            data: Dict[str, Any] = json.loads(raw)

            # ---------- завершение интервью ----------
            print(messages)
            if data.get("type") == "end":
                history_str: str = ttt.create_history_template(messages)
                print("---" * 300)
                print(history_str)
                star_result: Dict[str, str] = await run_star_evaluation(
                    star_agent, history_str
                )
                await ws.send_json(
                    {
                        "type": "star_summary",
                        "star": star_result.model_dump(),
                    }  # <-- важно: отправляем dict
                )
                break  # выходим из цикла — соединение будет закрыто сервером

            # ---------- текстовое сообщение ----------
            if data.get("type") == "text":
                user_input: str = data.get("message", "")
                is_audio: bool = False

            # ---------- аудио сообщение ----------
            elif data.get("type") == "audio":
                audio_bytes: bytes = base64.b64decode(data["audio"])
                tmp_path: str = os.path.join(TEMP_DIR, "temp_audio.webm")
                with open(tmp_path, "wb") as f:
                    f.write(audio_bytes)
                user_input = stt.transcribe_from_path(tmp_path)
                is_audio = True
            else:
                await ws.send_json({"type": "error", "text": "unknown message type"})
                continue

            # ---------- сохраняем реплику пользователя ----------
            messages.append(ttt.create_chat_message("user", user_input))

            # ---------- ответ агента‑интервьюера ----------
            history_for_agent: str = ttt.create_history_template(messages)
            response = await Runner.run(interviewee_agent, history_for_agent)
            assistant_text: str = response.final_output
            messages.append(ttt.create_chat_message("assistant", assistant_text))

            # ---------- отправляем ответ клиенту ----------
            if is_audio:
                tts_bytes = tts.generate_speech(
                    assistant_text,
                    tone=interviewee_prompts["persona_voice_tone_prompt"],
                ).content
                await ws.send_json(
                    {
                        "type": "voice",
                        "content": assistant_text,
                        "user_text": user_input,
                        "audio": base64.b64encode(tts_bytes).decode(),
                    }
                )
            else:
                await ws.send_json({"type": "text", "content": assistant_text})

    except WebSocketDisconnect:
        # клиент закрыл соединение
        pass
    finally:
        # сервер закрывает сокет, если ещё не закрыт
        await ws.close()
