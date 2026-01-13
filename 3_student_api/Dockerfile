FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 将当前目录下的所有文件复制到容器的 /app 目录
COPY . .

# 明确指定启动 app.main 模块中的 app 应用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]