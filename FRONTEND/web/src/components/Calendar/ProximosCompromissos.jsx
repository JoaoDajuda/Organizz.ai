import "./ProximosCompromissos.css";

/**
 * @param {Array<{id, titulo, categoria, horario}>} compromissos
 */
export default function ProximosCompromissos({ compromissos = [] }) {
  return (
    <div className="proximos">
      <h3 className="proximos__title">Próximos compromissos</h3>

      <ul className="proximos__list">
        {compromissos.map((c) => (
          <li key={c.id} className="proximos__item">
            <span
              className={`proximos__icon proximos__icon--${c.categoria}`}
            />
            <div className="proximos__info">
              <span className="proximos__nome">{c.titulo}</span>
              <span className="proximos__categoria">{c.categoria}</span>
            </div>
            <span className="proximos__horario">{c.horario}</span>
          </li>
        ))}

        {compromissos.length === 0 && (
          <li className="proximos__vazio">Nenhum compromisso agendado.</li>
        )}
      </ul>
    </div>
  );
}
