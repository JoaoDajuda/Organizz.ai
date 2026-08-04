import { useState } from "react";
import "./Login.css"
import Modal from "../../components/modal.jsx";
import criar_conta from "../../../../../BACKEND/auth_routes.py"
import api from "../../API/api.js";

export default function Login() {
    const [nome, setNome] = useState(""); //Cadastro
    const [email, setEmail] = useState(""); //Login
    const [senha, setSenha] = useState(""); //Login
    const [criarEmail, setcriarEmail] = useState(""); //Cadastro
    const [criarSenha, setcriarSenha] = useState(""); //Cadastro
    const [novaSenha, setNovaSenha] = useState(""); //Renovar Senha
    const [openModalCadastro, setOpenModalCadastro] = useState(false);
    const [openModalEsqueceuSenha, setOpenModalEsqueceuSenha] = useState(false);

    const FazerLogin = () => {
        api.post("/criar_conta", { email, senha})
    };

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
                                    FazerLogin(api.post(criar_conta(), {nome, email, senha}));
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
                                    <button className="BotaoLogin" onClick={() => {
                                        console.log("Nome:", nome); //RETIRAR DEPOIS
                                        console.log("Email:", criarEmail); //RETIRAR DEPOIS
                                        console.log("Senha:", criarSenha); //RETIRAR DEPOIS
                                        console.log("Nova Senha:", novaSenha); //RETIRAR DEPOIS
                                        setOpenModalCadastro(false)
                                    }}>
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