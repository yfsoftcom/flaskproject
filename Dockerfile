FROM python:3.7.6-alpine3.10
WORKDIR /apps
RUN pip install lxml && \
    pip install requests && \
    pip install flask
# -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 5555

CMD ["python", "main.py"]