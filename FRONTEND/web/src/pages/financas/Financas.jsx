import "./Financas.css"
import GraficoFinanceiro from "../../components/gráficoDeFinancas/GraficoFinancas.jsx"
import Transacoes from "../../components/transacoes/Transacoes.jsx"

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
            <div className="Conteudo">
                <div className="Grafico">
                    <GraficoFinanceiro
                        dados={[
                            { label: "Alimentação", valor: 46 },
                            { label: "Compras", valor: 46 },
                            { label: "Transporte", valor: 46 },
                            { label: "Lazer", valor: 46 },
                        ]}
                    />
                </div>
                <div className="ResumoTransacoes">
                    {/* <Transacoes
                        dadosTransacoes={[
                            { descricao: "Alimentação", valor: 46 },
                            { descricao: "Compras", valor: 46 },
                            { descricao: "Transporte", valor: 46 },
                            { descricao: "Lazer", valor: 46 },
                        ]}
                    /> */}
                </div>
            </div>
        </div>
    )
}