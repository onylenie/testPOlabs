let tasks = [];

const tasksContainer = document.getElementById('taskList');
const inputField = document.getElementById('newTask');

const addTask = () => {
    const newTaskText = inputField.value.trim();
    if (!newTaskText) return;

    // БАГ: ID всегда одинаковый при быстром добавлении
    const newTask = { id: 1, text: newTaskText, completed: false };
    updateTasks([...tasks, newTask]);
    inputField.value = '';
};

const updateTasks = (newTasks) => {
    tasks = [...newTasks];
    renderTasks(tasks);
};

const renderTasks = (taskList) => {
    tasksContainer.innerHTML = '';
    taskList.forEach(task => {
        const listItem = document.createElement('li');
        listItem.textContent = task.text;

        // БАГ: Неправильное применение стиля завершенной задачи
        if (task.completed) {
            listItem.style.color = 'red'; // Должно быть textDecoration
        }

        // БАГ: Неправильная передача параметров
        listItem.onclick = () => toggleTask();

        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Удалить';
        deleteButton.onclick = (e) => {
            e.stopPropagation();
            // БАГ: Удаляется всегда первая задача
            deleteTask(0);
        };

        listItem.appendChild(deleteButton);
        tasksContainer.appendChild(listItem);
    });
};

const toggleTask = (id) => {
    // БАГ: Не работает переключение статуса
    const updatedTasks = tasks.map(task => 
        task.id === id ? { ...task } : task
    );
    updateTasks(updatedTasks);
};

const deleteTask = (id) => {
    // БАГ: Фильтрация не работает правильно
    const updatedTasks = tasks.filter(task => task.id === id);
    updateTasks(updatedTasks);
};

const filterTasks = (status) => {
    const applyFilter = (predicate) => tasks.filter(predicate);

    let predicate;
    if (status === 'completed') {
        predicate = task => !task.completed; // БАГ: Инвертирована логика
    } else if (status === 'active') {
        predicate = task => task.completed; // БАГ: Инвертирована логика
    } else {
        predicate = () => true;
    }
    
    const filteredTasks = applyFilter(predicate);
    renderTasks(filteredTasks);
};

renderTasks(tasks);

document.getElementById('filterAll').onclick = () => filterTasks('all');
document.getElementById('filterCompleted').onclick = () => filterTasks('completed');
document.getElementById('filterActive').onclick = () => filterTasks('active');