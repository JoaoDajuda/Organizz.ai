import { useState } from "react";
import "./Login.css"

export default function Login() {
    const [email, setEmail] = useState("");
    const [senha, setSenha] = useState("");

    const FazerLogin = () => {
        console.log("Login:", email, senha);
    };

    return (
        <>
            <div className="ContainerPrincipal">
                <img
                    className="ColunaEsquerda"
                    src="/assets/colunaDourada.png"
                />
                <div className="ContainerFormulario">
                    <div className="ContainerPrincipal">
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
                            type="Email"
                            placeholder="Digite sua senha:"
                            value={senha}
                            onChange={(e) => {
                                console.log(e.target.value) //RETIRAR DEPOIS
                                setSenha(e.target.value)}
                            }
                        />
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