import './Task.css';


export default function Task() {
    return (
        <div className="container">
            <div className="Task">
                <h2 className="Tasktitle">Task</h2>
                <input className="TaskInput" type="checkbox" placeholder="Add a new task..." />
            </div>
            <div className="Task">
                <h2 className="Tasktitle">Task</h2>
                <input className="TaskInput" type="checkbox" placeholder="Add a new task..." />
            </div>
            <div className="Task">
                <h2 className="Tasktitle">Task</h2>
                <input className="TaskInput" type="checkbox" placeholder="Add a new task..." />
            </div>
        </div>
    );
}