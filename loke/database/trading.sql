DROP TABLE IF EXISTS strategy;
DROP TABLE IF EXISTS indicators;
DROP TABLE IF EXISTS exchanges;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS strategies;
DROP TABLE IF EXISTS strategy_indicators;
DROP TABLE IF EXISTS strategy_indicator_forms;
DROP TABLE IF EXISTS sell_conditions;
DROP TABLE IF EXISTS buy_conditions;
DROP TABLE IF EXISTS backtest;
DROP TABLE IF EXISTS sell_optimization;
DROP TABLE IF EXISTS buy_optimization;
PRAGMA foreign_keys = ON;
-- Create the 'user' table
CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT
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
    fk_exchange_id INTEGER NOT NULL DEFAULT 1,
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
CREATE TABLE strategy_indicator_forms (
    form_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_strategy_id INT NOT NULL,
    fk_user_id INTEGER NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE strategy_indicators (
    fk_strategy_id INT NOT NULL,
    fk_user_id INTEGER NOT NULL,
    fk_form_id INTEGER,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    indicator_name VARCHAR(55) NOT NULL,
    settings VARCHAR(255) NOT NULL,
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id),
    FOREIGN KEY (fk_user_id) REFERENCES user(id)
);
CREATE INDEX idx_indicator_name ON strategy_indicators(indicator_name);
CREATE TABLE sell_conditions (
    sell_conditions_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_user_id INT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fk_strategy_id INT NOT NULL,
    sell_eval VARCHAR(255),
    optimizer_params VARCHAR(255),
    FOREIGN KEY (fk_user_id) REFERENCES users(user_id),
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id)
);
CREATE TABLE buy_conditions (
    buy_conditions_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_user_id INT NOT NULL,
    fk_strategy_id INT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    buy_eval VARCHAR(255),
    optimizer_params VARCHAR(255),
    FOREIGN KEY (fk_user_id) REFERENCES users(user_id),
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id)
);
CREATE TABLE backtest (
    backtest_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_user_id INT NOT NULL,
    fk_strategy_id INT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    pnl FLOAT NOT NULL,
    drawdown FLOAT,
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id),
    FOREIGN KEY (fk_user_id) REFERENCES user(id)
);
CREATE TABLE sell_optimization (
    sell_optimization_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_user_id INT NOT NULL,
    fk_strategy_id INT,
    optimization_name VARCHAR(55) NOT NULL,
    class VARCHAR(55) NOT NULL,
    operator VARCHAR(2) NOT NULL,
    data_type VARCHAR(5) NOT NULL,
    optimization_min FLOAT NOT NULL,
    optimization_max FLOAT NOT NULL,
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id),
    FOREIGN KEY (fk_user_id) REFERENCES user(id)
);
CREATE TABLE buy_optimization (
    buy_optimization_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_user_id INT NOT NULL,
    fk_strategy_id INT,
    optimization_name VARCHAR(55) NOT NULL,
    class VARCHAR(55) NOT NULL,
    operator VARCHAR(2) NOT NULL,
    data_type VARCHAR(5) NOT NULL,
    optimization_min FLOAT NOT NULL,
    optimization_max FLOAT NOT NULL,
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id),
    FOREIGN KEY (fk_user_id) REFERENCES user(id)
);