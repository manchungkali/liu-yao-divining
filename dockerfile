# 使用官方的 Python 运行时作为父镜像
FROM python:3.8-slim-buster

# 在容器内将工作目录设置为 /app
WORKDIR /app

# 将当前目录内容添加到容器的 /app 里
ADD . /app

# 更新系统包，安装构建工具并清理缓存
RUN apt-get update -o Debug::pkgProblemResolver=yes && \
    apt-get install -y --no-install-recommends gcc build-essential && \
    rm -rf /var/lib/apt/lists/*

# 安装 requirements.txt 指定的任何需要的软件包
RUN pip install --no-cache-dir -r requirements.txt

# 暴露 Streamlit 使用的端口（默认为 8501）
EXPOSE 8501

# 当容器启动时运行 main.py
CMD ["streamlit", "run", "main.py"]
