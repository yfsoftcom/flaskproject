all: target build push clean

PROXY=socks5h://127.0.0.1:7070
ifdef proxy
PROXY = $(proxy)
endif
target:
	@echo target
test:
	python -m unittest discover -s apps/$(proj)/test -v -p *$(file).py
dev:
	PROXY=$(PROXY) python3 apps/main.py
run:
	docker-compose up -d
install:
	pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --user --upgrade
	pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --user --upgrade
build:
	docker build --tag yfsoftcom/xv_search .
push:
	docker push yfsoftcom/xv_search
clean:
	@echo ok