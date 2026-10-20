import { useEffect, useState } from "react"
import CalendarGrid, { DayUsageDashboard } from "../../components/Calendar/Calendar.jsx"
import Task from "../../components/Task/Task.jsx"
import {
    AtualizarStatusAgenda,
    CriarAgenda,
    ExcluirAgenda,
    ListarAgendas,
} from "../../services/api.js"
import './Rotina.css';

function dataAtualLocal() {
    const hoje = new Date()
    return `${hoje.getFullYear()}-${String(hoje.getMonth() + 1).padStart(2, '0')}-${String(hoje.getDate()).padStart(2, '0')}`
}

export default function Rotina() {
    const [agendas, setAgendas] = useState([])
    const [carregando, setCarregando] = useState(true)
    const [erro, setErro] = useState("")
    const [dataSelecionada, setDataSelecionada] = useState(dataAtualLocal)

    useEffect(() => {
        let ativo = true

        ListarAgendas()
            .then((dados) => {
                if (ativo) setAgendas(dados)
            })
            .catch((error) => {
                if (ativo) setErro(error.message)
            })
            .finally(() => {
                if (ativo) setCarregando(false)
            })

        return () => {
            ativo = false
        }
    }, [])

    async function criarAgenda(dados) {
        setErro("")
        try {
            const criada = await CriarAgenda(dados)
            setAgendas((atuais) => [...atuais, criada])
            return criada
        } catch (error) {
            setErro(error.message)
            throw error
        }
    }

    async function atualizarStatus(idAgenda, status) {
        setErro("")
        try {
            const atualizada = await AtualizarStatusAgenda(idAgenda, status)
            setAgendas((atuais) => atuais.map((agenda) => (
                agenda.id_agenda === atualizada.id_agenda ? atualizada : agenda
            )))
        } catch (error) {
            setErro(error.message)
            throw error
        }
    }

    async function excluirAgenda(idAgenda) {
        setErro("")
        try {
            await ExcluirAgenda(idAgenda)
            setAgendas((atuais) => atuais.filter((agenda) => agenda.id_agenda !== Number(idAgenda)))
        } catch (error) {
            setErro(error.message)
            throw error
        }
    }

    return (
        <div className="PaginaRotina">
            <div className="rotinaTop">
                <div className="rotinaLeft">
                    <CalendarGrid
                        agendas={agendas}
                        onCreateAgenda={criarAgenda}
                        onDeleteAgenda={excluirAgenda}
                        onDataSelect={setDataSelecionada}
                    />
                </div>
                <div className="rotinaRight">
                    {carregando && <p role="status">Carregando tarefas...</p>}
                    {erro && <p role="alert">{erro}</p>}
                    <Task
                        agendas={agendas}
                        onUpdateStatus={atualizarStatus}
                        onDeleteAgenda={excluirAgenda}
                    />
                </div>
            </div>
            <DayUsageDashboard agendas={agendas} dataSelecionada={dataSelecionada} />
        </div>
    )
}