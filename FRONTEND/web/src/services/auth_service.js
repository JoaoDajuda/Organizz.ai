import api from "../../services/api.js";

export async function CriarConta(nome, CriarEmail, CriarSenha) {
    const response = await api.post("/auth/criar_conta", { nome, CriarEmail, CriarSenha });
    return response.data
}