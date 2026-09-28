import { useState } from "react";
import "./Login.css"
import { CadastrarUsuario, LoginUsuario, EsqueciSenha, RedefinirSenha } from "../../services/api.js";
import { useNavigate } from "react-router-dom"


export default function Login() {
    const [nome, setNome] = useState(""); //Cadastro
    const [email, setEmail] = useState(""); //Login
    const [senha, setSenha] = useState(""); //Login
    const [criarEmail, setcriarEmail] = useState(""); //Cadastro
    const [criarSenha, setcriarSenha] = useState(""); //Cadastro
    const [novaSenha, setNovaSenha] = useState(""); //Redefinir Senha
    const [codigo, setCodigo] = useState("");  // Redefinir senha
    const [senhaReset, setSenhaReset] = useState("");// Redefinir senha
    const [confirmaSenhaReset, setConfirmaSenhaReset] = useState(""); // Redefinir senha
    const [modo, setModo] = useState("Login") //Login/Criar conta/Redefinir Senha
    const [confirmacao, setConfirmacao] = useState(""); //Confirmação de credenciais
    const navigate = useNavigate()

    const FazerCadastro = async () => {
        try {
            const response = await CadastrarUsuario(nome, criarEmail, criarSenha);
            console.log("Usuário cadastrado com sucesso:", response);
            setModo("Login");
            setConfirmacao("Cadastro realizado com sucesso! Faça login para continuar.");
        } catch (error) {
            console.error("Erro ao cadastrar usuário:", error);
            setConfirmacao("Erro ao cadastrar usuário. Verifique os dados e tente novamente.");
        }
    }

    const FazerLogin = async () => {
        try {
            const reponse = await LoginUsuario(email, senha);
            console.log("Login realizado com sucesso:", reponse);
            navigate("/app");
        } catch (error) {
            console.error("Erro ao fazer login:", error);
            setConfirmacao("Erro ao fazer login. Verifique suas credenciais e tente novamente.");
        }
    }

    const EsqueceuSenha = async () => {
        try {
            await EsqueciSenha(email);
            console.log(`Email de recuperação enviado para ${email}`)
            setModo("RedefinirSenha");ç
            setConfirmacao("Se o email estiver cadastrado, você receberá um código em instantes.");
        } catch (error) {
            setConfirmacao(error.message);
        }
    }

    const FazerRedefinicao = async () => {
        if (senhaReset !== confirmaSenhaReset) {
            setConfirmacao("As senhas não coincidem.");
            return;
        }
        try {
            await RedefinirSenha(email, codigo.trim(), senhaReset);
            setCodigo("");
            setSenhaReset("");
            setConfirmaSenhaReset("");
            setModo("Login");
            setConfirmacao("Senha atualizada com sucesso! Faça login.");
            console.log("Senha redefinida com sucesso");
        } catch (error) {
            console.log("Erro ao redefinir a senha: ", error);
            setConfirmacao(error.message);
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
                    {confirmacao && <p className="confirmacao">{confirmacao}</p>}
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
                                    <p className="esqueceu" onClick={() => {setModo("EsqueceuSenha"), setConfirmacao("")}}>Esqueceu sua Senha?</p>
                                    <p className="cadastro" onClick={() => {setModo("Cadastro"), setConfirmacao("")}}>Cadastre-se</p>
                                    <p className="cadastro" onClick={() => {setModo("Login"), setConfirmacao("")}}>Login</p>
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
                                    <p className="esqueceu" onClick={() => {setModo("EsqueceuSenha"), setConfirmacao("")}}>Esqueceu sua Senha?</p>
                                    <p className="cadastro" onClick={() => {setModo("Cadastro"), setConfirmacao("")}}>Cadastre-se</p>
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
                                    <p className="esqueceu" onClick={() => {setModo("EsqueceuSenha"), setConfirmacao("")}}>Esqueceu sua Senha?</p>
                                    <p className="cadastro" onClick={() => {setModo("Cadastro"), setConfirmacao("")}}>Cadastre-se</p>
                                    <p className="cadastro" onClick={() => {setModo("Login"), setConfirmacao("")}}>Login</p>
                                </div>
                                <button className="BotaoLogin" onClick={EsqueceuSenha}>
                                    Enviar email
                                </button>
                            </div>
                        </>
                    )}
                    {modo == "RedefinirSenha" && (
                        <>
                            <div className="inputs">
                                <input className="Input" type="email" placeholder="Digite seu email:" value={email} onChange={(e) => setEmail(e.target.value)} />
                                <input className="Input" type="text" placeholder="Código recebido por email:" value={codigo} onChange={(e) => setCodigo(e.target.value)} />
                                <input className="Input" type="password" placeholder="Nova senha:" value={senhaReset} onChange={(e) => setSenhaReset(e.target.value)} />
                                <input className="Input" type="password" placeholder="Confirme a nova senha:" value={confirmaSenhaReset} onChange={(e) => setConfirmaSenhaReset(e.target.value)} />
                            </div>
                            <div className="areaLogin">
                                <div className="editaUsuario">
                                    <p className="esqueceu" onClick={() => {setModo("EsqueceuSenha"), setConfirmacao("")}}>Reenviar código</p>
                                    <p className="cadastro" onClick={() => {setModo("Login"), setConfirmacao("")}}>Login</p>
                                </div>
                                <button className="BotaoLogin" onClick={FazerRedefinicao}>
                                    Redefinir senha
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