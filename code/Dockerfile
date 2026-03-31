# 20250123
FROM python:3
MAINTAINER Jeff Yeh

# 設置工作目錄
WORKDIR /app

# install python library
RUN apt-get update
RUN apt-get install -y 
RUN pip3 install playwright
RUN python3 -m playwright install
RUN playwright install-deps

# 複製當前目錄的內容到容器的 /app 目錄
COPY config.json .
COPY *.py .


# 設置執行 clock_out.py 腳本的入口點
RUN cd /app
CMD ["python3", "./auto_clock.py"]
