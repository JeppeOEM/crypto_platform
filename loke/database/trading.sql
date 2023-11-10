DROP TABLE IF EXISTS strategy;
DROP TABLE IF EXISTS indicators;
DROP TABLE IF EXISTS exchanges;
DROP TABLE IF EXISTS user;
PRAGMA foreign_keys = ON;
-- Create the 'user' table
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
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
-- Create the 'exchanges' table
CREATE TABLE exchanges (
    exchange_id INT PRIMARY KEY,
    exchange_name VARCHAR(255) NOT NULL
);
CREATE TABLE strategies (
    strategy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fk_user_id INTEGER NOT NULL,
    strategy_name TEXT NOT NULL,
    fk_exchange_id INTEGER,
    info TEXT,
    expression TEXT,
    FOREIGN KEY (fk_exchange_id) REFERENCES exchanges(exchange_id),
    FOREIGN KEY (fk_user_id) REFERENCES user(id)
);
-- Create the 'indicators' table
CREATE TABLE indicators (
    indicator_id INT PRIMARY KEY,
    indicator_name VARCHAR(255) NOT NULL
);
-- Create the junction table 'strategy_indicators'
CREATE TABLE strategy_indicators (
    fk_strategy_id INT,
    fk_user_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    indicator_name VARCHAR(55) NOT NULL,
    settings VARCHAR(255) NOT NULL,
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id),
    FOREIGN KEY (fk_user_id) REFERENCES user(id)
);
CREATE TABLE sell_conditions (
    fk_user_id INT,
    fk_strategy_id INT,
    sell_eval VARCHAR(255),
    optimizer_params VARCHAR(255),
    FOREIGN KEY (fk_user_id) REFERENCES users(user_id),
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id)
);
CREATE TABLE buy_conditions (
    fk_user_id INT,
    fk_strategy_id INT,
    buy_eval VARCHAR(255),
    optimizer_params VARCHAR(255),
    FOREIGN KEY (fk_user_id) REFERENCES users(user_id),
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id)
);
CREATE TABLE backtest (
    fk_user_id INT,
    fk_strategy_id INT,
    result VARCHAR(255) FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id),
    FOREIGN KEY (fk_user_id) REFERENCES user(id)
);