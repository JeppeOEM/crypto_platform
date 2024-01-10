CREATE TABLE conditions (
    condition_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fk_user_id INT NOT NULL,
    fk_strategy_id INT NOT NULL,
    fk_buy_list_id INT NOT NULL,
    buy_eval VARCHAR(255),
    optimizer_params VARCHAR(255),
    list_row INT NOT NULL,
    side VARCHAR(4) NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
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