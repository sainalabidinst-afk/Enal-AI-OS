# Qwen GPU Inference Guide

**Objective:** Run Qwen2.5-7B on NVIDIA RTX 2000 Ada (16GB VRAM) without AVX2 CPU dependency.

**Why GPU?** Ollama `0.1.26` fails on this host due to `libext_server.so` mapping issues. vLLM/Transformers bypass this by using CUDA directly.

---

## Prerequisites Check

```bash
# Verify GPU
nvidia-smi

# Verify CUDA driver (should show CUDA Version)
nvidia-smi | grep "CUDA Version"

# Verify Python
python --version  # Should be 3.11+
```

**Current System:**
- GPU: NVIDIA RTX 2000 Ada Generation
- VRAM: 16GB
- CUDA Driver: 13.2
- Python: 3.11.9

---

## Option A: vLLM (Recommended - Faster)

### 1. Install vLLM with CUDA Support

```powershell
# Install PyTorch with CUDA 12.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# Install vLLM
pip install vllm
```

**Note:** vLLM requires CUDA 11.8+. This system has CUDA 13.2 driver, which is backward compatible.

### 2. Download Model

```powershell
# Create models directory
mkdir E:\Enal-AI-OS\models\qwen2.5-7b

# Download from Hugging Face (requires git-lfs)
git lfs install
git clone https://huggingface.co/Qwen/Qwen2.5-7B E:\Enal-AI-OS\models\qwen2.5-7B
```

**Alternative:** Use `huggingface-cli`:
```powershell
pip install huggingface-hub
huggingface-cli download Qwen/Qwen2.5-7B --local-dir E:\Enal-AI-OS\models\qwen2.5-7B
```

### 3. Run Inference

```powershell
python E:\Enal-AI-OS\scripts\qwen_gpu_inference.py `
  --model-path E:\Enal-AI-OS\models\qwen2.5-7B `
  --prompt "Hello, can you summarize AI governance?" `
  --max-tokens 256 `
  --temperature 0.7
```

**Parameters:**
- `--tensor-parallel 1`: Use single GPU (RTX 2000 Ada)
- `--gpu-memory-utilization 0.9`: Use 90% of VRAM

---

## Option B: Hugging Face Transformers (Fallback)

If vLLM installation fails or is too large:

### 1. Install Transformers

```powershell
pip install transformers accelerate bitsandbytes
```

### 2. Download Model

Same as Option A.

### 3. Run Inference

```powershell
python E:\Enal-AI-OS\scripts\qwen_gpu_transformers.py `
  --model-name Qwen/Qwen2.5-7B `
  --prompt "Hello, explain observability in AI systems." `
  --max-length 256
```

**Note:** First run will download the model to Hugging Face cache if not present locally.

---

## VRAM Requirements

| Model | VRAM (FP16) | VRAM (INT8) | VRAM (INT4) |
|-------|-------------|-------------|-------------|
| Qwen2.5-7B | ~14GB | ~8GB | ~5GB |
| Qwen2.5-3B | ~6GB | ~4GB | ~2.5GB |
| Qwen2.5-1.5B | ~3GB | ~2GB | ~1.2GB |

**Current GPU:** 16GB VRAM → Can run 7B model in FP16 comfortably.

---

## Troubleshooting

### Issue: `torch.cuda.is_available()` returns False
**Solution:**
1. Update NVIDIA driver: https://www.nvidia.com/Download/index.aspx
2. Reinstall PyTorch with correct CUDA version:
   ```powershell
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
   ```

### Issue: vLLM installation fails
**Solution:** Use Transformers fallback (Option B).

### Issue: Out of VRAM
**Solution:** Use smaller model or quantization:
```powershell
# Use 3B model instead
python E:\Enal-AI-OS\scripts\qwen_gpu_inference.py --model-path Qwen/Qwen2.5-3B
```

---

## Integration with ECP Backend

To integrate this with the ECP backend, create an API endpoint that:
1. Receives prompt from frontend
2. Calls the vLLM/Transformers inference script
3. Returns response

See `apps/trading_analyst/engine.py` for integration pattern.

---

## Performance Expectations

| Model | Method | Tokens/sec (RTX 2000 Ada) |
|-------|--------|---------------------------|
| Qwen2.5-7B | vLLM | ~50-80 tokens/sec |
| Qwen2.5-7B | Transformers | ~20-30 tokens/sec |
| Qwen2.5-3B | vLLM | ~100-150 tokens/sec |

---

## Next Steps

1. Run setup script: `E:\Enal-AI-OS\scripts\setup_qwen_gpu.ps1`
2. Download model: `git clone https://huggingface.co/Qwen/Qwen2.5-7B E:\Enal-AI-OS\models\qwen2.5-7B`
3. Test inference: `python E:\Enal-AI-OS\scripts\qwen_gpu_inference.py`
4. Integrate with backend API
