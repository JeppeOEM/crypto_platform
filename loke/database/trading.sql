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
DROP TABLE IF EXISTS sell_condition_lists;
DROP TABLE IF EXISTS buy_condition_lists;
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
    strategy_indicator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_strategy_id INT NOT NULL,
    fk_user_id INTEGER NOT NULL,
    fk_form_id INTEGER,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    indicator_name VARCHAR(55) NOT NULL,
    settings VARCHAR(255) NOT NULL,
    category VARCHAR(55) NOT NULL,
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id),
    FOREIGN KEY (fk_user_id) REFERENCES user(id)
);
CREATE INDEX idx_indicator_name ON strategy_indicators(indicator_name);
CREATE TABLE sell_conditions (
    sell_conditions_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_user_id INT NOT NULL,
    fk_strategy_id INT NOT NULL,
    fk_sell_list_id INT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    sell_eval VARCHAR(255),
    optimizer_params VARCHAR(255),
    list_row INT NOT NULL,
    FOREIGN KEY (fk_user_id) REFERENCES user(id),
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id)
);
CREATE TABLE buy_conditions (
    buy_conditions_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_user_id INT NOT NULL,
    fk_strategy_id INT NOT NULL,
    fk_buy_list_id INT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    buy_eval VARCHAR(255),
    optimizer_params VARCHAR(255),
    list_row INT NOT NULL,
    FOREIGN KEY (fk_user_id) REFERENCES user(id),
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id)
);
CREATE TABLE sell_list_junction (
    id INTEGER PRIMARY KEY,
    fk_user_id INT NOT NULL,
    fk_strategy_id INT NOT NULL,
    fk_sell_list_id INTEGER,
    fk_sell_conditions_id INTEGER,
    FOREIGN KEY (fk_sell_list_id) REFERENCES sell_condition_lists(sell_list_id),
    FOREIGN KEY (fk_sell_conditions_id) REFERENCES sell_conditions(sell_conditions_id),
    FOREIGN KEY (fk_user_id) REFERENCES user(id),
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id)
);
CREATE TABLE buy_list_junction (
    id INTEGER PRIMARY KEY,
    fk_user_id INT NOT NULL,
    fk_strategy_id INT NOT NULL,
    fk_buy_list_id INTEGER,
    fk_buy_conditions_id INTEGER,
    FOREIGN KEY (fk_buy_list_id) REFERENCES buy_condition_lists(buy_list_id),
    FOREIGN KEY (fk_buy_conditions_id) REFERENCES buy_conditions(buy_conditions_id),
    FOREIGN KEY (fk_user_id) REFERENCES user(id),
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id)
);
CREATE TABLE sell_condition_lists (
    sell_list_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_user_id INT NOT NULL,
    fk_strategy_id INT NOT NULL,
    frontend_id INT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_user_id) REFERENCES user(id),
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id)
);
CREATE TRIGGER update_frontend_id
AFTER
INSERT ON sell_condition_lists BEGIN
UPDATE sell_condition_lists
SET frontend_id = (
        SELECT COUNT(DISTINCT frontend_id) + 1
        FROM sell_condition_lists
        WHERE fk_strategy_id = NEW.fk_strategy_id
    )
WHERE sell_list_id = NEW.sell_list_id;
END;
CREATE TABLE buy_condition_lists (
    buy_list_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_user_id INT NOT NULL,
    fk_strategy_id INT NOT NULL,
    frontend_id INT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_user_id) REFERENCES user(id),
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id)
);
CREATE TRIGGER update_frontend_id_buy
AFTER
INSERT ON buy_condition_lists BEGIN
UPDATE buy_condition_lists
SET frontend_id = (
        SELECT COUNT(DISTINCT frontend_id) + 1
        FROM buy_condition_lists
        WHERE fk_strategy_id = NEW.fk_strategy_id
    )
WHERE buy_list_id = NEW.buy_list_id;
END;
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
CREATE TABLE optimization_results (
    optimization_result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    result TEXT NOT NULL,
    fk_user_id INT NOT NULL,
    fk_strategy_id INT NOT NULL,
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id),
    FOREIGN KEY (fk_user_id) REFERENCES user(id)
);