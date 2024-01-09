import { selected_cond_instance } from "../globals.js";

const selected_cond = selected_cond_instance;

export function show_string(array_objs) {
  selected_cond.set_obj_array(array_objs);
  let arr_strings = [];
  for (let i = 0; i < array_objs.length; i++)
    for (const [key, value] of Object.entries(array_objs[i])) {
      arr_strings.push(value);
    }
  return JSON.stringify(arr_strings);
}
