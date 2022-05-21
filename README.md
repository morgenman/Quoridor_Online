# Quoridor Online

Notes:
* All source files are located in the src directory
* Resources includes external licensed assets
* As is, the project is designed to run as a local instance, accessed by localhost
* The adjustments made on cs-devel have not been pushed to this repository, since the changes are specific to the hosting situation

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

## API:

### To run tests

```bash
docker exec -it api bash
python test_engine_unittest.py
```

### rerun.sh
This clever little script, definitely not hodge-podged from StackOverflow, will restart the API server ever time a file in the directory is touched with a five second delay.   
Just long enough to make a quick adjustment!

### http_server.py
handles all the http requests on the api side, handling newgame requests, piece and wall movements, and player queue

### game_engine.py
handles a few in-between functions for making games

### game_classes.py
holds the main body of the api:

all the classes (tile, game, and player) with appropriate methods as well as all currently active games

## Web:

Django APP is located in `/src/client/quoridor_site/quoridor_site_backend/`
Django site is located in `/src/client/quoridor_site/quoridor_site/`  

NPM environmnet is located in `/src/client/quoridor_site/`
* The default package manager is yarn, which can be invoked in this directory
* `./package.json` is the package.json file for the project
* The JS files used for this project are located in `./quoridor_site_backend/static/`

The primary js file which handles the game rendering is called `game_canvas.js`

The file which handles the queueing mechanism on the user side is located in `queue.js`. 

> Note: there may be several files in our project which have since been depricated.
