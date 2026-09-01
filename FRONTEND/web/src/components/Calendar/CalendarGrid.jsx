import "./CalendarGrid.css";

const DIAS_SEMANA = ["DOM", "SEG", "TER", "QUA", "QUI", "SEX", "SÁB"];

const LEGENDA = [
  { categoria: "tarefas", label: "Tarefas" },
  { categoria: "treinos", label: "Treinos" },
  { categoria: "financas", label: "Finanças" },
  { categoria: "eventos", label: "Eventos" },
];

/**
 * @param {Date} mesAtual - qualquer data dentro do mês exibido
 * @param {Date} diaSelecionado - dia atualmente selecionado
 * @param {Object} eventosPorDia - ex: { "2025-05-16": ["tarefas", "financas"] }
 * @param {(data: Date) => void} onSelecionarDia
 * @param {() => void} onMesAnterior
 * @param {() => void} onMesSeguinte
 */
export default function CalendarGrid({
  mesAtual,
  diaSelecionado,
  eventosPorDia = {},
  onSelecionarDia,
  onMesAnterior,
  onMesSeguinte,
}) {
  const nomeMes = mesAtual
    .toLocaleDateString("pt-BR", { month: "long", year: "numeric" })
    .toUpperCase();

  const semanas = gerarSemanas(mesAtual);

  function chaveISO(data) {
    return data.toISOString().slice(0, 10);
  }

  function ehMesAtual(data) {
    return data.getMonth() === mesAtual.getMonth();
  }

  function ehSelecionado(data) {
    return (
      diaSelecionado && chaveISO(data) === chaveISO(diaSelecionado)
    );
  }

  return (
    <div className="calendar-grid">
      <div className="calendar-grid__header">
        <button
          className="calendar-grid__nav-btn"
          onClick={onMesAnterior}
          aria-label="Mês anterior"
        >
          ‹
        </button>
        <h2 className="calendar-grid__title">{nomeMes}</h2>
        <button
          className="calendar-grid__nav-btn"
          onClick={onMesSeguinte}
          aria-label="Próximo mês"
        >
          ›
        </button>
      </div>

      <div className="calendar-grid__weekdays">
        {DIAS_SEMANA.map((d) => (
          <span key={d}>{d}</span>
        ))}
      </div>

      <div className="calendar-grid__days">
        {semanas.flat().map((data) => {
          const categorias = eventosPorDia[chaveISO(data)] || [];
          return (
            <button
              key={chaveISO(data)}
              className={
                "calendar-grid__day" +
                (!ehMesAtual(data) ? " calendar-grid__day--fora-do-mes" : "") +
                (ehSelecionado(data) ? " calendar-grid__day--selecionado" : "")
              }
              onClick={() => onSelecionarDia?.(data)}
            >
              <span className="calendar-grid__day-number">
                {data.getDate()}
              </span>
              {categorias.length > 0 && (
                <span className="calendar-grid__day-dots">
                  {categorias.map((cat, i) => (
                    <span
                      key={i}
                      className={`calendar-grid__dot calendar-grid__dot--${cat}`}
                    />
                  ))}
                </span>
              )}
            </button>
          );
        })}
      </div>

      <div className="calendar-grid__legend">
        {LEGENDA.map((item) => (
          <span key={item.categoria} className="calendar-grid__legend-item">
            <span
              className={`calendar-grid__dot calendar-grid__dot--${item.categoria}`}
            />
            {item.label}
          </span>
        ))}
      </div>
    </div>
  );
}

// Gera a matriz de semanas (6 linhas x 7 dias) incluindo dias
// do mês anterior/seguinte para preencher a grade, igual ao mockup.
function gerarSemanas(mesAtual) {
  const primeiroDiaMes = new Date(
    mesAtual.getFullYear(),
    mesAtual.getMonth(),
    1
  );
  const inicioGrade = new Date(primeiroDiaMes);
  inicioGrade.setDate(inicioGrade.getDate() - primeiroDiaMes.getDay());

  const semanas = [];
  const cursor = new Date(inicioGrade);

  for (let semana = 0; semana < 6; semana++) {
    const dias = [];
    for (let dia = 0; dia < 7; dia++) {
      dias.push(new Date(cursor));
      cursor.setDate(cursor.getDate() + 1);
    }
    semanas.push(dias);
  }
  return semanas;
}
