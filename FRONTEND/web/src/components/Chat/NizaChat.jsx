import { useEffect, useRef, useState } from "react"
import { ObterOnboarding, SalvarOnboarding } from "../../services/api.js"
import "./NizaChat.css"

const WS_URL = import.meta.env.VITE_BOT_WS_URL || "ws://localhost:8001/robo/ws"

const EMPTY_PROFILE = {
    objetivo_financeiro: "",
    faixa_renda_mensal: "",
    faixa_despesas_mensais: "",
    possui_dividas: "",
    reserva_emergencia: "",
    perfil_risco: "",
}

const FAIXAS = [
    { value: "ate_2000", label: "Até R$ 2.000" },
    { value: "2001_5000", label: "R$ 2.001 a R$ 5.000" },
    { value: "5001_10000", label: "R$ 5.001 a R$ 10.000" },
    { value: "acima_10000", label: "Acima de R$ 10.000" },
    { value: "prefiro_nao_informar", label: "Prefiro não informar" },
]

const RESERVAS = [
    { value: "nenhuma", label: "Ainda não tenho reserva" },
    { value: "menos_1_mes", label: "Menos de 1 mês de despesas" },
    { value: "1_3_meses", label: "De 1 a 3 meses de despesas" },
    { value: "mais_3_meses", label: "Mais de 3 meses de despesas" },
    { value: "prefiro_nao_informar", label: "Prefiro não informar" },
]

const PERFIS_RISCO = [
    { value: "conservador", label: "Prefiro estabilidade" },
    { value: "moderado", label: "Equilíbrio entre segurança e crescimento" },
    { value: "arrojado", label: "Aceito oscilações por maior potencial" },
    { value: "nao_sei", label: "Ainda não sei" },
]

function perfilParaFormulario(profile) {
    if (!profile) return EMPTY_PROFILE
    return { ...profile, possui_dividas: String(profile.possui_dividas) }
}

function mensagemErro(error, fallback) {
    return error instanceof Error ? error.message : fallback
}

export default function NizaChat() {
    const [open, setOpen] = useState(false)
    const [view, setView] = useState("loading")
    const [loadAttempt, setLoadAttempt] = useState(0)
    const [step, setStep] = useState(0)
    const [form, setForm] = useState(EMPTY_PROFILE)
    const [saving, setSaving] = useState(false)
    const [formError, setFormError] = useState("")
    const [loadError, setLoadError] = useState("")
    const [socketStatus, setSocketStatus] = useState("closed")
    const [connectionError, setConnectionError] = useState("")
    const [messages, setMessages] = useState([])
    const [draft, setDraft] = useState("")
    const [generating, setGenerating] = useState(false)
    const socketRef = useRef(null)
    const bottomRef = useRef(null)

    useEffect(() => {
        if (!open) return undefined

        let cancelled = false

        ObterOnboarding()
            .then((state) => {
                if (cancelled) return
                setForm(perfilParaFormulario(state.profile))
                if (state.completed) {
                    setSocketStatus("connecting")
                    setConnectionError("")
                    setView("chat")
                } else {
                    setView("onboarding")
                }
            })
            .catch((error) => {
                if (cancelled) return
                setLoadError(mensagemErro(error, "Não foi possível carregar o onboarding."))
                setView("error")
            })

        return () => {
            cancelled = true
        }
    }, [open, loadAttempt])

    useEffect(() => {
        if (!open || view !== "chat") return undefined

        const token = localStorage.getItem("acess_token")
        if (!token) return undefined

        let disposed = false
        const socket = new WebSocket(WS_URL)
        socketRef.current = socket

        socket.onopen = () => {
            socket.send(JSON.stringify({ type: "auth", token }))
        }

        socket.onmessage = (event) => {
            if (disposed) return
            let data
            try {
                data = JSON.parse(event.data)
            } catch {
                setConnectionError("O bot enviou uma resposta inválida.")
                return
            }

            if (data.type === "authenticated") {
                setSocketStatus("ready")
                setConnectionError("")
            } else if (data.type === "start") {
                setGenerating(true)
                setMessages((current) => [
                    ...current,
                    { id: String(data.request_id), sender: "bot", content: "" },
                ])
            } else if (data.type === "delta") {
                setMessages((current) => current.map((message) => (
                    message.id === String(data.request_id)
                        ? { ...message, content: message.content + data.text }
                        : message
                )))
            } else if (data.type === "done") {
                setGenerating(false)
            } else if (data.type === "error") {
                setGenerating(false)
                if (data.request_id !== undefined) {
                    setMessages((current) => current.map((message) => (
                        message.id === String(data.request_id)
                            ? { ...message, content: message.content || data.detail }
                            : message
                    )))
                } else {
                    setConnectionError(data.detail || "Não foi possível iniciar a conversa.")
                }
            }
        }

        socket.onerror = () => {
            if (!disposed) setConnectionError("Não foi possível conectar ao serviço da Niza.")
        }

        socket.onclose = (event) => {
            if (disposed) return
            setSocketStatus("closed")
            setGenerating(false)
            if (event.code === 4401) {
                setConnectionError("Sua sessão expirou. Entre novamente para continuar.")
            } else if (event.code === 4403) {
                setConnectionError("Conclua seu perfil financeiro para iniciar a conversa.")
            } else if (event.code === 1013) {
                setConnectionError("O backend está indisponível. Tente novamente em instantes.")
            } else if (event.code !== 1000) {
                setConnectionError("A conexão com a Niza foi encerrada.")
            }
        }

        return () => {
            disposed = true
            socket.close(1000)
            if (socketRef.current === socket) socketRef.current = null
        }
    }, [open, view])

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" })
    }, [messages, view])

    useEffect(() => {
        if (!open) return undefined
        const fecharComEscape = (event) => {
            if (event.key === "Escape") setOpen(false)
        }
        document.addEventListener("keydown", fecharComEscape)
        return () => document.removeEventListener("keydown", fecharComEscape)
    }, [open])

    function atualizarCampo(event) {
        const { name, value } = event.target
        setForm((current) => ({ ...current, [name]: value }))
    }

    async function enviarOnboarding(event) {
        event.preventDefault()
        setFormError("")
        if (step === 0) {
            setStep(1)
            return
        }

        setSaving(true)
        try {
            const respostas = {
                ...form,
                possui_dividas: form.possui_dividas === "true",
            }
            const state = await SalvarOnboarding(respostas)
            setForm(perfilParaFormulario(state.profile))
            setMessages([])
            setSocketStatus("connecting")
            setConnectionError("")
            setView("chat")
        } catch (error) {
            setFormError(mensagemErro(error, "Não foi possível salvar suas respostas."))
        } finally {
            setSaving(false)
        }
    }

    function enviarMensagem(event) {
        event.preventDefault()
        const content = draft.trim()
        const socket = socketRef.current
        if (!content || socketStatus !== "ready" || generating || socket?.readyState !== WebSocket.OPEN) return

        const requestId = globalThis.crypto?.randomUUID?.() || String(Date.now())
        const userMessage = {
            id: `${requestId}-user`,
            sender: "user",
            content,
            type: "text",
        }
        const input = [...messages, userMessage].map((message) => ({
            id: message.id,
            sender: message.sender,
            content: message.content,
            type: "text",
        }))

        setMessages((current) => [...current, userMessage])
        setDraft("")
        socket.send(JSON.stringify({ type: "chat", request_id: requestId, input }))
    }

    function editarPerfil() {
        setStep(0)
        setFormError("")
        setView("onboarding")
    }

    function alternarChat() {
        if (open) {
            setOpen(false)
            return
        }
        setView("loading")
        setLoadError("")
        setOpen(true)
    }

    function tentarCarregar() {
        setView("loading")
        setLoadError("")
        setLoadAttempt((attempt) => attempt + 1)
    }

    return (
        <div className="niza-chat">
            <button
                type="button"
                className="niza-chat__trigger"
                aria-label={open ? "Fechar chat da Niza" : "Abrir chat da Niza"}
                aria-expanded={open}
                aria-controls="niza-chat-dialog"
                title={open ? "Fechar chat da Niza" : "Abrir chat da Niza"}
                onClick={alternarChat}
            >
                <span className="niza-chat__trigger-mark" aria-hidden="true">N</span>
            </button>

            {open && (
                <section
                    className="niza-chat__panel"
                    id="niza-chat-dialog"
                    role="dialog"
                    aria-modal="false"
                    aria-labelledby="niza-chat-title"
                >
                    <header className="niza-chat__header">
                        <div>
                            <p className="niza-chat__eyebrow">ORGANIZZ.AI</p>
                            <h2 id="niza-chat-title">Niza</h2>
                            <p>Planejamento financeiro pessoal</p>
                        </div>
                        <button
                            type="button"
                            className="niza-chat__close"
                            aria-label="Fechar chat da Niza"
                            onClick={() => setOpen(false)}
                        >
                            Fechar
                        </button>
                    </header>

                    {view === "loading" && (
                        <div className="niza-chat__state" role="status">Carregando seu perfil...</div>
                    )}

                    {view === "error" && (
                        <div className="niza-chat__state">
                            <p role="alert">{loadError}</p>
                            <button type="button" className="niza-chat__action" onClick={tentarCarregar}>
                                Tentar novamente
                            </button>
                        </div>
                    )}

                    {view === "onboarding" && (
                        <form className="niza-chat__onboarding" onSubmit={enviarOnboarding}>
                            <div className="niza-chat__progress-copy">Etapa {step + 1} de 2</div>
                            <div className="niza-chat__progress" aria-hidden="true">
                                <span style={{ width: step === 0 ? "50%" : "100%" }} />
                            </div>
                            {step === 0 ? (
                                <div className="niza-chat__fields">
                                    <label className="niza-chat__field">
                                        <span>Qual é sua principal meta financeira?</span>
                                        <textarea
                                            name="objetivo_financeiro"
                                            value={form.objetivo_financeiro}
                                            onChange={atualizarCampo}
                                            maxLength={300}
                                            minLength={3}
                                            placeholder="Ex.: montar uma reserva e organizar minhas despesas"
                                            required
                                        />
                                    </label>
                                    <label className="niza-chat__field">
                                        <span>Qual é sua renda mensal aproximada?</span>
                                        <select name="faixa_renda_mensal" value={form.faixa_renda_mensal} onChange={atualizarCampo} required>
                                            <option value="" disabled>Selecione uma faixa</option>
                                            {FAIXAS.map((faixa) => <option key={faixa.value} value={faixa.value}>{faixa.label}</option>)}
                                        </select>
                                    </label>
                                </div>
                            ) : (
                                <div className="niza-chat__fields">
                                    <label className="niza-chat__field">
                                        <span>Quanto você gasta por mês, aproximadamente?</span>
                                        <select name="faixa_despesas_mensais" value={form.faixa_despesas_mensais} onChange={atualizarCampo} required>
                                            <option value="" disabled>Selecione uma faixa</option>
                                            {FAIXAS.map((faixa) => <option key={faixa.value} value={faixa.value}>{faixa.label}</option>)}
                                        </select>
                                    </label>
                                    <fieldset className="niza-chat__field niza-chat__radio-group">
                                        <legend>Você tem dívidas atualmente?</legend>
                                        <label><input type="radio" name="possui_dividas" value="true" checked={form.possui_dividas === "true"} onChange={atualizarCampo} required /> Sim</label>
                                        <label><input type="radio" name="possui_dividas" value="false" checked={form.possui_dividas === "false"} onChange={atualizarCampo} required /> Não</label>
                                    </fieldset>
                                    <label className="niza-chat__field">
                                        <span>Como está sua reserva de emergência?</span>
                                        <select name="reserva_emergencia" value={form.reserva_emergencia} onChange={atualizarCampo} required>
                                            <option value="" disabled>Selecione uma opção</option>
                                            {RESERVAS.map((reserva) => <option key={reserva.value} value={reserva.value}>{reserva.label}</option>)}
                                        </select>
                                    </label>
                                    <label className="niza-chat__field">
                                        <span>Como você se sente sobre riscos em investimentos?</span>
                                        <select name="perfil_risco" value={form.perfil_risco} onChange={atualizarCampo} required>
                                            <option value="" disabled>Selecione uma opção</option>
                                            {PERFIS_RISCO.map((perfil) => <option key={perfil.value} value={perfil.value}>{perfil.label}</option>)}
                                        </select>
                                    </label>
                                </div>
                            )}
                            {formError && <p className="niza-chat__error" role="alert">{formError}</p>}
                            <footer className="niza-chat__form-actions">
                                {step === 1 && (
                                    <button type="button" className="niza-chat__secondary" onClick={() => setStep(0)}>
                                        Voltar
                                    </button>
                                )}
                                <button type="submit" className="niza-chat__action" disabled={saving}>
                                    {saving ? "Salvando..." : step === 0 ? "Continuar" : "Salvar e conversar"}
                                </button>
                            </footer>
                            <p className="niza-chat__privacy">Você pode editar essas respostas depois. Não informe senhas ou dados bancários.</p>
                        </form>
                    )}

                    {view === "chat" && (
                        <div className="niza-chat__conversation">
                            <div className="niza-chat__toolbar">
                                <span className={`niza-chat__status niza-chat__status--${socketStatus}`} role="status">
                                    {socketStatus === "ready" ? "Conectada" : socketStatus === "connecting" ? "Conectando..." : "Desconectada"}
                                </span>
                                <button type="button" className="niza-chat__edit" onClick={editarPerfil}>Editar perfil</button>
                            </div>
                            {connectionError && <p className="niza-chat__error" role="alert">{connectionError}</p>}
                            <div className="niza-chat__messages" aria-live="polite" aria-relevant="additions text">
                                {messages.length === 0 && (
                                    <div className="niza-chat__welcome">
                                        <p>Oi! Já conheço suas prioridades financeiras.</p>
                                        <p>O que você gostaria de organizar hoje?</p>
                                    </div>
                                )}
                                {messages.map((message) => (
                                    <div
                                        key={message.id}
                                        className={`niza-chat__message niza-chat__message--${message.sender}`}
                                    >
                                        {message.content || (message.sender === "bot" && generating ? "..." : "")}
                                    </div>
                                ))}
                                <div ref={bottomRef} />
                            </div>
                            <form className="niza-chat__composer" onSubmit={enviarMensagem}>
                                <label className="niza-chat__sr-only" htmlFor="niza-chat-input">Mensagem para a Niza</label>
                                <textarea
                                    id="niza-chat-input"
                                    value={draft}
                                    onChange={(event) => setDraft(event.target.value)}
                                    placeholder="Escreva sua mensagem..."
                                    rows={2}
                                    maxLength={2000}
                                    disabled={socketStatus !== "ready" || generating}
                                />
                                <button
                                    type="submit"
                                    className="niza-chat__send"
                                    aria-label="Enviar mensagem"
                                    title="Enviar mensagem"
                                    disabled={!draft.trim() || socketStatus !== "ready" || generating}
                                >
                                    Enviar
                                </button>
                            </form>
                        </div>
                    )}
                </section>
            )}
        </div>
    )
}