// Rotina.jsx — CORRIGIDO
import CalendarGrid from "../../components/Calendar/Calendar";
import './Rotina.css';

function Rotina() {
    return (
        <div className="agenda-page">
            <div className="agenda-left">
                <CalendarGrid />
                <ProximosCompromissos />  {/* componente novo, lista simples */}
            </div>
            <div className="agenda-right">
                <AgendaDoDia />  {/* lista de horários, como no mockup */}
            </div>
        </div>
    );
}

export default Rotina;