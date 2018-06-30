### Something Kit For Worldcup-2018

##### Usage
```bash
$ pip install -r requirements.txt
```

##### Test
- test one `test_*.py`
  ```bash
  $ python -m unittest discover -s test -v -p *logic.py
  ```


- [ ] Get The Basic Data
  - [x] Teams
    - [x] static data:
      ```
      ["俄罗斯", "沙特阿拉伯", "埃及", "乌拉圭"], 
      ["葡萄牙", "西班牙", "摩洛哥", "伊朗"], 
      ["法国", "澳大利亚", "秘鲁", "丹麦"], 
      ["阿根廷", "冰岛", "克罗地亚", "尼日利亚"], 
      ["巴西", "瑞士", "哥斯达黎加", "塞尔维亚"], 
      ["德国", "墨西哥", "瑞典", "韩国"], 
      ["比利时", "巴拿马", "突尼斯", "英格兰"], 
      ["波兰", "塞内加尔", "哥伦比亚", "日本"]
      ```
    - [ ] top 16 teams
    - [ ] top 8 teams
    - [ ] top 4 teams
    - [ ] champion

  - [x] Matches
    - [x] Group Matches
    - [x] set match
      - [x] The Actual Matches' Result Ranking & Score
    - [x] calc score and goals
    - [x] calc ranking of each team in group
    - [x] ~Fetch Actual Matches' Result From Web [http://2018.zgzcw.com/](http://2018.zgzcw.com/)~
    - [x] Fetch Actual Matches' Result From Web [http://matchweb.sports.qq.com/matchUnion/list?startTime=2018-06-14&endTime=2018-07-20&columnId=4&index=0](http://matchweb.sports.qq.com/matchUnion/list?startTime=2018-06-14&endTime=2018-07-20&columnId=4&index=0)

- [x] Forecast Matchs
  - [x] calc ranking of each team in group
  - [x] calc 

- [x] Get Tech Count
  - [ ] Fetch From [http://ziliaoku.sports.qq.com/cube/index?cubeId=32&dimId=61&params=t2:4&order=t1&from=sportsdatabase](http://ziliaoku.sports.qq.com/cube/index?cubeId=32&dimId=61&params=t2:4&order=t1&from=sportsdatabase)

- [x] Fetch Lottery By Request
  Data From [http://cp.zgzcw.com/lottery/jchtplayvsForJsp.action?lotteryId=47&type=jcmini](http://cp.zgzcw.com/lottery/jchtplayvsForJsp.action?lotteryId=47&type=jcmini)
  - [x] Get Nearly 9 Matches Lottery Data
  - [x] Calc the Input/Return/Rate Of The 9 Matches


#### docker
```bash
$ docker build --tag worldcup .
$ docker run -d --name worldcup -p 5000:5000 worldcup
```


#### Use grpc to provider an micro-service
```
$ python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=./service/ ./service/service.proto
```