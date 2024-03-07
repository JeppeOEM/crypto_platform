def chart_settings(indi):
    if indi == "rsi":
        return {"type": "line_add_pane"}
    elif indi == "ao":
        return {"type": "line_add_pane"}
    elif indi == "adx":
        return {"type": "line_add_pane"}
