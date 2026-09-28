// CalendarGrid.jsx
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import './fullcalendar-overrides.css';
import { useState } from 'react';

const mockEvents = [
  { id: '1', title: 'Reunião de equipe', start: '2026-09-22T10:00:00', end: '2026-09-22T11:00:00' },
  { id: '2', title: 'Entrega de relatório', start: '2026-09-25', allDay: true },
  { id: '3', title: 'Revisão de orçamento', start: '2026-09-23T14:00:00', end: '2026-09-23T15:30:00', color: '#C9A94D' },
];

function CalendarGrid() {
  const [events, setEvents] = useState(mockEvents);

  const handleSelect = (info) => {
    const title = prompt('Título do evento:'); // troque pelo Modal depois
    if (title) {
      setEvents([...events, {
        id: String(Date.now()),
        title,
        start: info.startStr,
        end: info.endStr,
        allDay: info.allDay,
      }]);
    }
  };

  const handleEventClick = (info) => {
    if (confirm(`Remover "${info.event.title}"?`)) {
      setEvents(events.filter(ev => ev.id !== info.event.id));
    }
  };

  return (
    <div className="calendar-wrapper">
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        initialView="dayGridMonth"
        locale="pt-br"
        events={events}
        selectable={true}
        select={handleSelect}
        eventClick={handleEventClick}
        headerToolbar={{
          left: 'prev,next today',
          center: 'title',
          right: 'dayGridMonth,timeGridWeek,timeGridDay',
        }}
      />
    </div>
  );
}

export default CalendarGrid;