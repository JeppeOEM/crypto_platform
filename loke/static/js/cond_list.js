"use strict";

class TaskManager {
  constructor(identifier) {
    this.identifier = identifier;
    this.addTaskText = "Add";
    this.updateTaskText = "Update";
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

    this.insertTaskInColumn("Task 1", "done");
  }

  insertTaskInColumn(text, column) {
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

    const columnList = this.TodoContent.querySelector(`.${column}List`);
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
    const currentTask = this.TodoContent.querySelector(".currentTask");
    const txtTask = this.TodoContent.querySelector(".txtTask");
    const newID = parseInt(currentTask.getAttribute("lastid")) + 1;

    txtTask.value = "";
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
    e.stopPropagation();
    const taskHeight = e.target.parentElement.offsetHeight + 10;
    const currentListName = e.target.parentElement.parentElement.id;

    e.target.parentElement.remove();

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
    const taskText = this.TodoContent.querySelector(".txtTask");
    const currentTask = this.TodoContent.querySelector(".currentTask");

    if (taskText.value.trim() === "") {
      taskText.focus();
      return false;
    }

    if (this.TodoContent.querySelector(".btnOk").value === this.addTaskText) {
      this.addTaskToList();
    } else {
      this.updateTask();
    }

    taskText.value = "";
    currentTask.style.display = "none";
  }

  addTaskToList() {
    const task = document.createElement("div");
    const taskText = this.TodoContent.querySelector(".txtTask");
    const currentTask = this.TodoContent.querySelector(".currentTask");
    const newID = parseInt(currentTask.getAttribute("currentid")) + 1;

    task.classList.add("task");
    task.classList.add("toDo");
    task.innerText = taskText.value;
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
    //this.resizeLists();
  }

  updateTask() {
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
      let lol = e.target;
      console.log(lol);
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

    //this.resizeLists();
    // }
  }

  deleteButton() {
    const deleteButton = document.createElement("a");

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

class TaskManagerHandler {
  constructor() {
    this.taskManagers = [];
    //ensure incrementing id
    this.countArray = [];
  }
  count() {
    return this.countArray.length;
  }

  createTaskManager(identifier) {
    this.identifier = identifier;
    console.log(this.identifier);
    const taskManager = new TaskManager(this.identifier);
    this.taskManagers.push(taskManager);
    // just pushing something of no value
    this.countArray.push(0);
    return taskManager;
  }
}

const taskManagerHandler = new TaskManagerHandler();
const taskManager1 = taskManagerHandler.createTaskManager("conditions_interface_buy");
const taskManager2 = taskManagerHandler.createTaskManager("conditions_interface_sell");

document.querySelector("#new_todo_buy").addEventListener("click", () => {
  createList("buy", "conditions_interface_buy");
});

document.querySelector("#new_todo_sell").addEventListener("click", () => {
  createList("sell", "conditions_interface_sell");
});

async function createList(side, element) {
  const newId = await newList();
  console.log(newId);
  const taskManager = taskManagerHandler.createTaskManager(newId);
  async function newList() {
    const cloneContainer = document.querySelector(`.clone_${side}`);
    const clone = cloneContainer.cloneNode(true);

    const elementsToRemove = clone.querySelectorAll(`[taskid]`);
    elementsToRemove.forEach((element) => {
      element.parentNode.removeChild(element);
    });

    const todoContent = clone.querySelector(`.${element}`);
    const newId = "todoContent" + (taskManagerHandler.count() + 1);
    todoContent.classList.add(newId);
    console.log(newId);

    // Create TaskManager after updating the id
    cloneContainer.parentNode.appendChild(clone);
    return newId;
  }
}
