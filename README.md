## Flask Projects

- [ ] XV Searcher
  Just For Fun!
  

### Test
```bash
python -m unittest discover -s test -v -p *.py
```

- Test Libs
```bash
cd apps
python -m unittest discover -s libs\test -v -p *.py
```

### Run Docker
```bash
docker-compose -f docker-compose.dev.yml up --build -d
```

Run in product mode
```bash
docker-compose up --build -d
```
Run in global mode
```bash
docker-compose -f docker-compose.global.yml up --build -d
```
### Run Ngrok
```bash
ngrok http 5555
```
- run backend
```bash
apt-install screen
screen -S keepngrok
ngrok http 5555
CTRL + A + D
```