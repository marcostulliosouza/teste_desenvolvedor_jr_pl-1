import dotenv from "dotenv";
dotenv.config();
import app from "./app";

const PORT = process.env.PORT || 3000;

// Validação da porta
if (!process.env.PORT) {
  console.warn('Aviso: Variável de ambiente PORT não definido. Usando porta padrão 3000.')
}

app.listen(PORT, () => {
  console.log(`Node API rodando na porta ${PORT}`);
});
