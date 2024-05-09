function fetchTasks() {
  fetch("http://localhost:9999/get_tasks")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((tasks) => {
      const taskList = document.getElementById("tasks");
      taskList.innerHTML = "";

      tasks.forEach((task) => {
        const listItem = document.createElement("li");
        listItem.textContent = task.description;

        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "Delete";
        deleteBtn.dataset.taskId = task.id;
        deleteBtn.onclick = () => deleteTask(deleteBtn.dataset.taskId);

        listItem.appendChild(deleteBtn);
        taskList.appendChild(listItem);
      });
    })
    .catch((error) => {
      console.error("There was a problem with the fetch operation:", error);
    });
}
document.addEventListener("DOMContentLoaded", function () {
  fetchTasks();
});

function addTask() {
  const newTaskInput = document.getElementById("new-task-input");
  const newTaskDescription = newTaskInput.value.trim();

  if (newTaskDescription === "") {
    alert("Please enter a task description.");
    return;
  }

  const formData = new URLSearchParams();
  formData.append("description", newTaskDescription);

  fetch("/add", {
    method: "POST", 
    headers: {
      "Content-Type": "application/x-www-form-urlencoded", 
    },
    body: formData, 
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json(); 
    })
    .then((data) => {
      console.log("Task added:", data);
      fetchTasks(); // 
    })
    .catch((error) => {
      console.error("Error:", error);
    });

  newTaskInput.value = "";
}

function deleteTask(taskId) {
  fetch(`/delete/${taskId}`, {
    method: "DELETE",
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    })
    .then((data) => {
      console.log("Task deleted:", data);
      fetchTasks(); 
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

document.addEventListener("DOMContentLoaded", function () {
  document.querySelector(".new-task button").onclick = addTask;

  fetchTasks();
});
