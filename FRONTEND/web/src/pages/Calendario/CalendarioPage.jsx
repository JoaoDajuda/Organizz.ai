import { useEffect, useMemo, useState } from "react";
import Sidebar from "../../components/Layout/Sidebar";
import Header from "../../components/Layout/Header";
import CalendarGrid from "../../components/Calendar/CalendarGrid";
import AgendaList from "../../components/Calendar/AgendaList";
import ProximosCompromissos from "../../components/Calendar/ProximosCompromissos";
import "./CalendarioPage.css";

// -----------------------------------------------------------------
// Dados de exemplo — troque pelas chamadas reais à sua API (FastAPI)
// quando conectar este componente ao backend do OrganizzAI/Organiza.
// Sugestão de endpoints: GET /agenda?data=YYYY-MM-DD
//                         GET /agenda/mes?ano=&mes=
//                         GET /compromissos/proximos
// -----------------------------------------------------------------
const EVENTOS_POR_DIA_MOCK = {
  "2025-05-08": ["tarefas"],
  "2025-05-09": ["tarefas", "eventos"],
  "2025-05-14": ["treinos", "eventos"],
  "2025-05-15": ["tarefas"],
  "2025-05-19": ["tarefas"],
  "2025-05-20": ["tarefas", "treinos"],
  "2025-05-21": ["tarefas"],
  "2025-05-22": ["treinos", "financas"],
  "2025-05-26": ["financas"],
  "2025-05-28": ["tarefas", "treinos", "eventos"],
  "2025-05-29": ["tarefas"],
  "2025-05-30": ["tarefas", "financas"],
};

const AGENDA_DIA_MOCK = [
  { id: "1", horario: "07:00", titulo: "Acordar e Meditar", categoria: "rotina", concluido: false },
  { id: "2", horario: "07:30", titulo: "Leitura", categoria: "rotina", concluido: false },
  { id: "3", horario: "08:00", titulo: "Café da Manhã", categoria: "alimentacao", concluido: false },
  { id: "4", horario: "09:00", titulo: "Estudar para o TCC", categoria: "estudos", concluido: false },
  { id: "5", horario: "12:30", titulo: "Almoço", categoria: "alimentacao", concluido: false },
  { id: "6", horario: "14:00", titulo: "Desenvolver Projeto", categoria: "tcc", concluido: false },
  { id: "7", horario: "16:00", titulo: "Treino – Peito e Tríceps", categoria: "academia", concluido: false },
  { id: "8", horario: "19:30", titulo: "Reunião de TCC", categoria: "online", concluido: false },
  { id: "9", horario: "21:00", titulo: "Revisar Anotações", categoria: "estudos", concluido: false },
  { id: "10", horario: "22:30", titulo: "Dormir", categoria: "rotina", concluido: false },
];

const PROXIMOS_MOCK = [
  { id: "1", titulo: "Treino – Peito e Tríceps", categoria: "academia", horario: "16:00" },
  { id: "2", titulo: "Reunião de TCC", categoria: "online", horario: "19:30" },
  { id: "3", titulo: "Pagamento do Curso", categoria: "financas", horario: "22/05" },
];

export default function CalendarioPage({ userName = "Usuário" }) {
  const [mesAtual, setMesAtual] = useState(new Date(2025, 4, 1));
  const [diaSelecionado, setDiaSelecionado] = useState(new Date(2025, 4, 19));
  const [agendaDoDia, setAgendaDoDia] = useState(AGENDA_DIA_MOCK);

  // Quando conectar ao backend: refazer o fetch da agenda toda vez
  // que o dia selecionado mudar.
  useEffect(() => {
    // Exemplo:
    // const chave = diaSelecionado.toISOString().slice(0, 10);
    // fetch(`/api/agenda?data=${chave}`)
    //   .then((res) => res.json())
    //   .then(setAgendaDoDia);
  }, [diaSelecionado]);

  function irParaMesAnterior() {
    setMesAtual((atual) => new Date(atual.getFullYear(), atual.getMonth() - 1, 1));
  }

  function irParaMesSeguinte() {
    setMesAtual((atual) => new Date(atual.getFullYear(), atual.getMonth() + 1, 1));
  }

  function alternarConcluido(id) {
    setAgendaDoDia((itens) =>
      itens.map((item) =>
        item.id === id ? { ...item, concluido: !item.concluido } : item
      )
    );
  }

  const frase = useMemo(
    () => "Disciplina hoje, liberdade amanhã.",
    []
  );

  return (
    <div className="calendario-page">
      <Sidebar />

      <div className="calendario-page__content">
        <Header userName={userName} />

        <main className="calendario-page__main">
          <div className="calendario-page__heading">
            <h1 className="calendario-page__title">Calendário &amp; Agenda</h1>
            <p className="calendario-page__frase">&ldquo;{frase}&rdquo;</p>
          </div>

          <div className="calendario-page__grid">
            <section className="calendario-page__coluna-esquerda">
              <CalendarGrid
                mesAtual={mesAtual}
                diaSelecionado={diaSelecionado}
                eventosPorDia={EVENTOS_POR_DIA_MOCK}
                onSelecionarDia={setDiaSelecionado}
                onMesAnterior={irParaMesAnterior}
                onMesSeguinte={irParaMesSeguinte}
              />
              <ProximosCompromissos compromissos={PROXIMOS_MOCK} />
            </section>

            <section className="calendario-page__coluna-direita">
              <AgendaList
                data={diaSelecionado}
                itens={agendaDoDia}
                onToggleConcluido={alternarConcluido}
              />
            </section>
          </div>
        </main>
      </div>
    </div>
  );
}
