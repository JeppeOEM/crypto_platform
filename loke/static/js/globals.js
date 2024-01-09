class SelectedCond {
  constructor() {
    this._selectedCond;
  }

  get() {
    return this._selectedCond;
  }

  set(value) {
    this._selectedCond = value;
  }
}

// Create an instance of the class
const selected_cond_instance = new SelectedCond();

// Export both the class and its instance
export { selected_cond_instance };
