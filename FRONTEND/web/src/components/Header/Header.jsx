import "./Header.css"
import { Outlet, NavLink } from "react-router-dom"
import { useNavigate, useLocation } from "react-router-dom"
import { Logout } from "../../services/api.js"
import NizaChat from "../Chat/NizaChat.jsx"

const TITULOS_POR_ROTA = {
    "/app/rotina": "Ἡμέρα — A ordem do dia",
    "/app/financas": "Οἰκονομία — A arte de administrar a casa",
}

export default function Header() {
    const navigate = useNavigate()
    const handleLogout = () => {
        Logout()
        navigate("/login")
    }

    // O título acompanha a rota atual (useLocation reage à navegação SPA);
    // rotas sem título definido mostram o nome do app
    const { pathname } = useLocation()
    const title = TITULOS_POR_ROTA[pathname] ?? "Organizz.ai"

    return (
        <div className="MainContainer">
            <img className="MainContainer-borda" src="/assets/bordaPrincipal2.png" alt="" />
            <div className="Menu">
                <img className="logo" src="/assets/logoMinimal.png" alt="Organizzai" />
                <ul className="ItensMenu">
                    <li>
                        <NavLink to="/app/rotina" className={({ isActive }) => isActive ? "active" : ""}>
                            Rotina
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to="/app/financas" className={({ isActive }) => isActive ? "active" : ""}>
                            Finanças
                        </NavLink>
                    </li>
                </ul>
                <img className="davidImage" src="/assets/davi.png" alt="" />
            </div>
            <div className="Header">
                <h1 className="title">{title}</h1>
                <button onClick={handleLogout} className="logout-button">Sair</button>
            </div>
            <div className="content">
                <Outlet />
            </div>
            <NizaChat />
        </div>
    )
}