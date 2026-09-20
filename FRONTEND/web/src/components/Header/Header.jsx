import "./Header.css"
import Calendar from "../Calendar/Calendar.jsx"
import { Outlet, NavLink } from "react-router-dom"

export default function Header() {
    return (
        <div className="MainContainer">
            <img className="MainContainer-borda" src="/assets/bordaPrincipal2.png" alt="" />
            <div className="Menu">
                <img className="logo" src="/assets/logoMinimal.png" alt="Organizzai" />
                <ul className="ItensMenu">
                    <li>
                        <NavLink to="/" end className={({ isActive }) => isActive ? "active" : ""}>
                            Início
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to="/rotina" className={({ isActive }) => isActive ? "active" : ""}>
                            Rotina
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to="/financas" className={({ isActive }) => isActive ? "active" : ""}>
                            Finanças
                        </NavLink>
                    </li>
                </ul>
                <img className="davidImage" src="/assets/davi.png" alt="" />
            </div>
            <div className="Header">
                <h1>Organizzai</h1>
                <h3>Perfil</h3>
            </div>
            <div className="content">
                <Outlet />
            </div>
        </div>
    )
}