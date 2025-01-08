import fs from 'fs-extra';
import path from 'path';

interface Task {
  id: number;
  text: string;
  summary: string | null;
  lang: string; //Adicionando campo para idioma
}

export class TasksRepository {
  private tasks: Task[] = [];
  private currentId: number = 1;
  private tasksFilePath: string;

  constructor() {
    this.tasksFilePath = path.join(__dirname, '...', 'data', 'tasks.json'); // Caminho do arquivo de pesistência

    this.loadTasksFromFile();
  }

  private loadTasksFromFile(): void {
    if (fs.existsSync(this.tasksFilePath)) {
      const fileData = fs.readFileSync(this.tasksFilePath, 'utf-8');
      const data = JSON.parse(fileData);

      this.tasks = data.tasks || [];
      this.currentId = data.currentId || 1;
    }
  }

  // Salvas as tarefas no arquivo json
  private saveTasksToFile(): void {
    const data = {
      tasks: this.tasks,
      currentId: this.currentId
    };
    // Cria diretório se não existir
    fs.ensureDirSync(path.dirname(this.tasksFilePath));
    fs.writeFileSync(this.tasksFilePath, JSON.stringify(data, null, 2), 'utf-8');
  }

  createTask(text: string, lang: string): Task {
    const task: Task = {
      id: this.currentId++,
      text,
      summary: null,
      lang
    };
    this.tasks.push(task);
    this.saveTasksToFile(); // Salva a tarefa no arquivo
    return task;
  }

  updateTask(id: number, summary: string): Task | null {
    const taskIndex = this.tasks.findIndex(t => t.id === id);
    if (taskIndex > -1) {
      this.tasks[taskIndex].summary = summary;
      this.saveTasksToFile(); // Salva a atualização no arquivo
      return this.tasks[taskIndex];
    }
    return null;
  }

  getTaskById(id: number): Task | null {
    return this.tasks.find(t => t.id === id) || null;
  }

  getAllTasks(): Task[] {
    return this.tasks;
  }

  // Função para deletar uma tarefa pelo ID
  deleteTask(id: number): boolean {
    const taskIndex = this.tasks.findIndex(t => t.id === id);
    if (taskIndex > -1) {
      this.tasks.splice(taskIndex, 1); // Remove a tarefa
      this.saveTasksToFile(); // Salva a alteração no arquivo
      return true;
    }
    return false; // Se não encontrar a tarefa retorna falso.
  }
}