FROM python:3.6.5
COPY ./requirements.txt /requirements.txt
WORKDIR /apps
RUN pip install -r /requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 5555

CMD ["python", "main.py"]