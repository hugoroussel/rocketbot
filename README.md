# rocketbot
Lauzhack 2018 swissquote challenge

## Setup

Make sure you have pipenv and yarn installed.

In one terminal, run the backend:
```
cd bot
./run.sh
```

In the other terminal, run the frontend:
```
cd interface
yarn
yarn start
```

## Start training

Add a data.csv file to the /training folder

In a terminal, go to the root folder of this project then run the command:
```
docker build -t rocketbot
docker run -it --rm rocketbot
```
