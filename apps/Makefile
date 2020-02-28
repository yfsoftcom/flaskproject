all: test

docker-redis:
	docker run -p 6379:6379 -d --name redis-server redis:alpine3.11 

redis-client:
	docker exec -it redis-server redis-cli

test:
	python -m unittest discover -s $(proj)/test -v -p *$(file).py

perform:
	curl localhost:5555/xv/api/search/p/0/jv
	curl localhost:5555/xv/api/top3
	curl localhost:5555/xv/api/video/8768021/asian_teen_shows_her_nice_body_for_a_photographer

