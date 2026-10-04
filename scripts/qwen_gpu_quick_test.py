"""
Quick Qwen GPU Inference Test
"""
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "E:/Enal-AI-OS/models/qwen2.5-3b"
prompt = "Hi"
max_length = 32

print(f"Loading model from: {model_name}")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.float16,
    device_map="auto",
)

print(f"Prompt: {prompt}")
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

print("Generating...")
with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_length=max_length,
        temperature=0.7,
        do_sample=True,
    )

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(f"\nResponse:\n{response}")
print("\nSUCCESS: GPU inference works!")
