"""
Qwen2.5-7B GPU Inference with vLLM
No AVX2 CPU dependency - runs entirely on GPU
"""
import argparse

from vllm import LLM, SamplingParams


def main():
    parser = argparse.ArgumentParser(description="Qwen2.5-7B GPU Inference")
    parser.add_argument("--model-path", default="./models/qwen2.5-7b", help="Path to model")
    parser.add_argument("--prompt", default="Hello, can you summarize AI governance?", help="Prompt")
    parser.add_argument("--max-tokens", type=int, default=256, help="Max tokens")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature")
    parser.add_argument("--tensor-parallel", type=int, default=1, help="Tensor parallel size")
    args = parser.parse_args()

    print(f"Loading model from: {args.model_path}")
    llm = LLM(
        model=args.model_path,
        tensor_parallel_size=args.tensor_parallel,
        gpu_memory_utilization=0.9,
    )

    sampling_params = SamplingParams(
        temperature=args.temperature,
        max_tokens=args.max_tokens,
    )

    print(f"\nPrompt: {args.prompt}")
    print("\nGenerating response...")
    outputs = llm.generate([args.prompt], sampling_params)

    for output in outputs:
        print(f"\nResponse:\n{output.outputs[0].text}")


if __name__ == "__main__":
    main()
