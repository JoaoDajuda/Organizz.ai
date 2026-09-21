import CalendarGrid from "../../components/Calendar/Calendar.jsx"
import './Rotina.css';

export default function Rotina() {
    return (
        <div className="PaginaRotina">
            <div className="agenda-left">
                <CalendarGrid />
                {/* <ProximosCompromissos /> entra aqui depois */}
            </div>
            <div className="agenda-right">
                {/* <AgendaDoDia /> entra aqui depois */}
            </div>
        </div>
    )
}