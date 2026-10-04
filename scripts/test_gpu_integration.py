"""Test GPU inference integration with ECP backend."""
import asyncio
import logging

from backend.app.core.gpu_inference_service import GPUInferenceService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    model_path = "E:/Enal-AI-OS/models/qwen2.5-3b"
    service = GPUInferenceService(model_path=model_path)
    await service.initialize()

    messages = [
        {"role": "system", "content": "You are Jenny, a helpful assistant."},
        {"role": "user", "content": "Hello, can you explain observability in AI systems?"},
    ]

    result = await service.chat(messages, max_tokens=128, temperature=0.7)
    print("\n=== GPU Inference Result ===")
    print(result)
    print("=== End of Result ===")


if __name__ == "__main__":
    asyncio.run(main())
