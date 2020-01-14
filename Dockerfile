FROM python:3.7-alpine
COPY ./requirements.txt /requirements.txt
WORKDIR /apps
RUN apk add --update --no-cache --virtual .build-deps \
        g++ \
        python-dev \
        libxml2 \
        libxml2-dev && \
        apk add libxslt-dev  && \
        pip install --no-cache-dir -r /requirements.txt && \
        apk del .build-deps
# -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 5555

CMD ["python", "main.py"]