"""Smoke-test GPU inference directly against GPUInferenceService.

Requires a local CUDA device plus weights at ``settings.GPU_MODEL_PATH``.
    python scripts/test_gpu_integration.py
"""

import asyncio
import logging

from backend.app.core.config import settings
from backend.app.core.gpu_inference_service import GPUInferenceError, GPUInferenceService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main() -> int:
    service = GPUInferenceService(model_path=settings.GPU_MODEL_PATH)
    logger.info("GPU service status: %s", service.status())

    try:
        await asyncio.to_thread(service.initialize)
    except GPUInferenceError as exc:
        logger.error("GPU model unavailable: %s", exc)
        return 1

    messages = [
        {"role": "system", "content": "You are Jenny, a helpful assistant."},
        {"role": "user", "content": "Hello, can you explain observability in AI systems?"},
    ]

    result = await service.chat(messages, max_tokens=128, temperature=0.7)
    print("\n=== GPU Inference Result ===")
    print(result)
    print("=== End of Result ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
