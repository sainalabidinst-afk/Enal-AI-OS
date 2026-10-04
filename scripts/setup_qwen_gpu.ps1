@echo off
echo ============================================
echo  Qwen GPU Setup - Enal AI OS
echo  GPU: NVIDIA RTX 2000 Ada (16GB VRAM)
echo ============================================
echo.

echo [1/3] Checking Python version...
python --version
echo.

echo [2/3] Installing PyTorch with CUDA 12.8...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
echo.

echo [3/3] Installing vLLM with CUDA support...
pip install vllm
echo.

echo ============================================
echo  Setup Complete!
echo ============================================
pause
