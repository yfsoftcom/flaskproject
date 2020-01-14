FROM python:3.7
COPY ./requirements.txt /requirements.txt
COPY ./apps /apps
WORKDIR /apps
RUN pip install --no-cache-dir -r /requirements.txt
# -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 5555

CMD ["python", "main.py"]