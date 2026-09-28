import "./AgendaList.css";

/**
 * @param {Date} data - dia exibido no cabeçalho
 * @param {Array<{id, horario, titulo, categoria, concluido}>} itens
 * @param {(id: string) => void} onToggleConcluido
 */
export default function AgendaList({ data, itens = [], onToggleConcluido }) {
  const dataFormatada = data
    .toLocaleDateString("pt-BR", {
      day: "2-digit",
      month: "long",
      weekday: "long",
    })
    .toUpperCase();

  return (
    <div className="agenda-list">
      <h2 className="agenda-list__title">AGENDA — {dataFormatada}</h2>

      <ul className="agenda-list__items">
        {itens.map((item) => (
          <li key={item.id} className="agenda-list__item">
            <span className="agenda-list__horario">{item.horario}</span>

            <span
              className={`agenda-list__icon agenda-list__icon--${item.categoria}`}
            />

            <div className="agenda-list__texto">
              <span className="agenda-list__nome">{item.titulo}</span>
              <span className="agenda-list__categoria">{item.categoria}</span>
            </div>

            <input
              type="checkbox"
              className="agenda-list__checkbox"
              checked={item.concluido}
              onChange={() => onToggleConcluido?.(item.id)}
              aria-label={`Marcar "${item.titulo}" como concluído`}
            />
          </li>
        ))}

        {itens.length === 0 && (
          <li className="agenda-list__vazio">
            Nenhum compromisso para este dia. Que tal planejar algo?
          </li>
        )}
      </ul>
    </div>
  );
}
