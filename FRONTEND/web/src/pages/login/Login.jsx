import { useState } from "react";
import "./Login.css"
import Modal from "../../components/modal.jsx";
// import criar_conta from "../../../../../BACKEND/auth_routes.py"
import { CadastrarUsuario } from "../../services/api.js";

export default function Login() {
    const [nome, setNome] = useState(""); //Cadastro
    const [email, setEmail] = useState(""); //Login
    const [senha, setSenha] = useState(""); //Login
    const [criarEmail, setcriarEmail] = useState(""); //Cadastro
    const [criarSenha, setcriarSenha] = useState(""); //Cadastro
    const [novaSenha, setNovaSenha] = useState(""); //Renovar Senha
    const [openModalCadastro, setOpenModalCadastro] = useState(false);
    const [openModalEsqueceuSenha, setOpenModalEsqueceuSenha] = useState(false);

    const FazerCadastro = async () => {
        try {
            const response = await CadastrarUsuario(nome, criarEmail, criarSenha);
            console.log("Usuário cadastrado com sucesso:", response);
            setOpenModalCadastro(false);
        } catch (error) {
            console.error("Erro ao cadastrar usuário:", error);
        }
    }

    return (
        <>
            <div className="ContainerPrincipal">
                <img
                    className="ColunaEsquerda"
                    src="/assets/colunaDourada.png"
                />
                <div className="ContainerFormulario">
                    <img
                        className="logo"
                        src="/assets/logoDourada.png"
                    />
                    <input 
                        className="Input"
                        type="Email"
                        placeholder="Digite seu email:"
                        value={email}
                        onChange={(e) => {
                            console.log(e.target.value) //RETIRAR DEPOIS
                            setEmail(e.target.value)
                        }}
                    />
                    <input 
                        className="Input"
                        type="Password"
                        placeholder="Digite sua senha:"
                        value={senha}
                        onChange={(e) => {
                            setSenha(e.target.value)}
                        }
                    />
                    <div className="criarConta">
                        <div className="cadastrarSenha">
                            <p className="esqueceu" onClick={() => setOpenModalEsqueceuSenha(true)}>
                                Esqueceu sua senha?
                            </p>
                            <Modal isOpen={openModalEsqueceuSenha} onClose={() => setOpenModalEsqueceuSenha(false)}>
                                <div className="inputs">
                                    <input className="Input" type="email" placeholder="Digite seu email:" onChange={(e) => {setEmail(e.target.value);}} />
                                    <input className="Input" type="password" placeholder="Digite sua senha:" onChange={(e) => {setSenha(e.target.value);}} />
                                </div>
                                <div className="areaLogin">
                                    <button className="BotaoLogin" onClick={() => {
                                        console.log("Email:", email); //RETIRAR DEPOIS
                                        console.log("Senha:", senha); //RETIRAR DEPOIS
                                        setOpenModalEsqueceuSenha(false)
                                    }}>
                                        Enviar
                                    </button>
                                </div>
                            </Modal>
                            <p className="cadastro" onClick={() => {
                                    setOpenModalCadastro(true)}
                                }>
                                Cadastre-se
                            </p>
                            <Modal isOpen={openModalCadastro} onClose={() => setOpenModalCadastro(false)}>
                                <div className="inputs">
                                    <input className="Input" type="text" placeholder="Digite seu nome:" value={nome} onChange={(e) => setNome(e.target.value)} />
                                    <input className="Input" type="email" placeholder="Digite seu email:" value={criarEmail} onChange={(e) => setcriarEmail(e.target.value)} />
                                    <input className="Input" type="password" placeholder="Digite sua senha:" value={criarSenha} onChange={(e) => setcriarSenha(e.target.value)} />
                                    <input className="Input" type="password" placeholder="Confirme sua senha:" value={novaSenha} onChange={(e) => setNovaSenha(e.target.value)} />
                                </div>
                                <div className="areaLogin">
                                    <button className="BotaoLogin" onClick={FazerCadastro}>
                                        Cadastrar
                                    </button>
                                </div>
                            </Modal>
                        </div>
                        <button className="BotaoLogin">
                            Entrar
                        </button>
                    </div>
                </div>
                <img
                    className="ColunaDireita"
                    src="/assets/colunaDourada.png"
                />
            </div>
        </>
    );
}