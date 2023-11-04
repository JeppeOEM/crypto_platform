DROP TABLE IF EXISTS strategy;
DROP TABLE IF EXISTS indicators;
DROP TABLE IF EXISTS exchanges;

CREATE TABLE strategies (
    strategy_id INT PRIMARY KEY,
    strategy_name VARCHAR(255) NOT NULL,
    exchange_id INT,
    FOREIGN KEY (exchange_id) REFERENCES exchanges(exchange_id)
);

-- Create the 'indicators' table
CREATE TABLE indicators (
    indicator_id INT PRIMARY KEY,
    indicator_name VARCHAR(255) NOT NULL
);

-- Create the 'exchanges' table
CREATE TABLE exchanges (
    exchange_id INT PRIMARY KEY,
    exchange_name VARCHAR(255) NOT NULL
);

-- Create the junction table 'strategy_indicators'
CREATE TABLE strategy_indicators (
    strategy_id INT,
    indicator_id INT,
    PRIMARY KEY (strategy_id, indicator_id),
    FOREIGN KEY (strategy_id) REFERENCES strategies(strategy_id),
    FOREIGN KEY (indicator_id) REFERENCES indicators(indicator_id)
);