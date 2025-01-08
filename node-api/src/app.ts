import express, { Application, Request, Response, NextFunction } from 'express';
import tasksRoutes from './routes/tasksRoutes';

const app: Application = express();
app.use(express.json());

// Rotas
app.use('/tasks', tasksRoutes);

// Rota inicial
app.get('/', (req, res) => {
  res.json({ message: 'API is running' })
});

app.use((error: Error, req: Request, res: Response, next: NextFunction) => {
  console.error(error.stack);
  res.status(500).json({ error: 'Erro do Servidor Interno' });
});

export default app;