import { Router, Request, Response } from "express";
import { TasksRepository } from "../repositories/tasksRepository";
import axios from 'axios';

const router = Router();
const tasksRepository = new TasksRepository();

// Definindo a URL do serviço python a partir da .env
const PYTHON_LLM_URL = process.env.PYTHON_LLM_URL || "http://localhost:5000";

// Função para interagir com o serviço python e ter o resumo
const getSummaryFromPython = async (text: string, lang: string): Promise<string> => {
  try {
    const response = await axios.post(`${PYTHON_LLM_URL}/summarize`, { text, lang });
    return response.data.summary;
  } catch (error) {
    console.error('Erro ao se comunicar com o serviço python: ', error);
    throw new Error('Não foi possível gerar o resumo.');
  }
};

// POST: Cria uma tarefa e solicita resumo ao serviço Python
router.post("/", async (req: Request, res: Response) => {
  try {
    const { text, lang } = req.body;
    if (!text) {
      return res.status(400).json({ error: 'Campo "text" é obrigatório.' });
    }

    const supportedLanguages = ['pt', 'en', 'es'];
    if (!lang || !supportedLanguages.includes(lang)) {
      return res
        .status(400)
        .json({ error: 'Campo "lang" é obrigatório e deve ser um dos valores: "pt", "en", "es".' });
    }

    // Cria a "tarefa"
    const task = tasksRepository.createTask(text, lang);

    // Solicita o resumo ao serviço python
    const summary = await getSummaryFromPython(text, lang);

    // Atualiza a tarefa com o resumo
    tasksRepository.updateTask(task.id, summary);

    return res.status(201).json({
      message: "Tarefa criada com sucesso!",
      task: tasksRepository.getTaskById(task.id),
    });
  } catch (error) {
    console.error("Erro ao criar tarefa:", error);
    return res
      .status(500)
      .json({ error: "Ocorreu um erro ao criar a tarefa." });
  }
});

// GET: Lista todas as tarefas
router.get("/", (req: Request, res: Response) => {
  const tasks = tasksRepository.getAllTasks();
  return res.json(tasks);
});

// GET: Retorna uma tarefa específica pelo ID
router.get('/:id', (req: Request, res: Response) => {
  const taskId = parseInt(req.params.id, 10);
  const task = tasksRepository.getTaskById(taskId);

  if (!task) {
    return res.status(404).json({ error: 'Tarefa não encontrada.' });
  }

  return res.json(task);
});

// DELETE: Remove uma tarefa pelo ID
router.delete('/:id', (req: Request, res: Response) => {
  const taskId = parseInt(req.params.id, 10);
  const task = tasksRepository.getTaskById(taskId);

  if (!task) {
    return res.status(404).json({ error: 'Tarefa não encontrada.' });
  }

  tasksRepository.deleteTask(taskId);

  return res.status(200).json({ message: 'Tarefa removida com sucesso.' });
});
export default router;
