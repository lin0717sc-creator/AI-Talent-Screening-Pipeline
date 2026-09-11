# 1. 声明基础环境：使用官方极其轻量的 Python 3.10 slim 版本
FROM python:3.10-slim

# 2. 设置容器内的工作目录
WORKDIR /app

# 3. 优化缓存层：先把依赖清单拷进去安装，这样只要依赖不改，这层就能复用
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 4. 把你所有的代码和配置全部拷入集装箱
COPY . .

# 5. 声明数据卷：告诉 Docker，这里的 data 文件夹是用来和外界通讯的
VOLUME ["/app/data"]

# 6. 点火指令：当容器启动时，执行这个命令
CMD ["python", "main.py"]