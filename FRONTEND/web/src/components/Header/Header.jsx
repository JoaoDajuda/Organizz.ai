import "./Header.css"
import { Outlet, NavLink } from "react-router-dom"
import { useNavigate } from "react-router-dom"

export default function Header() {
    const navigate = useNavigate()
    const handleLogout = () => {
        // localStorage.removeItem("token") — quando tiver autenticação
        navigate("/login")
    }
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
                <h1>Organizzai</h1>
                <button onClick={handleLogout} className="logout-button">Sair</button>
            </div>
            <div className="content">
                <Outlet />
            </div>
        </div>
    )
}