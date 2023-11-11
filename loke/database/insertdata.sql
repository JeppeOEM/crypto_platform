PRAGMA foreign_keys = ON;
INSERT INTO exchanges (exchange_id, exchange_name)
VALUES (1, 'binance'),
    (2, 'huobi'),
    (3, 'bybit');
INSERT INTO user (id, username, password)
VALUES (1, 'x', "x");
INSERT INTO strategies (
        strategy_id,
        fk_user_id,
        strategy_name,
        fk_exchange_id
    )
VALUES (1, 1, "test", 1);