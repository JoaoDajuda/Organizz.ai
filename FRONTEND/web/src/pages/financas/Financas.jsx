import { useEffect, useMemo, useState } from "react"
import { Doughnut } from "react-chartjs-2"
import { ArcElement, Chart as ChartJS, Legend, Tooltip } from "chart.js"
import { CriarValor, ListarValores } from "../../services/api.js"
import "./Financas.css"

ChartJS.register(ArcElement, Tooltip, Legend)

const TIPOS_GASTO = [
    "Moradia",
    "Alimentação",
    "Transporte",
    "Saúde",
    "Lazer",
    "Educação",
    "Outros",
]

const CORES_TIPOS = {
    "Moradia": "#C9A94D",
    "Alimentação": "#E4C87A",
    "Transporte": "#A8863E",
    "Saúde": "#5B8C85",
    "Lazer": "#8C6A3F",
    "Educação": "#5B7DB1",
    "Outros": "#475569",
}

const formatoMoeda = new Intl.NumberFormat("pt-BR", {
    style: "currency",
    currency: "BRL",
})

function dataAtualLocal() {
    const hoje = new Date()
    return `${hoje.getFullYear()}-${String(hoje.getMonth() + 1).padStart(2, '0')}-${String(hoje.getDate()).padStart(2, '0')}`
}

function mesmoMes(dataIso) {
    const data = new Date(dataIso)
    const hoje = new Date()
    return data.getMonth() === hoje.getMonth() && data.getFullYear() === hoje.getFullYear()
}

// Plugin que desenha o total no centro da rosca
const pluginTextoCentro = {
    id: "textoCentro",
    afterDraw(chart) {
        const meta = chart.getDatasetMeta(0)
        if (!meta?.data?.length) return
        const { x, y } = meta.data[0]
        const config = chart.options.plugins.textoCentro
        if (!config) return

        const { ctx } = chart
        ctx.save()
        ctx.textAlign = "center"
        ctx.font = "600 0.7rem Cinzel, serif"
        ctx.fillStyle = "#C5CCD6"
        ctx.fillText(config.titulo, x, y - 10)
        ctx.font = "700 1.15rem Cinzel, serif"
        ctx.fillStyle = "#C9A94D"
        ctx.fillText(config.valor, x, y + 12)
        ctx.restore()
    },
}

export default function Financas() {
    const [movimentacoes, setMovimentacoes] = useState([])
    const [carregando, setCarregando] = useState(true)
    const [erro, setErro] = useState("")

    const [form, setForm] = useState({
        tipo: "Saida",
        valor: "",
        categoria: "Moradia",
        data: dataAtualLocal(),
    })
    const [enviando, setEnviando] = useState(false)
    const [erroForm, setErroForm] = useState("")
    const [mensagemForm, setMensagemForm] = useState("")

    useEffect(() => {
        let ativo = true

        ListarValores()
            .then((dados) => {
                if (ativo) setMovimentacoes(dados)
            })
            .catch((error) => {
                if (ativo) setErro(error.message || "Não foi possível carregar suas movimentações.")
            })
            .finally(() => {
                if (ativo) setCarregando(false)
            })

        return () => {
            ativo = false
        }
    }, [])

    const doMes = useMemo(
        () => movimentacoes.filter((movimento) => mesmoMes(movimento.data_movimentacao)),
        [movimentacoes]
    )

    const totalEntradas = useMemo(
        () => doMes
            .filter((movimento) => movimento.tipo_valor === "Entrada")
            .reduce((soma, movimento) => soma + movimento.valor, 0),
        [doMes]
    )

    const gastosPorTipo = useMemo(() => {
        const acumulado = new Map()
        doMes
            .filter((movimento) => movimento.tipo_valor === "Saida")
            .forEach((movimento) => {
                const tipo = movimento.categoria || "Outros"
                acumulado.set(tipo, (acumulado.get(tipo) ?? 0) + movimento.valor)
            })
        return [...acumulado.entries()]
            .map(([tipo, valor]) => ({ tipo, valor }))
            .sort((a, b) => b.valor - a.valor)
    }, [doMes])

    const totalGastos = gastosPorTipo.reduce((soma, gasto) => soma + gasto.valor, 0)
    const saldo = totalEntradas - totalGastos
    const temDados = gastosPorTipo.length > 0

    const dadosGrafico = useMemo(() => ({
        labels: gastosPorTipo.map((gasto) => gasto.tipo),
        datasets: [{
            data: gastosPorTipo.map((gasto) => gasto.valor),
            backgroundColor: gastosPorTipo.map((gasto) => CORES_TIPOS[gasto.tipo] ?? "#475569"),
            borderColor: "#1B2A4A",
            borderWidth: 2,
            hoverOffset: 8,
        }],
    }), [gastosPorTipo])

    const opcoesGrafico = useMemo(() => ({
        cutout: "68%",
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: "#0F1B33",
                borderColor: "rgba(201, 169, 77, 0.45)",
                borderWidth: 1,
                titleColor: "#F5F0E6",
                bodyColor: "#C5CCD6",
                titleFont: { family: "Cinzel, serif" },
                padding: 10,
                callbacks: {
                    label(contexto) {
                        const porcentagem = ((contexto.parsed / totalGastos) * 100).toFixed(1)
                        return ` ${formatoMoeda.format(contexto.parsed)} (${porcentagem}%)`
                    },
                },
            },
            textoCentro: {
                titulo: "Total do mês",
                valor: formatoMoeda.format(totalGastos),
            },
        },
    }), [totalGastos])

    function atualizarForm(campo, valor) {
        setForm((atual) => ({ ...atual, [campo]: valor }))
    }

    async function enviarForm(evento) {
        evento.preventDefault()
        setErroForm("")
        setMensagemForm("")

        const valorNumerico = Number(form.valor)
        if (!form.valor || Number.isNaN(valorNumerico) || valorNumerico <= 0) {
            setErroForm("Informe um valor maior que zero.")
            return
        }
        if (form.tipo === "Saida" && !form.categoria) {
            setErroForm("Selecione o tipo de gasto.")
            return
        }

        setEnviando(true)
        try {
            const criada = await CriarValor({
                tipo_valor: form.tipo,
                valor: valorNumerico,
                categoria: form.tipo === "Saida" ? form.categoria : null,
                data: form.data || null,
            })
            setMovimentacoes((atuais) => [criada, ...atuais])
            setMensagemForm(
                form.tipo === "Entrada"
                    ? "Entrada registrada com sucesso!"
                    : "Gasto registrado com sucesso!"
            )
            setForm((atual) => ({ ...atual, valor: "" }))
        } catch (error) {
            setErroForm(error.message || "Não foi possível registrar o valor.")
        } finally {
            setEnviando(false)
        }
    }

    return (
        <div className="PaginaFinancas">
            <header className="financasTopo">
                <h1 className="financasTitulo">Finanças</h1>
                <p className="financasSubtitulo">Como seus gastos estão distribuídos neste mês</p>
            </header>

            {carregando && <p role="status">Carregando movimentações...</p>}
            {erro && <p role="alert">{erro}</p>}

            <section className="financasResumo">
                <div className="financasCardResumo">
                    <span className="resumoRotulo">Entradas</span>
                    <span className="resumoValor resumoEntradas">
                        {formatoMoeda.format(totalEntradas)}
                    </span>
                </div>
                <div className="financasCardResumo">
                    <span className="resumoRotulo">Gastos</span>
                    <span className="resumoValor resumoSaidas">
                        {formatoMoeda.format(totalGastos)}
                    </span>
                </div>
                <div className="financasCardResumo">
                    <span className="resumoRotulo">Saldo</span>
                    <span className={`resumoValor ${saldo >= 0 ? "resumoEntradas" : "resumoSaidas"}`}>
                        {formatoMoeda.format(saldo)}
                    </span>
                </div>
            </section>

            <section className="financasCorpo">
                <div className="financasCardGrafico">
                    <h2 className="cardTitulo">Gastos por tipo</h2>
                    {temDados ? (
                        <div className="graficoArea">
                            <Doughnut data={dadosGrafico} options={opcoesGrafico} plugins={[pluginTextoCentro]} />
                        </div>
                    ) : (
                        <p className="graficoVazio">
                            Nenhuma saída registrada neste mês. Adicione um valor ao lado para
                            começar a acompanhar seus gastos.
                        </p>
                    )}
                </div>

                <div className="financasLateral">
                    <aside className="financasCardTipos">
                        <h2 className="cardTitulo">Tipos de gasto</h2>
                        {temDados ? (
                            <ul className="tiposLista">
                                {gastosPorTipo.map((gasto) => {
                                    const porcentagem = ((gasto.valor / totalGastos) * 100).toFixed(1)
                                    return (
                                        <li key={gasto.tipo} className="tipoItem">
                                            <span
                                                className="tipoCor"
                                                style={{ backgroundColor: CORES_TIPOS[gasto.tipo] ?? "#475569" }}
                                            />
                                            <span className="tipoNome">{gasto.tipo}</span>
                                            <span className="tipoValores">
                                                <span className="tipoValor">
                                                    {formatoMoeda.format(gasto.valor)}
                                                </span>
                                                <span className="tipoPorcentagem">{porcentagem}%</span>
                                            </span>
                                        </li>
                                    )
                                })}
                            </ul>
                        ) : (
                            <p className="listaVazia">Nenhum gasto registrado neste mês.</p>
                        )}
                    </aside>

                    <form className="financasCardForm" onSubmit={enviarForm}>
                        <h2 className="cardTitulo">Adicionar valor</h2>

                        <div className="formTipo" role="group" aria-label="Tipo de movimentação">
                            <button
                                type="button"
                                className={`formTipoBotao ${form.tipo === "Entrada" ? "selecionado entrada" : ""}`}
                                onClick={() => atualizarForm("tipo", "Entrada")}
                            >
                                Entrada
                            </button>
                            <button
                                type="button"
                                className={`formTipoBotao ${form.tipo === "Saida" ? "selecionado saida" : ""}`}
                                onClick={() => atualizarForm("tipo", "Saida")}
                            >
                                Saída
                            </button>
                        </div>

                        <label className="formCampo">
                            <span>Valor</span>
                            <input
                                type="number"
                                step="0.01"
                                min="0.01"
                                placeholder="0,00"
                                value={form.valor}
                                onChange={(evento) => atualizarForm("valor", evento.target.value)}
                                required
                            />
                        </label>

                        {form.tipo === "Saida" && (
                            <label className="formCampo">
                                <span>Tipo de gasto</span>
                                <select
                                    value={form.categoria}
                                    onChange={(evento) => atualizarForm("categoria", evento.target.value)}
                                >
                                    {TIPOS_GASTO.map((tipo) => (
                                        <option key={tipo} value={tipo}>{tipo}</option>
                                    ))}
                                </select>
                            </label>
                        )}

                        <label className="formCampo">
                            <span>Data</span>
                            <input
                                type="date"
                                value={form.data}
                                onChange={(evento) => atualizarForm("data", evento.target.value)}
                            />
                        </label>

                        {erroForm && <p className="formFeedback erro" role="alert">{erroForm}</p>}
                        {mensagemForm && <p className="formFeedback sucesso" role="status">{mensagemForm}</p>}

                        <button type="submit" className="formEnviar" disabled={enviando}>
                            {enviando ? "Registrando..." : "Adicionar"}
                        </button>
                    </form>
                </div>
            </section>
        </div>
    )
}
