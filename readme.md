## Experimental Cryptocurrency Trading strategy optimizer

Work in progress.

Started out as a small project that grow way to big for vanilla javascript.

Experimenting with using a genetic algorithm to find the best parameters for a trading strategy.

Have been a way for me to learn so needs to be totally refactored, needs mongoDB, UX, TimescaleDB and frontend needs to be rewritten in Typescript.

## Features

Login
Markov Model image generation
Price chart
Backtesting and Genetic Optimization algorithms - not connected to frontend yet
Frontend configurations is saved in Sqlite database

```
flask --app main_app run --debug

```

init database:

```
flask --app main_app init-db
```

INFO:
webpack tutorial:
https://digitalhedgehog.org/articles/how-to-use-flask-with-webpack
