<template>
    <div class="d-flex flex-column align-content-center flex-wrap">
        <h2 class="text-center">Task Tracker</h2>
        <div class="w-50 p-3">
            <label>Task Name</label>
            <input class="form-control" type="text" placeholder="Enter Task Name" v-model="task"/>
            <label>Due Date</label>
            <input class="form-control" type="date" placeholder="Due Date" v-model="due_date"/>
            <label>Priority</label>
            <input class="form-control" type="number" placeholder="Enter Priority" v-model="priority"/>
            <label>Email</label>
            <input class="form-control" type="email" placeholder="Enter Email" v-model="email"/>
        </div>
        <TaskList
            :task="task"
            :due_date="due_date"
            :priority="priority"
            :email="email"
            @clear-form="clearform"
        />
    </div>
</template>
  
<script>

import TaskList from './components/TaskList.vue';

export default {
    data() {
        return {
            task: "",
            due_date:"",
            priority: "",
            email: "",
        }
    },
    methods: {
        clearform() {
            this.task=""
            this.due_date=""
            this.priority=""
            this.email=""
        }
    },
    async mounted() {
    },
    components: {
        TaskList,
        
    }
}
</script>
