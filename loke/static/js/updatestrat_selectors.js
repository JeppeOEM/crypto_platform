document.addEventListener("DOMContentLoaded", function () {
  const updateStratText = document.getElementById("update_strat_text");
  updateStratText.innerText = "Edit Name/Info";
  const stratText = document.getElementById("strat_text");
  updateStratText.addEventListener("click", function () {
    console.log("update_strat_text clicked");

    stratText.classList.remove("hidden");
  });
  const saveDb = document.getElementById("save_edit_db");
  saveDb.addEventListener("click", function () {
    stratText.classList.add("hidden");
  });
});
