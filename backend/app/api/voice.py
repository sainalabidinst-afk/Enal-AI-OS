from __future__ import annotations

import logging
from typing import Any

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    Query,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import StreamingResponse

from backend.app.core.config import settings
from backend.app.core.voice_vision_agent import VoiceTranscription, voice_agent

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/voice", tags=["voice"])


@router.get("/languages")
async def supported_languages() -> dict[str, list[str]]:
    return {"languages": voice_agent.get_supported_languages()}


@router.get("/providers")
async def provider_info() -> dict[str, Any]:
    return {
        "stt_provider": settings.STT_PROVIDER,
        "tts_provider": settings.TTS_PROVIDER,
        "tts_voice": settings.TTS_VOICE,
        "stt_language": settings.STT_LANGUAGE,
        "supported_languages": voice_agent.get_supported_languages(),
    }


@router.post("/transcribe", response_model=VoiceTranscription)
async def transcribe_audio(
    file: UploadFile = File(..., description="Audio file (WAV recommended)"),
    language: str = Query(default="id", description="Language code (e.g. 'id', 'en')"),
) -> VoiceTranscription:
    try:
        audio_data = await file.read()
        if not audio_data:
            raise HTTPException(status_code=400, detail="No audio data received")
        result = await voice_agent.transcribe(audio_data, language=language)
        return result
    except Exception as e:
        logger.error("Transcription failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Transcription failed: {e}") from e


@router.post("/speak")
async def synthesize_speech(
    text: str = Query(..., min_length=1, max_length=5000, description="Text to synthesize"),
    voice: str = Query(default="", description="Voice identifier (e.g. 'en', 'id')"),
    speed: float = Query(default=1.0, ge=0.5, le=2.0, description="Speech rate multiplier"),
) -> StreamingResponse:
    try:
        v = voice if voice else settings.TTS_VOICE
        audio_data = await voice_agent.speak(text, voice=v, speed=speed)
        return StreamingResponse(
            iter([audio_data]),
            media_type="audio/wav",
            headers={"Content-Disposition": "inline"},
        )
    except Exception as e:
        logger.error("TTS synthesis failed: %s", e)
        raise HTTPException(status_code=500, detail=f"TTS synthesis failed: {e}") from e


@router.websocket("/ws/voice")
async def voice_websocket(ws: WebSocket):
    """WebSocket endpoint for real-time voice streaming.

    Client sends binary audio chunks; server responds with transcriptions
    as JSON messages.

    Protocol:
        - Client sends binary frame: raw audio bytes (WAV, 16kHz)
        - Server responds with JSON: {"text": "...", "confidence": 0.x, "final": true/false}
        - Client sends "STOP" text frame to end session
    """
    await ws.accept()
    logger.info("Voice WebSocket connection established")

    try:
        audio_buffer = bytearray()
        while True:
            data = await ws.receive()
            if data is None:
                continue

            if isinstance(data, bytes):
                audio_buffer.extend(data)

                if len(audio_buffer) >= 16000:
                    try:
                        result = await voice_agent.transcribe(
                            bytes(audio_buffer),
                            language=settings.STT_LANGUAGE,
                        )
                        await ws.send_json({
                            "text": result.text,
                            "confidence": result.confidence,
                            "language": result.language,
                            "final": bool(result.text),
                        })
                        audio_buffer.clear()
                    except Exception as e:
                        await ws.send_json({
                            "error": str(e),
                            "final": True,
                        })
                        audio_buffer.clear()

            elif isinstance(data, str):
                if data.strip().upper() == "STOP":
                    await ws.send_json({"type": "session_ended"})
                    await ws.close()
                    return

    except WebSocketDisconnect:
        logger.info("Voice WebSocket client disconnected")
    except Exception as e:
        logger.error("Voice WebSocket error: %s", e)
        try:
            await ws.send_json({"error": str(e), "final": True})
            await ws.close()
        except Exception:
            pass
