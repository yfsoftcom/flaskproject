all: target build push clean

target:
	@echo target
dev:
	python3 apps/main.py
install:
	pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
build:
	@echo build
push:
	@echo push
clean:
	@echo ok