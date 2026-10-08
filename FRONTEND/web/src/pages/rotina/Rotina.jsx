import CalendarGrid from "../../components/Calendar/Calendar.jsx"
import Task from "../../components/Task/Task.jsx"
import './Rotina.css';

export default function Rotina() {
    return (
        <div className="PaginaRotina">
            <div className="rotinaLeft">
                <CalendarGrid />
            </div>
            <div className="rotinaRight">
                <Task />
            </div>
        </div>
    )
}