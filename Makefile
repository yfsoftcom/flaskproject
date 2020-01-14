all: target build push clean

target:
	@echo target
test:
	 python -m unittest discover -s apps/$(proj)/test -v -p *$(file).py
dev:
	python3 apps/main.py
run:
	docker run -e NET_MODE=GLOBAL --restart=always -p 5555:5555 -d --name xv_search yfsoftcom/xv_search
install:
	pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
build:
	docker build --tag yfsoftcom/xv_search .
push:
	docker push yfsoftcom/xv_search
clean:
	@echo ok