import "./Header.css";

const TOP_NAV = [
  { to: "/inicio", label: "Início" },
  { to: "/rotina", label: "Rotina" },
  { to: "/financas", label: "Finanças" },
  { to: "/treinos", label: "Treinos" },
];

export default function Header({ userName = "Usuário" }) {
  return (
    <header className="app-header">
      <nav className="app-header__nav" aria-label="Navegação secundária">
        {TOP_NAV.map((item) => (
          <a key={item.to} href={item.to} className="app-header__link">
            {item.label}
          </a>
        ))}
      </nav>

      <div className="app-header__user">
        <button className="app-header__bell" aria-label="Notificações">
          <span className="app-header__bell-icon" />
        </button>
        <span className="app-header__avatar" aria-hidden="true" />
        <span className="app-header__greeting">Olá, {userName}</span>
      </div>
    </header>
  );
}
