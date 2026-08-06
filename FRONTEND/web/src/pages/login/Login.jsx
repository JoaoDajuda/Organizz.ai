import { useState } from "react";
import "./Login.css"
import Modal from "../../components/modal.jsx";
import api from "../../API/api.js";

export default function Login() {
    const [email, setEmail] = useState("");
    const [senha, setSenha] = useState("");
    const [openModalCadastro, setOpenModalCadastro] = useState(false);
    const [openModalEsqueceuSenha, setOpenModalEsqueceuSenha] = useState(false);

    const FazerLogin = () => {
        api.post("/login", { email, senha})
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
                            console.log(e.target.value) //RETIRAR DEPOIS
                            setSenha(e.target.value)}
                        }
                    />
                    <div className="areaLogin">
                        <div className="cadastrarSenha">
                            <p className="esqueceu" onClick={() => setOpenModalEsqueceuSenha(true)}>
                                Esqueceu sua senha?
                            </p>
                            <Modal isOpen={openModalEsqueceuSenha} onClose={() => setOpenModalEsqueceuSenha(false)}>
                                <div className="inputs">
                                    <input className="Input" type="email" placeholder="Digite seu email:" />
                                </div>
                                <div className="areaLogin">
                                    <button className="BotaoLogin" onClick={() => setOpenModalEsqueceuSenha(false)}>
                                        Enviar
                                    </button>
                                </div>
                            </Modal>
                            <p className="cadastro" onClick={() => setOpenModalCadastro(true)}>
                                Cadastre-se
                            </p>
                            <Modal isOpen={openModalCadastro} onClose={() => setOpenModalCadastro(false)}>
                                <div className="inputs">
                                    <input className="Input" type="text" placeholder="Digite seu nome:" />
                                    <input className="Input" type="email" placeholder="Digite seu email:" />
                                    <input className="Input" type="password" placeholder="Digite sua senha:" />
                                    <input className="Input" type="password" placeholder="Confirme sua senha:" />
                                </div>
                                <div className="areaLogin">
                                    <button className="BotaoLogin" onClick={() => setOpenModalCadastro(false)}>
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