import axios from "axios";

const api = axios.create({
    baseURL: "http://localhost:8000",
    headers: { "Content-Type": "application/json" }
});

export async function CadastrarUsuario(nome, email, senha) {
    try {
        const response = await api.post("auth/criar_conta", { nome, email, senha, ativo: true , admin: false });
        return response.data;
    } catch (error) {
        const mensagem = error.response?.data?.detail || "Erro ao cadastrar";
        throw new Error(mensagem);

    }
}

export async function LoginUsuario(email, senha) {
    try {
        const response = await api.post("auth/login", { email, senha });
        return response.data;
    } catch (error) {
        const mensagem = error.response?.data?.detail || "Erro ao fazer login";
        throw new Error(mensagem);
    }
}
