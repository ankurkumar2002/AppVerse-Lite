# ✅ Use lightweight Python image
FROM python:3.11-slim

# ✅ Set working directory
WORKDIR /app

# ✅ Copy only requirements first (better caching)
COPY requirements.txt .

# ✅ Install CPU-only torch (prevents huge GPU install ❗)
RUN pip install --no-cache-dir \
    torch==2.2.2+cpu \
    torchvision==0.17.2+cpu \
    -f https://download.pytorch.org/whl/torch_stable.html

# ✅ Install remaining dependencies
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Copy all source code
COPY . .

# ✅ Expose FastAPI port
EXPOSE 8001

# ✅ Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]