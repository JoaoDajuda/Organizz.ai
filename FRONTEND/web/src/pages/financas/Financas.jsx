import "./Financas.css"

export default function Financas() {
    return (
        <div className="PaginaFinancas">
            <div className="Header">
                <img
                    className="logo"
                    src="/assets/logoDourada.png"
                />
                <ul className="ItensHeader" styles={{ listStyleType: "none" }}>
                    <li>Início</li>
                    <li>Rotina</li>
                    <li>Finanças</li>
                </ul>
            </div>
        </div>
    )
}