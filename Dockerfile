FROM python:3.7.6-alpine3.10
COPY ./requirements.txt /requirements.txt
WORKDIR /apps
RUN apk add --update --no-cache --virtual .build-deps \
        g++ \
        python-dev \
        libxml2 \
        libxml2-dev && \
    apk add libxslt-dev && \
    apk del .build-deps
RUN pip install -r /requirements.txt
# -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 5555

CMD ["python", "main.py"]