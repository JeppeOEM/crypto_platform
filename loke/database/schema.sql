-- Drop existing tables if they exist
DROP TABLE IF EXISTS strategy_indicators;
DROP TABLE IF EXISTS indicators;
DROP TABLE IF EXISTS strategies;
DROP TABLE IF EXISTS exchanges;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS user;



-- Create the 'user' table
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
);

-- Create the 'post' table
CREATE TABLE post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    body TEXT NOT NULL,
    FOREIGN KEY (author_id) REFERENCES user(id)
);


-- Create the 'strategies' table
CREATE TABLE strategies (
    strategy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    strategy_name TEXT NOT NULL,
    fk_exchange_id INTEGER,
    expression TEXT NOT NULL,
    FOREIGN KEY (fk_exchange_id) REFERENCES exchanges(exchange_id),
);

-- Create the 'indicators' table
CREATE TABLE indicators (
    indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    indicator_name TEXT NOT NULL
);

-- Create the junction table 'strategy_indicators'
CREATE TABLE strategy_indicators (
    strategy_id INTEGER,
    indicator_id INTEGER,
    PRIMARY KEY (strategy_id, indicator_id),
    FOREIGN KEY (strategy_id) REFERENCES strategies(strategy_id),
    FOREIGN KEY (indicator_id) REFERENCES indicators(indicator_id)
);
-- Create the 'exchanges' table
CREATE TABLE exchanges (
    exchange_id INTEGER PRIMARY KEY AUTOINCREMENT,
    exchange_name TEXT NOT NULL
);

