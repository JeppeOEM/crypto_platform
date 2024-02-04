"use strict";
import { selected_cond, last_cond_dom, dragged_cond } from "../classes/globals.js";
import { strategyDataInstance } from "../classes/StrategyData.js";
import { save_cond_sell, save_cond_buy } from "./conditions.js";
import { optimizer_params } from "./optimize.js";
import { postJsonGetData, postJsonGetStatus, getJson } from "../functions/fetch.js";
import { build_buttons } from "./build_strategy_page.js";
import { remove_element } from "../functions/remove_element.js";
import { build_conds } from "./conditions.js";

const strategyData = strategyDataInstance;

export class CondController {
  constructor() {
    this.objList = [];
    this.obj = {};
    //ensure incrementing id
    this.countArray = [];
  }
  count() {
    return this.countArray.length;
  }

  createCondManager(identifier, primary_key) {
    this.identifier = identifier;
    this.primary_key = primary_key;

    const taskManager = new CondManager(this.identifier, this.primary_key);
    this.objList.push(taskManager);

    // Assign the TaskManager instance to this.obj using the identifier as the key
    this.obj[this.identifier] = taskManager;

    // just pushing something of no value
    this.countArray.push(0);

    return taskManager;
  }

  addCond(identifier, text, column) {
    this.identifier = identifier;
    this.text = text;
    this.column = column;
    const current_cond_list = this.obj[this.identifier];
    current_cond_list.insert_cond(this.text, this.column);
  }

  getKey(key) {
    const result = [];
    // Lenght here is 0 in the Console

    for (let i = 0; i < this.objList.length; i++) {
      if (this.objList[i].primary_key === key) {
        return this.objList[i];
      }
    }
  }
}
const condListController = new CondController();
export { condListController };

// class CondManager {
//   constructor(identifier, primary_key) {
//     this.primary_key = primary_key;
//     this.identifier = identifier;
//     this.cond = [];
//   }
//   insert_cond(text, column) {
//     this.cond.push({ ind: text, cond: column });
//   }
// }

class CondManager {
  constructor(identifier, primary_key) {
    this.primary_key = primary_key;
    this.identifier = identifier;
    this.addTaskText = "Add";
    this.updateTaskText = "Update";
    //individual box
    this.CondList = document.querySelector(`.${this.identifier}`);
    this.toDoList = this.CondList.querySelector(".toDoList");
    this.draggedTask = {};
    this.toDoListHeight = this.toDoList.offsetHeight;
    this.ongoingListHeight = 0;
    this.doneListHeight = 0;

    document.addEventListener("DOMContentLoaded", () => {
      const currentTask = this.CondList.querySelector(".currentTask");
      currentTask.setAttribute("currentid", "");
      currentTask.setAttribute("lastid", "0");
    });

    this.CondList.querySelector(".addTask").addEventListener("click", () => this.addTask());

    this.CondList.querySelector(".btnOk").addEventListener("click", () => this.handleTaskButton());

    this.CondList.querySelector(".btnCancel").addEventListener("click", () => this.cancelTaskEdition());
    this.CondList.querySelector(".txtCond").addEventListener("keyup", (e) =>
      e.code === "Escape" ? this.cancelTaskEdition() : true
    );

    this.CondList.querySelector(".showHelp").addEventListener("click", () => this.showHelp());

    const btnClose = this.CondList.querySelector(".btnClose");
    btnClose.addEventListener("click", () => this.hideHelp());
    btnClose.addEventListener("keyup", (e) => (e.code === "Escape" ? this.hideHelp() : true));

    // this.CondList.querySelectorAll(".listColumn").forEach((list) => {
    //   list.addEventListener("dragover", (e) => console.log(e.target));
    // });

    this.CondList.querySelectorAll(".listColumn").forEach((list) => {
      list.addEventListener("dragover", (e) => e.preventDefault());
    });

    this.CondList.querySelector(".toDoList").addEventListener("drop", (e) => this.dropCond(e, "toDo"));
    this.CondList.querySelector(".ongoingList").addEventListener("drop", (e) => this.dropCond(e, "ongoing"));
    this.CondList.querySelector(".doneList").addEventListener("drop", (e) => this.dropCond(e, "done"));
  }

  insert_cond(text, column, id, side) {
    const task = document.createElement("div");
    const newID = parseInt(this.CondList.querySelector(".currentTask").getAttribute("lastid")) + 1;

    task.classList.add("single_condition");
    task.classList.add(column);
    task.innerText = text;
    task.setAttribute("frontend_cond_id", newID);
    this.CondList.querySelector(".currentTask").setAttribute("lastid", newID);
    task.addEventListener("click", (e) => this.taskClick(e));
    task.setAttribute("draggable", "true");
    task.addEventListener("dragstart", (e) => this.dragStart(e));
    task.prepend(this.deleteButton());
    task.dataset.cond_key = id;
    const columnList = this.CondList.querySelector(`.${column}List`);
    columnList.prepend(task);

    switch (column) {
      case "toDo":
        this.toDoListHeight += task.offsetHeight + 10;
        break;
      case "ongoing":
        this.ongoingListHeight += task.offsetHeight + 10;
        break;
      case "done":
        this.doneListHeight += task.offsetHeight + 10;
        break;
    }
  }

  addTask() {
    //global variable for the db
    selected_cond.set(parseInt(this.CondList.dataset.primary_key));
    const currentTask = this.CondList.querySelector(".currentTask");
    const txtCond = this.CondList.querySelector(".txtCond");
    const newID = parseInt(currentTask.getAttribute("lastid")) + 1;
    // txtCond.value = "";
    this.CondList.querySelector(".btnOk").value = this.addTaskText;
    currentTask.setAttribute("currentid", newID);
    currentTask.style.display = "block";
    txtCond.focus();
    let saved_data = strategyData.getData();
    saved_data.cols;

    build_buttons(["<", ">", "==", "&", "or"], "compare_btns", "button", "compare_cond");
    build_buttons(["or", "&"], "or_and_btns", "button", "or_and_cond");
    build_buttons(saved_data.cols, "condition_btns", "button", "indicator_cond");
  }

  taskClick(e) {
    const currentTask = this.CondList.querySelector(".currentTask");
    const txtCond = this.CondList.querySelector(".txtCond");
    const ID = parseInt(e.target.getAttribute("frontend_cond_id"));
    this.CondList.querySelector(".btnOk").value = this.updateTaskText;
    txtCond.value = e.target.innerText;
    currentTask.setAttribute("currentid", ID);
    currentTask.style.display = "block";
    txtCond.focus();
  }

  async deleteButtonClick(e) {
    //Make sure that the click event stops here and dont fire anything in the ancestors/descendants
    e.stopPropagation();
    let side;
    if (e.target.closest(".sell_side")) {
      side = "sell";
    } else if (e.target.closest(".buy_side")) {
      side = "buy";
    }
    const taskHeight = e.target.parentElement.offsetHeight + 10;
    const currentListName = e.target.parentElement.parentElement.id;

    e.target.parentElement.remove();

    let data = {
      id: e.target.parentElement.dataset.cond_key,
      side: side,
    };

    switch (currentListName) {
      case "toDoList":
        this.toDoListHeight -= taskHeight;
        break;
      case "ongoingList":
        this.ongoingListHeight -= taskHeight;
        break;
      case "doneList":
        this.doneListHeight -= taskHeight;
        break;
    }

    await postJsonGetStatus(data, "delete_condition");

    console.log(data, "delete button click");
    //load conditions again after deletion
    const json = await getJson("load_conditions");
    console.log(json, "json!!!!!!!!!!!!!!!!");
    const buy_conds = json.buy_conds;
    const sell_conds = json.sell_conds;
    // console.log(this.CondList, "this.CondList");
    remove_element("param");
    optimizer_params(buy_conds, "_BUY", "param_buy");
    optimizer_params(sell_conds, "_SELL", "param_buy");
  }

  handleTaskButton() {
    // const taskText = this.CondList.querySelector(".txtCond");
    const currentTask = this.CondList.querySelector(".currentTask");

    // if (taskText.value.trim() === "") {
    //   taskText.focus();
    //   return false;
    // }
    //check if the button is the add button or the update button

    if (this.CondList.classList.contains("buy_side")) {
      save_cond_buy();
    } else if (this.CondList.classList.contains("sell_side")) {
      save_cond_sell();
    } else {
      console.log("classList not containing buy_side or sell_side");
    }

    if (this.CondList.querySelector(".btnOk").value === this.addTaskText) {
      this.addTaskToList();
    } else {
      this.updateTask();
    }

    // taskText.value = "";
    currentTask.style.display = "none";
  }

  addTaskToList() {
    const task = document.createElement("div");
    last_cond_dom.set(task);

    // const taskText = this.CondList.querySelector(".currentTask.modal");
    const currentTask = this.CondList.querySelector(".currentTask");
    const newID = parseInt(currentTask.getAttribute("currentid")) + 1;

    task.classList.add("single_condition");
    task.classList.add("toDo");
    task.innerText = selected_cond.get_string();
    task.setAttribute("frontend_cond_id", currentTask.getAttribute("currentid"));
    currentTask.setAttribute("lastid", newID);
    task.addEventListener("click", (e) => this.taskClick(e));
    task.setAttribute("draggable", "true");
    task.addEventListener("dragstart", (e) => this.dragStart(e));
    task.addEventListener("drop", (e) => {
      e.preventDefault();
      console.log("hit");
    });
    //Prepend: inserts nodes before first child of node
    task.prepend(this.deleteButton());
    console.log("########################################### task GOOOOOOOOOOOOOO");
    console.log(this.toDoList, "toDoList GOOOOOOOOOOOOOO");
    this.toDoList.prepend(task);
    this.toDoListHeight += task.offsetHeight + 10;

    this.load_opti_params();
  }

  updateTask() {
    selected_cond.reset_cond();
    const taskText = this.CondList.querySelector(".txtCond");
    const currentTask = this.CondList.querySelector(".currentTask");
    const task = this.CondList.querySelector(
      'div.task[frontend_cond_id="' + currentTask.getAttribute("currentid") + '"]'
    );
    const previousHeight = task.offsetHeight;
    const currentListName = task.parentNode.id;

    task.innerText = taskText.value;
    task.prepend(this.deleteButton());

    switch (currentListName) {
      case "toDoList":
        this.toDoListHeight = this.toDoListHeight - previousHeight + task.offsetHeight;
        break;
      case "ongoingList":
        this.ongoingListHeight = this.ongoingListHeight - previousHeight + task.offsetHeight;
        break;
      case "doneList":
        this.doneListHeight = this.doneListHeight - previousHeight + task.offsetHeight;
    }

    this.load_opti_params();
    //this.resizeLists();
  }

  cancelTaskEdition() {
    const currentTask = this.CondList.querySelector(".currentTask");
    currentTask.setAttribute("currentid", "0");
    currentTask.style.display = "none";
  }

  showHelp() {
    this.CondList.querySelector(".help").style.display = "block";
    this.CondList.querySelector(".btnClose").focus();
  }

  hideHelp() {
    this.CondList.querySelector(".help").style.display = "none";
  }

  async load_opti_params() {
    const json = await getJson("load_conditions");
    const buy_conds = json.buy_conds;
    const sell_conds = json.sell_conds;
    remove_element("param");
    optimizer_params(buy_conds, "_BUY", "param_buy");
    optimizer_params(sell_conds, "_SELL", "param_buy");
  }

  swapElements(element1, element2) {
    // Create a placeholder element
    const temp = document.createElement("div");

    // Swap the classNames of element1 and element2
    const tempClassName = element1.className;
    element1.className = element2.className;
    element2.className = tempClassName;

    // Insert the placeholder before element1
    element1.parentNode.insertBefore(temp, element1);

    // Move element2 to the position of element1
    element2.parentNode.insertBefore(element1, element2);

    // Move element1 to the position of element2
    temp.parentNode.insertBefore(element2, temp);

    // Remove the placeholder
    temp.parentNode.removeChild(temp);
    console.log(element1, element2);
    this.load_opti_params();
  }

  dragStart(e) {
    e.dataTransfer.setData("text/plain", null);
    this.draggedTask = e.target;
    dragged_cond.setKey(this.draggedTask.dataset.cond_key);
    dragged_cond.setStartingSide(this.draggedTask);
    console.log(this.draggedTask);
    console.log("Drag started", this.draggedTask.classList);
  }

  dropDiffrentList(e) {
    console.log("diffrent");
    console.log(dragged_cond.getKey());
    console.log(dragged_cond.getStartingSide(), "STAAAAAAAAAAAAAAAAAAAAAAAAART");

    const destinationElement = e.target;
    let row = destinationElement.classList;
    console.log(destinationElement);
    let destination_list = destinationElement.closest(".single_list");
    console.log("destination primary", destination_list.dataset.primary_key);
    console.log(row[0]);
    let buy = destinationElement.closest(".buy_clones");
    let sell = destinationElement.closest(".sell_clones");
    let side;
    let starting_side = dragged_cond.getStartingSide();
    if (buy) {
      side = "buy";
    }
    if (sell) {
      side = "sell";
    }

    let data = {
      fk_list_id: destination_list.dataset.primary_key,
      list_row: which_list(row[0]), //first classname of the classList is what we are after
      id: dragged_cond.getKey(),
      //destination side
      side,
      starting_side,
    };
    console.log(data);

    this.update_cond(data);
  }

  dropCond(e, listName) {
    let current_cond_list;
    let draggedTask = this.draggedTask;
    console.log(draggedTask, "draggedTask");
    // check if draggedTask is empty, if it is empty, then another condition list is hit
    if (Object.keys(this.draggedTask).length === 0) {
      return this.dropDiffrentList(e);
    }

    try {
      current_cond_list = draggedTask.parentNode.id;
    } catch {
      console.log("catch Activated");
      console.log(this.draggedTask);
    }

    const destinationElement = e.target;
    console.log(destinationElement.classList);
    let destination_list = destinationElement.closest(".single_list");
    console.log(destination_list.dataset.primary_key);
    //get the frontend_cond_id of the element where the task was dropped, if it is a task
    const dropped_frontend_cond_id = destinationElement.getAttribute("frontend_cond_id");
    if (dropped_frontend_cond_id) {
      // const dragged_frontend_cond_id = draggedTask.getAttribute("frontend_cond_id");
      // const element1 = document.querySelector(`.task[frontend_cond_id="${dragged_frontend_cond_id}"]`);
      // const element2 = document.querySelector(`.task[frontend_cond_id="${dropped_frontend_cond_id}"]`);
      // console.log(element1, element2);
      console.log(draggedTask, destinationElement);
      this.swapElements(draggedTask, destinationElement);
    }
    //check if the the listName already matches the class stored in the element
    // if (current_cond_list !== listName + "List") {
    const taskHeight = draggedTask.offsetHeight + 10;

    console.log(draggedTask, "hiiiiiiiiiit");
    draggedTask.parentNode.removeChild(draggedTask);

    switch (listName) {
      case "toDo":
        this.toDoListHeight -= taskHeight;
        break;
      case "ongoing":
        this.ongoingListHeight -= taskHeight;
        break;
      case "done":
        this.doneListHeight -= taskHeight;
        break;
    }

    draggedTask.classList.remove("toDo", "ongoing", "done");
    draggedTask.classList.add(listName);

    // Dynamically select the correct list based on listName
    // const destinationList = this.CondList.querySelector(`.${listName}List`);
    // console.log(destinationList);
    // destinationList.appendChild(draggedTask);

    switch (listName) {
      case "toDo":
        this.toDoListHeight += taskHeight;
        break;
      case "ongoing":
        this.ongoingListHeight += taskHeight;
        break;
      case "done":
        this.doneListHeight += taskHeight;
        break;
    }

    let buy = draggedTask.closest(".buy_clones");
    let sell = draggedTask.closest(".sell_clones");
    let side;
    if (buy) {
      side = "buy";
    }
    if (sell) {
      side = "sell";
    }

    const data = {
      id: draggedTask.dataset.cond_key,
      list_row: which_row_string(listName),
      side,
    };

    this.update_cond(data);

    // console.log(response);
    //this.resizeLists();
    // }
    // this.load_opti_params();
  }
  async update_cond(data) {
    await postJsonGetData(data, "update_condition_row");
    console.log(data);
    const json = await getJson("load_conditions");
    console.log(json, "json!!!!!!!!!!!!!!!!");
    // const buy_conds = json.buy_conds;
    // const sell_conds = json.sell_conds;
    // console.log(this.CondList, "this.CondList");
    let elements = document.querySelectorAll(`.param`);
    console.log(elements, "elements");
    elements.forEach(function (ele) {
      ele.parentNode.removeChild(ele);
    });
    // optimizer_params(buy_conds, "_BUY", "param_buy");
    // optimizer_params(sell_conds, "_SELL", "param_buy");

    build_conds();
  }

  deleteButton() {
    const deleteButton = document.createElement("a");
    deleteButton.innerText = "🗑️";
    deleteButton.classList.add("deleteButton");
    deleteButton.addEventListener("click", (e) => this.deleteButtonClick(e));

    return deleteButton;
  }

  // resizeLists() {
  //   const higherListHeight = Math.max(this.toDoListHeight, this.ongoingListHeight, this.doneListHeight);

  //   this.CondList.querySelectorAll(".listColumn").forEach((list) => {
  //     list.style.height = higherListHeight + "px";
  //   });

  //   this.CondList.querySelector(".listContent").style.height = higherListHeight + 20 + "px";
  // }
}

// const condListController = new CondController();
// const taskManager1 = condListController.createCondManager("buy_cond_list1");
// const taskManager2 = condListController.createCondManager("sell_cond_list2");

// document.querySelector("#new_todo_buy").addEventListener("click", () => {
//   createList("buy", "insert_here");
// });

// document.querySelector("#new_todo_sell").addEventListener("click", () => {
//   createList("sell", "insert_here");
// });

// async function createList(side, element) {
//   const newId = await newList();
//   console.log(newId);
//   condListController.createCondManager(newId);

//   async function newList() {
//     const cloneContainer = document.querySelector(`.clone_template`);
//     const append_here = document.querySelector(`${side}_clones`);
//     console.log(cloneContainer, "clone_container");
//     const clone = cloneContainer.cloneNode(true);

//     // const elementsToRemove = clone.querySelectorAll(`[frontend_cond_id]`);
//     // elementsToRemove.forEach((element) => {
//     //   element.parentNode.removeChild(element);
//     // });

//     const cond_list_content = clone.querySelector(`.${element}`);

//     console.log(cond_list_content, "cond_list");
//     const newId = side + "_cond_list" + (condListController.count() + 1);
//     cond_list_content.classList.add(newId);
//     console.log(newId);

//     // Create TaskManager after updating the id
//     append_here.appendChild(clone);
//     return newId;
//   }
// }

// document.getElementById("toggleButton").addEventListener("click", toggleConditions);

function toggleConditions() {
  const buyToggle = document.querySelector(".buy_toggle");
  const sellToggle = document.querySelector(".sell_toggle");

  const button = document.getElementById("toggleButton");

  if (buyToggle.classList.contains("hidden")) {
    button.innerText = "Hide Sell Conditions";
    buyToggle.classList.remove("hidden");
    buyToggle.classList.add("block");
    sellToggle.classList.remove("block");
    sellToggle.classList.add("hidden");
  } else {
    button.innerText = "Hide Buy Conditions";
    buyToggle.classList.remove("block");
    buyToggle.classList.add("hidden");
    sellToggle.classList.remove("hidden");
    sellToggle.classList.add("block");
  }
}
function which_row_string(string) {
  switch (string) {
    case "toDo":
      return 1;
    case "ongoing":
      return 2;
    case "done":
      return 3;
  }
}
function which_list(string) {
  switch (string) {
    case "toDoList":
      return 1;
    case "ongoingList":
      return 2;
    case "doneList":
      return 3;
  }
}
