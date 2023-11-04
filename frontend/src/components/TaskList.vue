<template>
  <button @click="submit" class="btn btn-primary">
      Submit
  </button>

  <div>
    <ul>
      <div v-for="task in tasks" :key="task.id" class="border border-dark p-3 m-3">
        <h4>Task: {{ task.title }}</h4>
        <p>Priority: {{ task.priority }}</p>
        <p>Due: {{ task.due_date }}</p>
        <p>Belongs to: {{ task.email }}</p>
        <button @click="editTask(task)" class="btn btn-primary">Edit</button>
        <button @click="deleteTask(task.id)" class="btn btn-primary">Delete</button>
      </div>
    </ul>

    <div v-if="editingTask">
      <h3>Edit Task</h3>
      <form @submit.prevent="updateTask">
        <label for="editTitle">Title:</label>
        <input type="text" id="editTitle" v-model="editedTask.title" required>
        <label for="editPriority">Priority:</label>
        <input type="number" id="editPriority" v-model="editedTask.priority" required>
        <label for="editDueDate">Due Date:</label>
        <input type="date" id="editDueDate" v-model="editedTask.due_date" required>
        <label for="editEmail">Email:</label>
        <input type="email" id="editEmail" v-model="editedTask.email" required>
        <button type="submit">Save</button>
        <button @click="cancelEdit">Cancel</button>
      </form>
    </div>
  </div>

</template>

<script>
export default {
  emits: ['clear-form'],
  data() {
    return {
      tasks: [], // Initialize tasks as an empty array
      editingTask: null,
      editedTask: {
        title: '',
        priority: 0,
        due_date: '',
        email: '',
      },
    };
  },
  mounted() {
    this.fetchData(); // Fetch data when the component is created
  },
  props: ['task','due_date', 'priority','email'],
  methods: {
    submit() {

      const newData= {
          title: this.task,
          due_date: this.due_date,
          priority: this.priority,
          email: this.email,
      };

      fetch("http://localhost:8000/api/tasks/", {
        method: "POST",
        headers:{
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newData),
      })
      .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
      })
      .then((data) => {
        this.tasks.push(data); // Push the new task data to the tasks array
        this.fetchData();
      })
      .catch((error) => {
        console.error('Error posting data:', error);
      });

      this.$emit('clear-form');
      
    },
    fetchData() {
      fetch("http://127.0.0.1:8000/api/tasks/")
        .then((response) => response.json())
        .then((data) => {
          console.log(data)
          this.tasks = data; // Update the tasks data with the fetched data
        })
        .catch((error) => {
          console.error("Error fetching data:", error);
        });
    },
    editTask(task) {
      this.editingTask = task;
      this.editedTask = { ...task }; // Create a copy of the task to edit
    },
    updateTask() {
      // Send a PUT request to update the task on the server
      const taskId = this.editingTask.id;
      fetch(`http://127.0.0.1:8000/api/tasks/${taskId}/`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(this.editedTask),
      })
        .then((response) => response.json())
        .then(() => {
          // Update the local data with the edited task
          const taskIndex = this.tasks.findIndex((task) => task.id === taskId);
          if (taskIndex !== -1) {
            this.tasks[taskIndex] = this.editedTask;
          }
          this.cancelEdit();
        })
        .catch((error) => {
          console.error("Error updating task:", error);
        });
    },
    cancelEdit() {
      this.editingTask = null;
      this.editedTask = {
        title: '',
        priority: 0,
        due_date: '',
        email: '',
      };
    },
    deleteTask(taskId) {
      fetch(`http://127.0.0.1:8000/api/tasks/${taskId}/`, {
        method: "DELETE",
      })
      .then((response) => {
        
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.text();
      
      })
      .then((data) => {
        this.tasks.push(data);
        this.fetchData();
      })
      .catch((error) => {
        console.error("Error deleting task:", error);
      });
    }
  },
}
</script>