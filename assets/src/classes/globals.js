import { show_string } from "../functions/show_string.js";
//save the last inserted condition list in the dom

class DraggedCond {
  constructor() {
    this._dragged_cond;
    this._starting_side;
  }

  getKey() {
    return this._dragged_cond;
  }

  setKey(value) {
    this._dragged_cond = value;
  }
  setStartingSide(element) {
    let buy = element.closest(".buy_clones");
    let sell = element.closest(".sell_clones");
    let side;
    if (buy) {
      this._starting_side = "buy";
    }
    if (sell) {
      this._starting_side = "sell";
    }
  }
  getStartingSide() {
    return this._starting_side;
  }
}
const dragged_cond = new DraggedCond();
export { dragged_cond };

class LastCondDom {
  constructor() {
    this._last_cond_dom;
  }

  get() {
    return this._last_cond_dom;
  }

  set(value) {
    this._last_cond_dom = value;
  }
}
const last_cond_dom = new LastCondDom();

export { last_cond_dom };

class SelectedCond {
  constructor() {
    this._cond_id;
    this._cond_string;
    this._cond_obj_array = [];
    this._cond = [];
  }

  get() {
    return this._cond_id;
  }

  set(value) {
    this._cond_id = value;
  }

  get_string() {
    return this._cond_string;
  }

  set_string() {
    this._cond_string = show_string(this._cond);
  }

  get_cond() {
    return this._cond;
  }

  add_cond(value) {
    this._cond.push(value);
  }

  reset_cond() {
    this._cond = [];
  }

  del_last() {
    this._cond.pop();
  }
}

// Create an instance of the class
const selected_cond = new SelectedCond();

// Export both the class and its instance
export { selected_cond };
