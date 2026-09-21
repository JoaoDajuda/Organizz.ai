import { useState } from "react";
import "./Login.css"
import { CadastrarUsuario, LoginUsuario, EsqueciSenha } from "../../services/api.js";
import { useNavigate } from "react-router-dom"
// Falta o esqueceu a senha

export default function Login() {
    const [nome, setNome] = useState(""); //Cadastro
    const [email, setEmail] = useState(""); //Login
    const [senha, setSenha] = useState(""); //Login
    const [criarEmail, setcriarEmail] = useState(""); //Cadastro
    const [criarSenha, setcriarSenha] = useState(""); //Cadastro
    const [novaSenha, setNovaSenha] = useState(""); //Redefinir Senha
    const [modo, setModo] = useState("Login") //Login/Criar conta/Redefinir Senha

    const navigate = useNavigate()

    const FazerCadastro = async () => {
        try {
            const response = await CadastrarUsuario(nome, criarEmail, criarSenha);
            console.log("Usuário cadastrado com sucesso:", response);
            alert("Usuário cadastrado com sucesso!");
            setModo("Login");
        } catch (error) {
            console.error("Erro ao cadastrar usuário:", error);
            alert("Erro ao cadastrar usuário. Verifique os dados e tente novamente.");
        }
    }

    const FazerLogin = async () => {
        try {
            const reponse = await LoginUsuario(email, senha);
            console.log("Login realizado com sucesso:", reponse);
            alert("Login realizado com sucesso!");
            navigate("/app");
        } catch (error) {
            console.error("Erro ao fazer login:", error);
            alert("Erro ao fazer login. Verifique suas credenciais e tente novamente.");
        }
    }

    const EsqueceuSenha = async () => {
        try {
            const response = await EsqueciSenha(email);
            console.log("Recuperar a senha:", response);
            alert("Email de recuperação enviado com sucesso!");
        } catch (error) {
            console.log("Erro ao recuperar a senha: ", error);
            alert("Erro ao solicitar redefinição de senha. Verifique seu email e tente novamente.");
        }
    }

    return (
        <>
            <div className="ContainerPrincipal">
                <img
                    className="ColunaEsquerda"
                    src="/assets/colunaRealista.png"
                />
                <div className="ContainerFormulario">
                    <img
                        className="Logo"
                        src="/assets/logoMinimal.png"
                    />
                    {modo == "Cadastro" && (
                        <>
                            <div className="inputs">
                                <input className="Input" type="text" placeholder="Digite seu nome:" value={nome} onChange={(e) => setNome(e.target.value)} />
                                <input className="Input" type="email" placeholder="Digite seu email:" value={criarEmail} onChange={(e) => setcriarEmail(e.target.value)} />
                                <input className="Input" type="password" placeholder="Digite sua senha:" value={criarSenha} onChange={(e) => setcriarSenha(e.target.value)} />
                                <input className="Input" type="password" placeholder="Confirme sua senha:" value={novaSenha} onChange={(e) => setNovaSenha(e.target.value)} />
                            </div>
                            <div className="areaLogin">
                                <div className="editaUsuario">
                                    <p className="esqueceu" onClick={() => setModo("EsqueceuSenha")}>Esqueceu sua Senha?</p>
                                    <p className="cadastro" onClick={() => setModo("Cadastro")}>Cadastre-se</p>
                                    <p className="cadastro" onClick={() => setModo("Login")}>Login</p>
                                </div>
                                <button className="BotaoLogin" onClick={FazerCadastro}>
                                    Cadastrar
                                </button>
                            </div>
                        </>
                    )}
                    {modo == "Login" && (
                        <>
                            <div className="inputs">
                                <input className="Input" type="email" placeholder="Digite seu email ou usuário:" value={email} onChange={(e) => setEmail(e.target.value)} />
                                <input className="Input" type="password" placeholder="Digite sua senha:" value={senha} onChange={(e) => setSenha(e.target.value)} />
                            </div>
                            <div className="areaLogin">
                                <div className="editaUsuario">
                                    <p className="esqueceu" onClick={() => setModo("EsqueceuSenha")}>Esqueceu sua Senha?</p>
                                    <p className="cadastro" onClick={() => setModo("Cadastro")}>Cadastre-se</p>
                                </div>
                                <button className="BotaoLogin" onClick={FazerLogin}>
                                    Login
                                </button>
                            </div>
                        </>
                    )}
                    {modo == "EsqueceuSenha" && (
                        <>
                            <div className="inputs">
                                <input className="Input" type="email" placeholder="Digite seu email ou usuário:" value={email} onChange={(e) => setEmail(e.target.value)} />
                            </div>
                            <div className="areaLogin">
                                <div className="editaUsuario">
                                    <p className="esqueceu" onClick={() => setModo("EsqueceuSenha")}>Esqueceu sua Senha?</p>
                                    <p className="cadastro" onClick={() => setModo("Cadastro")}>Cadastre-se</p>
                                    <p className="cadastro" onClick={() => setModo("Login")}>Login</p>
                                </div>
                                <button className="BotaoLogin" onClick={EsqueceuSenha}>
                                    Enviar email
                                </button>
                            </div>
                        </>
                    )}
                </div>
                <img
                    className="ColunaDireita"
                    src="/assets/colunaRealista.png"
                />
            </div>
        </>
    );
}