DROP TABLE IF EXISTS strategy;
DROP TABLE IF EXISTS indicators;
DROP TABLE IF EXISTS exchanges;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS strategies;
DROP TABLE IF EXISTS strategy_indicators;
DROP TABLE IF EXISTS strategy_indicator_forms;
DROP TABLE IF EXISTS sell_conditions;
DROP TABLE IF EXISTS buy_conditions;
DROP TABLE IF EXISTS conditions;
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
    pair VARCHAR(35) NOT NULL,
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
    chart_info VARCHAR(55) NOT NULL,
    chart_visible TINYINT(1) NOT NULL DEFAULT 1,
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id),
    FOREIGN KEY (fk_user_id) REFERENCES user(id)
);
CREATE INDEX idx_indicator_name ON strategy_indicators(indicator_name);
CREATE TABLE sell_conditions (
    condition_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_user_id INT NOT NULL,
    fk_strategy_id INT NOT NULL,
    fk_list_id INT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    indicator_json VARCHAR(255),
    optimizer_params VARCHAR(255),
    list_row INT NOT NULL,
    FOREIGN KEY (fk_user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id) ON DELETE CASCADE,
    FOREIGN KEY (fk_list_id) REFERENCES sell_condition_lists(list_id) ON DELETE CASCADE
);
CREATE TABLE buy_conditions (
    condition_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_user_id INT NOT NULL,
    fk_strategy_id INT NOT NULL,
    fk_list_id INT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    indicator_json VARCHAR(255),
    optimizer_params VARCHAR(255),
    list_row INT NOT NULL,
    FOREIGN KEY (fk_user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id) ON DELETE CASCADE,
    FOREIGN KEY (fk_list_id) REFERENCES buy_condition_lists(list_id) ON DELETE CASCADE
);
CREATE TABLE sell_condition_lists (
    list_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
WHERE list_id = NEW.list_id;
END;
CREATE TABLE buy_condition_lists (
    list_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
WHERE list_id = NEW.list_id;
END;
CREATE TABLE condition_lists (
    list_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_user_id INT NOT NULL,
    fk_strategy_id INT NOT NULL,
    frontend_id INT,
    side VARCHAR(4) NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (fk_user_id) REFERENCES user(id),
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id)
);
CREATE TRIGGER update_id
AFTER
INSERT ON condition_lists BEGIN
UPDATE condition_lists
SET frontend_id = (
        SELECT COUNT(DISTINCT frontend_id) + 1
        FROM buy_condition_lists
        WHERE fk_strategy_id = NEW.fk_strategy_id
    )
WHERE list_id = NEW.list_id;
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
    fk_list_id INT NOT NULL,
    list_row INT NOT NULL,
    fk_condition_id INT,
    FOREIGN KEY (fk_condition_id) REFERENCES sell_conditions(condition_id) ON DELETE CASCADE,
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id) ON DELETE CASCADE,
    FOREIGN KEY (fk_user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY(fk_list_id) REFERENCES sell_condition_lists(list_id) ON DELETE CASCADE
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
    fk_list_id INT NOT NULL,
    list_row INT NOT NULL,
    fk_condition_id INT,
    FOREIGN KEY (fk_condition_id) REFERENCES buy_conditions(condition_id) ON DELETE CASCADE,
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id) ON DELETE CASCADE,
    FOREIGN KEY (fk_user_id) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY(fk_list_id) REFERENCES buy_condition_lists(list_id) ON DELETE CASCADE
);
CREATE TABLE optimization_results (
    optimization_result_id INTEGER PRIMARY KEY AUTOINCREMENT,
    result TEXT NOT NULL,
    fk_user_id INT NOT NULL,
    fk_strategy_id INT NOT NULL,
    FOREIGN KEY (fk_strategy_id) REFERENCES strategies(strategy_id),
    FOREIGN KEY (fk_user_id) REFERENCES user(id)
);