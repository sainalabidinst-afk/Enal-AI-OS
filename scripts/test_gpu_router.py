"""Test GPU inference through ModelRouter."""
import asyncio
import logging

from backend.app.core.config import Settings
from backend.app.core.gpu_inference_service import GPUInferenceService
from backend.app.core.model_router import ModelRouter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    settings = Settings(GPU_INFERENCE_ENABLED=True)
    service = GPUInferenceService(model_path=settings.GPU_MODEL_PATH)
    await service.initialize()

    router = ModelRouter()
    router.default_model = "gpu/qwen2.5-3b"

    messages = [
        {"role": "system", "content": "You are Jenny, a helpful assistant."},
        {"role": "user", "content": "Explain observability in one sentence."},
    ]

    result = await router.acomplete(messages, model="gpu/qwen2.5-3b", max_tokens=64, temperature=0.7)
    print("\n=== ModelRouter GPU Result ===")
    print(result)
    print("=== End of Result ===")


if __name__ == "__main__":
    asyncio.run(main())
