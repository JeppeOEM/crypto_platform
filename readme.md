## Experimental Cryptocurrency Trading strategy optimizer

**Work in progress**. 
**DISCLAIMER: This is a code sketch book where my main goal was to create a flask API that would connect a Genetic Algorithm to a trading strategy and then backtest on old market data.
It ended up including all kind of other things, as Markov Model, Frontend Chart, vanilla Javascript frontend with drang n drop.

The code is NOT clean, and frontend is NOT pretty as it was first an formost a way of rapid prototyping, as i quickly moved from one subject to the next, trying not get lost in details and therefore leaving parts of the code unpolished and unoptimized.
I gained alot of insight in the project that i will bring with me into the new version of the project, that i am embarking on as a semester project.
The new project will include

- Typescript frontend with drag n drop
- MongoDB for making the frontend persistent
- TimescaleDB for working with timeseries data
- .NET for a maintainable OOP backend
- Python microservice for Algorithms/data manipulation

## Features

- Login
- Markov Model image generation
- Price chart
- Backtesting and Genetic Optimization algorithms - not connected to frontend yet
- Frontend configurations is saved in Sqlite database

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
