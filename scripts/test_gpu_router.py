"""Smoke-test GPU inference through the ModelRouter.

Requires a local CUDA device plus weights at ``settings.GPU_MODEL_PATH``.
Set ``GPU_INFERENCE_ENABLED=true`` in the environment before running; otherwise
the router degrades to ``settings.FALLBACK_MODEL`` and no weights are loaded.

    python scripts/test_gpu_router.py
"""

import asyncio
import logging
import os

from backend.app.core.gpu_inference_service import GPUInferenceError, get_gpu_service
from backend.app.core.model_router import ModelRouter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MODEL = "gpu/qwen2.5-3b"


async def main() -> int:
    os.environ.setdefault("GPU_INFERENCE_ENABLED", "true")

    service = get_gpu_service()
    if service is None:
        logger.error("GPU service disabled — set GPU_INFERENCE_ENABLED=true")
        return 1

    logger.info("GPU service status: %s", service.status())
    try:
        await asyncio.to_thread(service.initialize)
    except GPUInferenceError as exc:
        logger.error("GPU model unavailable: %s", exc)
        return 1

    router = ModelRouter()
    router.default_model = MODEL

    messages = [
        {"role": "system", "content": "You are Jenny, a helpful assistant."},
        {"role": "user", "content": "Explain observability in one sentence."},
    ]

    result = await router.acomplete(messages, model=MODEL, max_tokens=64, temperature=0.7)
    print("\n=== ModelRouter GPU Result ===")
    print(result)
    print("=== End of Result ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
