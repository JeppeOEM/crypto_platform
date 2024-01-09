class SelectedCond {
  constructor() {
    this._cond_id;
    this._cond_string;
    this._cond_obj_array = [];
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

  set_string(value) {
    this._cond_string = value;
  }

  get_obj_array() {
    return this._cond_obj_array;
  }

  set_obj_array(value) {
    this._cond_obj_array = value;
  }
}

// Create an instance of the class
const selected_cond_instance = new SelectedCond();

// Export both the class and its instance
export { selected_cond_instance };
