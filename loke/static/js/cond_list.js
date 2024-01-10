"use strict";
import { selected_cond_instance } from "./globals.js";
import { save_cond_buy } from "./conditions.js";
import { save_cond_sell } from "./conditions.js";
import { last_cond_dom } from "./globals.js";
import { optimizer_params } from "./conditions.js";
import { postJsonGetData, postJsonGetStatus, getJson } from "./fetch.js";
const selected_cond = selected_cond_instance;

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
    console.log(this.primary_key, "primary_key!!!!!!!");

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
    console.log(key, "key");
    const result = [];
    for (let i = 0; i < this.objList.length; i++) {
      if (this.objList[i].primary_key === key) {
        return this.objList[i];
      }
    }

    console.log(result);
    // let arr = this.objList.forEach((obj) => {
    //   if (obj.primary_key === key) {
    //     return obj;
    //   }
    // });
  }
}
const condController = new CondController();
export { condController };
class CondManager {
  constructor(identifier, primary_key) {
    this.primary_key = primary_key;
    console.log(this.primary_key, "primary_key COND CONTROl");
    this.identifier = identifier;
    this.addTaskText = "Add";
    this.updateTaskText = "Update";
    //individual box
    this.TodoContent = document.querySelector(`.${this.identifier}`);
    this.toDoList = this.TodoContent.querySelector(".toDoList");
    this.draggedTask = {};
    this.toDoListHeight = this.toDoList.offsetHeight;
    this.ongoingListHeight = 0;
    this.doneListHeight = 0;

    document.addEventListener("DOMContentLoaded", () => {
      const currentTask = this.TodoContent.querySelector(".currentTask");
      currentTask.setAttribute("currentid", "");
      currentTask.setAttribute("lastid", "0");
    });

    this.TodoContent.querySelector(".addTask").addEventListener("click", () => this.addTask());

    this.TodoContent.querySelector(".btnOk").addEventListener("click", () => this.handleTaskButton());

    this.TodoContent.querySelector(".btnCancel").addEventListener("click", () => this.cancelTaskEdition());
    this.TodoContent.querySelector(".txtTask").addEventListener("keyup", (e) =>
      e.code === "Escape" ? this.cancelTaskEdition() : true
    );

    this.TodoContent.querySelector(".showHelp").addEventListener("click", () => this.showHelp());

    const btnClose = this.TodoContent.querySelector(".btnClose");
    btnClose.addEventListener("click", () => this.hideHelp());
    btnClose.addEventListener("keyup", (e) => (e.code === "Escape" ? this.hideHelp() : true));

    // this.TodoContent.querySelectorAll(".listColumn").forEach((list) => {
    //   list.addEventListener("dragover", (e) => console.log(e.target));
    // });

    this.TodoContent.querySelectorAll(".listColumn").forEach((list) => {
      list.addEventListener("dragover", (e) => e.preventDefault());
    });

    this.TodoContent.querySelector(".toDoList").addEventListener("drop", (e) => this.dropTask(e, "toDo"));
    this.TodoContent.querySelector(".ongoingList").addEventListener("drop", (e) => this.dropTask(e, "ongoing"));
    this.TodoContent.querySelector(".doneList").addEventListener("drop", (e) => this.dropTask(e, "done"));
  }

  insert_cond(text, column, id) {
    const task = document.createElement("div");
    const newID = parseInt(this.TodoContent.querySelector(".currentTask").getAttribute("lastid")) + 1;

    task.classList.add("task");
    task.classList.add(column);
    task.innerText = text;
    task.setAttribute("taskId", newID);
    this.TodoContent.querySelector(".currentTask").setAttribute("lastid", newID);
    task.addEventListener("click", (e) => this.taskClick(e));
    task.setAttribute("draggable", "true");
    task.addEventListener("dragstart", (e) => this.dragStart(e));
    task.prepend(this.deleteButton());
    task.dataset.cond_key = id;
    const columnList = this.TodoContent.querySelector(`.${column}List`);
    console.log(columnList, "columnList", task);
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
    selected_cond.set(parseInt(this.TodoContent.dataset.primary_key));
    console.log(selected_cond.get, "selected_cond");
    console.log(selected_cond, "selected_cond");
    const currentTask = this.TodoContent.querySelector(".currentTask");
    const txtTask = this.TodoContent.querySelector(".txtTask");
    const newID = parseInt(currentTask.getAttribute("lastid")) + 1;
    // txtTask.value = "";
    this.TodoContent.querySelector(".btnOk").value = this.addTaskText;
    currentTask.setAttribute("currentid", newID);
    currentTask.style.display = "block";
    txtTask.focus();
  }

  taskClick(e) {
    const currentTask = this.TodoContent.querySelector(".currentTask");
    const txtTask = this.TodoContent.querySelector(".txtTask");
    const ID = parseInt(e.target.getAttribute("taskId"));

    this.TodoContent.querySelector(".btnOk").value = this.updateTaskText;
    txtTask.value = e.target.innerText;
    currentTask.setAttribute("currentid", ID);
    currentTask.style.display = "block";
    txtTask.focus();
  }

  deleteButtonClick(e) {
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

    postJsonGetStatus(data, "delete_condition");

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
    //this.resizeLists();
  }

  handleTaskButton() {
    // const taskText = this.TodoContent.querySelector(".txtTask");
    const currentTask = this.TodoContent.querySelector(".currentTask");

    // if (taskText.value.trim() === "") {
    //   taskText.focus();
    //   return false;
    // }
    //check if the button is the add button or the update button

    if (this.TodoContent.classList.contains("buy_side")) {
      save_cond_buy();
    } else if (this.TodoContent.classList.contains("sell_side")) {
      save_cond_sell();
    } else {
      console.log("classList not containing buy_side or sell_side");
    }

    if (this.TodoContent.querySelector(".btnOk").value === this.addTaskText) {
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

    // const taskText = this.TodoContent.querySelector(".currentTask.modal");
    const currentTask = this.TodoContent.querySelector(".currentTask");
    const newID = parseInt(currentTask.getAttribute("currentid")) + 1;

    task.classList.add("task");
    task.classList.add("toDo");
    console.log(selected_cond.get_string());
    task.innerText = selected_cond.get_string();
    task.setAttribute("taskId", currentTask.getAttribute("currentid"));
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

    this.toDoList.prepend(task);
    this.toDoListHeight += task.offsetHeight + 10;

    this.load_opti_params();
  }

  updateTask() {
    selected_cond.reset_cond();
    const taskText = this.TodoContent.querySelector(".txtTask");
    const currentTask = this.TodoContent.querySelector(".currentTask");
    const task = this.TodoContent.querySelector('div.task[taskid="' + currentTask.getAttribute("currentid") + '"]');
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
    const currentTask = this.TodoContent.querySelector(".currentTask");
    currentTask.setAttribute("currentid", "0");
    currentTask.style.display = "none";
  }

  showHelp() {
    this.TodoContent.querySelector(".help").style.display = "block";
    this.TodoContent.querySelector(".btnClose").focus();
  }

  hideHelp() {
    this.TodoContent.querySelector(".help").style.display = "none";
  }

  async load_opti_params() {
    const json = await getJson("load_conditions");
    const buy_conds = json.buy_conds;
    const sell_conds = json.sell_conds;
    // optimizer_params(sell_conds, "_SELL", "param_sell");
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
  }

  dragStart(e) {
    e.dataTransfer.setData("text/plain", null);
    this.draggedTask = e.target;
    console.log(this.draggedTask);
    console.log("Drag started");
  }

  dropTask(e, listName) {
    let taskList;
    let draggedTask = this.draggedTask;

    try {
      taskList = draggedTask.parentNode.id;
    } catch {
      let lol = e.targwet;
      console.log(lol, "lol!!!!!!!!!!!!!!!!!!");
      console.log(this.draggedTask);
    }

    // console.log(taskList, "tasklist");
    const destinationElement = e.target;
    //get the taskid of the element where the task was dropped, if it is a task
    const dropped_taskid = destinationElement.getAttribute("taskid");
    if (dropped_taskid) {
      // const dragged_taskid = draggedTask.getAttribute("taskid");
      // const element1 = document.querySelector(`.task[taskid="${dragged_taskid}"]`);
      // const element2 = document.querySelector(`.task[taskid="${dropped_taskid}"]`);
      // console.log(element1, element2);
      console.log(draggedTask, destinationElement);
      this.swapElements(draggedTask, destinationElement);
    }
    //check if the the listName already matches the class stored in the element
    // if (taskList !== listName + "List") {
    console.log("task list hit hit");
    const taskHeight = draggedTask.offsetHeight + 10;

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
    const destinationList = this.TodoContent.querySelector(`.${listName}List`);
    destinationList.appendChild(draggedTask);

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
    console.log(listName);
    const data = {
      id: draggedTask.dataset.cond_key,
      list_row: which_row_string(listName),
      side: "buy",
    };

    update_cond(data);

    async function update_cond(data) {
      await postJsonGetData(data, "update_condition_row");
      console.log(data);
    }
    // console.log(response);
    //this.resizeLists();
    // }
  }

  deleteButton() {
    const deleteButton = document.createElement("a");
    deleteButton.innerText = "🗑️";
    deleteButton.classList.add("deleteButton");
    deleteButton.addEventListener("click", (e) => this.deleteButtonClick(e));

    return deleteButton;
  }

  insertTask() {}

  // resizeLists() {
  //   const higherListHeight = Math.max(this.toDoListHeight, this.ongoingListHeight, this.doneListHeight);

  //   this.TodoContent.querySelectorAll(".listColumn").forEach((list) => {
  //     list.style.height = higherListHeight + "px";
  //   });

  //   this.TodoContent.querySelector(".listContent").style.height = higherListHeight + 20 + "px";
  // }
}

// const condController = new CondController();
// const taskManager1 = condController.createCondManager("buy_cond_list1");
// const taskManager2 = condController.createCondManager("sell_cond_list2");

// document.querySelector("#new_todo_buy").addEventListener("click", () => {
//   createList("buy", "insert_here");
// });

// document.querySelector("#new_todo_sell").addEventListener("click", () => {
//   createList("sell", "insert_here");
// });

// async function createList(side, element) {
//   const newId = await newList();
//   console.log(newId);
//   condController.createCondManager(newId);

//   async function newList() {
//     const cloneContainer = document.querySelector(`.clone_template`);
//     const append_here = document.querySelector(`${side}_clones`);
//     console.log(cloneContainer, "clone_container");
//     const clone = cloneContainer.cloneNode(true);

//     // const elementsToRemove = clone.querySelectorAll(`[taskid]`);
//     // elementsToRemove.forEach((element) => {
//     //   element.parentNode.removeChild(element);
//     // });

//     const cond_list_content = clone.querySelector(`.${element}`);

//     console.log(cond_list_content, "cond_list");
//     const newId = side + "_cond_list" + (condController.count() + 1);
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
