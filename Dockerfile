FROM python:3.7.6-alpine3.10
COPY ./requirements.txt /requirements.txt
WORKDIR /apps
RUN apk add --no-cache libxslt && \
    pip install -r /requirements.txt && \
    apk del .build-deps
# -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 5555

CMD ["python", "main.py"]