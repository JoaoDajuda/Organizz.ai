import './Task.css';
import { LuCircleAlert, LuCheckCheck } from "react-icons/lu";
import { FaTrash } from "react-icons/fa";
import { useState } from 'react';

function formatarData(data) {
    if (data === "sem-data") return "Data não definida";

    const [ano, mes, dia] = data.split("-").map(Number);
    return new Intl.DateTimeFormat("pt-BR", {
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric",
    }).format(new Date(ano, mes - 1, dia));
}

function formatarHora(data) {
    if (!data) return null;
    const valor = /^\d{4}-\d{2}-\d{2}$/.test(data) ? `${data}T00:00:00` : data;
    const dataHora = new Date(valor);
    if (Number.isNaN(dataHora.getTime())) return null;
    return new Intl.DateTimeFormat("pt-BR", {
        hour: "2-digit",
        minute: "2-digit",
        hourCycle: "h23",
    }).format(dataHora);
}

function formatarHorario(agenda) {
    if (agenda.dia_inteiro || !agenda.data?.includes("T")) return "00:00–23:59";

    const inicio = formatarHora(agenda.data);
    if (!inicio) return "Horário não definido";

    let fim = formatarHora(agenda.data_fim);
    if (!fim) {
        const dataFim = new Date(agenda.data);
        dataFim.setHours(dataFim.getHours() + 1);
        fim = formatarHora(dataFim.toISOString());
    }

    return `${inicio}–${fim}`;
}

export default function Task({ agendas, onUpdateStatus, onDeleteAgenda }) {
    const [proceed, setProceed] = useState(false);
    const [error, setError] = useState("");
    const agendasPorDia = agendas.reduce((grupos, agenda) => {
        const data = typeof agenda.data === "string" ? agenda.data.slice(0, 10) : "";
        const chave = /^\d{4}-\d{2}-\d{2}$/.test(data) ? data : "sem-data";
        grupos[chave] ??= [];
        grupos[chave].push(agenda);
        return grupos;
    }, {});
    const diasOrdenados = Object.keys(agendasPorDia).sort((a, b) => {
        if (a === "sem-data") return 1;
        if (b === "sem-data") return -1;
        return a.localeCompare(b);
    });

    async function alternarStatus(agenda) {
        setError("");
        try {
            await onUpdateStatus(
                agenda.id_agenda,
                agenda.status === "concluida" ? "pendente" : "concluida",
            );
        } catch (requestError) {
            setError(requestError.message);
        }
    }

    async function excluir(agenda) {
        setError("");
        try {
            await onDeleteAgenda(agenda.id_agenda);
        } catch (requestError) {
            setError(requestError.message);
        }
    }

    return (
        <div className="container">
            {agendas.length === 0 && <p>Nenhuma tarefa agendada.</p>}
            {diasOrdenados.map((dia) => (
                <section className="TaskDayGroup" key={dia}>
                    <h3 className="TaskDayTitle">{formatarData(dia)}</h3>
                    {agendasPorDia[dia].map((agenda) => {
                        const completed = agenda.status === "concluida";
                        return (
                            <div
                                className="Task"
                                key={agenda.id_agenda}
                                style={{ textDecoration: completed ? 'line-through' : 'none' }}
                            >
                                <input
                                    type="checkbox"
                                    checked={completed}
                                    disabled={!proceed}
                                    onChange={() => alternarStatus(agenda)}
                                    aria-label={`Marcar ${agenda.titulo} como ${completed ? "pendente" : "concluída"}`}
                                />
                                {completed ? <LuCheckCheck /> : <LuCircleAlert />}
                                <div className="TaskTitle">
                                    <span>{agenda.titulo}</span>
                                    <small className="TaskTime">{formatarHorario(agenda)}</small>
                                </div>
                                <button
                                    className="TaskDelete"
                                    type="button"
                                    disabled={!proceed}
                                    aria-label={`Excluir ${agenda.titulo}`}
                                    onClick={() => excluir(agenda)}
                                >
                                    <FaTrash />
                                </button>
                            </div>
                        );
                    })}
                </section>
            ))}
            {error && <p role="alert">{error}</p>}
            <button className="Confirm" onClick={() => setProceed(!proceed)}>
                {proceed ? "Sair do modo de edição" : "Modificar"}
            </button>
        </div>
    );
}