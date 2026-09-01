import { NavLink } from "react-router-dom";
import "./Sidebar.css";

// Cada item liga a uma rota real do app — troque os "to" conforme
// as rotas já definidas no seu router.
const NAV_ITEMS = [
  { to: "/inicio", label: "Início", icon: "home" },
  { to: "/rotina", label: "Rotina", icon: "checklist" },
  { to: "/financas", label: "Finanças", icon: "cifrao" },
  { to: "/treinos", label: "Treinos", icon: "halter" },
  { to: "/calendario", label: "Calendário", icon: "calendario" },
  { to: "/relatorios", label: "Relatórios", icon: "grafico" },
  { to: "/configuracoes", label: "Configurações", icon: "engrenagem" },
];

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar__brand">
        {/* troque pelo seu asset de coluna jônica */}
        <img
          className="sidebar__brand-icon"
          src="/assets/icons/coluna.svg"
          alt=""
          aria-hidden="true"
        />
        <span className="sidebar__brand-name">ORGANIZA</span>
      </div>

      <nav className="sidebar__nav" aria-label="Navegação principal">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) =>
              "sidebar__link" + (isActive ? " sidebar__link--active" : "")
            }
          >
            <span className={`sidebar__icon sidebar__icon--${item.icon}`} />
            {item.label}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar__figure" aria-hidden="true">
        {/* busto/estátua decorativa — substitua pelo seu asset */}
        <img src="/assets/img/busto.png" alt="" />
      </div>
    </aside>
  );
}
