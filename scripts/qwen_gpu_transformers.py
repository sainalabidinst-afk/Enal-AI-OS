"""
Qwen2.5-7B GPU Inference with Hugging Face Transformers
Fallback if vLLM has issues
"""

import argparse

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer


def main():
    parser = argparse.ArgumentParser(description="Qwen2.5-7B Transformers GPU Inference")
    parser.add_argument("--model-name", default="Qwen/Qwen2.5-7B", help="Model name")
    parser.add_argument(
        "--prompt", default="Hello, explain observability in AI systems.", help="Prompt"
    )
    parser.add_argument("--max-length", type=int, default=256, help="Max length")
    parser.add_argument("--temperature", type=float, default=0.7, help="Temperature")
    args = parser.parse_args()

    print(f"Loading model: {args.model_name}")
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    model = AutoModelForCausalLM.from_pretrained(
        args.model_name,
        torch_dtype=torch.float16,
        device_map="auto",
    )

    inputs = tokenizer(args.prompt, return_tensors="pt").to("cuda")

    print(f"\nPrompt: {args.prompt}")
    print("\nGenerating response...")
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=args.max_length,
            temperature=args.temperature,
            do_sample=True,
        )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"\nResponse:\n{response}")


if __name__ == "__main__":
    main()
