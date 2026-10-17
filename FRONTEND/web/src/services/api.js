import axios from "axios";

const apiBaseURL = import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
    baseURL: apiBaseURL,
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
        const response = await api.post("auth/fazer_login", { email, senha });
        const { acess_token, refresh_token } = response.data;
        localStorage.setItem("acess_token", acess_token);
        localStorage.setItem("refresh_token", refresh_token);
        return response.data;
    } catch (error) {
        const mensagem = error.response?.data?.detail || "Erro ao fazer login";
        throw new Error(mensagem);
    }
}

export async function ObterOnboarding() {
    try {
        const response = await api.get("/onboarding");
        return response.data;
    } catch (error) {
        const mensagem = error.response?.data?.detail || "Não foi possível carregar seu perfil financeiro";
        throw new Error(mensagem);
    }
}

export async function SalvarOnboarding(respostas) {
    try {
        const response = await api.put("/onboarding", respostas);
        return response.data;
    } catch (error) {
        const mensagem = error.response?.data?.detail || "Não foi possível salvar seu perfil financeiro";
        throw new Error(mensagem);
    }
}

// Para enviar o token em toda requisição
api.interceptors.request.use((config) => {
    const token = localStorage.getItem("acess_token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Renova o token quando expira
api.interceptors.response.use(
    (response) => response,
    async (error) => {
        const original = error.config;
        const status = error.response?.status;

        if (status === 401 && !original._retry && !original.url.includes("auth/")) {
            original._retry = true;
            try {
                const refresh = localStorage.getItem("refresh_token");
                const { data } = await axios.get(`${apiBaseURL}/auth/refresh`, {
                    headers: { Authorization: `Bearer ${refresh}` },
                });
                localStorage.setItem("acess_token", data.acess_token);
                original.headers.Authorization = `Bearer ${data.acess_token}`;
                return api(original);
            } catch {
                Logout();
                window.location.href = "/login";
            }
        }
        return Promise.reject(error);
    }
);

export function Logout() {
    localStorage.removeItem("acess_token");
    localStorage.removeItem("refresh_token");
}

export async function EsqueciSenha(email) {
    try {
        const response = await api.post("auth/esqueci-senha", { email });
        return response.data;
    } catch (error) {
        const mensagem = error.response?.data?.detail || "Erro ao solicitar redefinição de senha";
        throw new Error(mensagem);
    }
}

export async function RedefinirSenha(email, codigo, novaSenha) {
    try {
        const response = await api.post("auth/resetar-senha", {
            email,
            codigo,
            nova_senha: novaSenha,
        });
        return response.data;
    } catch (error) {
        const mensagem = error.response?.data?.detail || "Erro ao redefinir senha";
        throw new Error(mensagem);
    }
}

