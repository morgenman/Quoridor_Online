# dev Repository

## To bring online:

```bash
docker-compose up
```
if you don't want to see the logs after you start it up you can run this instead
```bash
docker-compose up -d
```

## To take it offline:

```bash
docker-compose down
```

## To run tests

See /Selenium_test/README.txt

## API:

### To run tests

```bash
docker exec -it api bash
python test_engine_unittest.py
```

### http_server.py
handles all the http requests on the api side, handling newgame requests, piece and wall movements, and player queue

### game_engine.py
handles a few in-between functions for making games

### game_classes.py
holds the main body of the api:

all the classes (tile, game, and player) with appropriate methods as well as all currently active games