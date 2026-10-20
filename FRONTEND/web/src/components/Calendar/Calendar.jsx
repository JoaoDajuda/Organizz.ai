// CalendarGrid.jsx
import FullCalendar from '@fullcalendar/react';
import dayGridPlugin from '@fullcalendar/daygrid';
import timeGridPlugin from '@fullcalendar/timegrid';
import interactionPlugin from '@fullcalendar/interaction';
import './fullcalendar-overrides.css';
import { useState } from 'react';

const MINUTOS_NO_DIA = 24 * 60;

function dataLocal(data, diaInteiro = false) {
  if (!data) return null;
  const valor = diaInteiro || !data.includes('T') ? `${data.slice(0, 10)}T00:00:00` : data;
  const parsed = new Date(valor);
  return Number.isNaN(parsed.getTime()) ? null : parsed;
}

function formatarDataSelecionada(data) {
  const [ano, mes, dia] = data.split('-').map(Number);
  return new Intl.DateTimeFormat('pt-BR', {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  }).format(new Date(ano, mes - 1, dia));
}

function formatarMinutos(minutos) {
  const valor = Math.min(minutos, MINUTOS_NO_DIA - 1);
  const horas = Math.floor(valor / 60);
  const restante = valor % 60;
  return `${String(horas).padStart(2, '0')}:${String(restante).padStart(2, '0')}`;
}

function formatarDuracao(minutos) {
  const horas = Math.floor(minutos / 60);
  const restante = minutos % 60;
  if (!horas) return `${restante} min`;
  return restante ? `${horas} h ${restante} min` : `${horas} h`;
}

function intervalosDoDia(agendas, dataSelecionada) {
  const inicioDia = new Date(`${dataSelecionada}T00:00:00`);
  const fimDia = new Date(inicioDia);
  fimDia.setDate(fimDia.getDate() + 1);

  return agendas.flatMap((agenda) => {
    const diaInteiro = agenda.dia_inteiro || !agenda.data?.includes('T');
    const inicio = dataLocal(agenda.data, diaInteiro);
    if (!inicio) return [];

    let fim = dataLocal(agenda.data_fim, diaInteiro);
    if (!fim) {
      fim = new Date(inicio);
      fim.setMinutes(fim.getMinutes() + (diaInteiro ? MINUTOS_NO_DIA : 60));
    }
    if (fim <= inicio || fim <= inicioDia || inicio >= fimDia) return [];

    const inicioVisivel = Math.max(inicio.getTime(), inicioDia.getTime());
    const fimVisivel = Math.min(fim.getTime(), fimDia.getTime());
    return [{
      id: agenda.id_agenda,
      titulo: agenda.titulo,
      status: agenda.status,
      inicio: Math.max(0, Math.floor((inicioVisivel - inicioDia.getTime()) / 60000)),
      fim: Math.min(MINUTOS_NO_DIA, Math.ceil((fimVisivel - inicioDia.getTime()) / 60000)),
    }];
  }).sort((a, b) => a.inicio - b.inicio || a.fim - b.fim);
}

function posicionarIntervalos(intervalos) {
  const finaisDasFaixas = [];
  return intervalos.map((intervalo) => {
    let faixa = finaisDasFaixas.findIndex((fim) => fim <= intervalo.inicio);
    if (faixa === -1) faixa = finaisDasFaixas.length;
    finaisDasFaixas[faixa] = intervalo.fim;
    return { ...intervalo, faixa };
  });
}

function minutosOcupados(intervalos) {
  const unidos = [];
  intervalos.forEach(({ inicio, fim }) => {
    const ultimo = unidos[unidos.length - 1];
    if (ultimo && inicio <= ultimo.fim) {
      ultimo.fim = Math.max(ultimo.fim, fim);
    } else {
      unidos.push({ inicio, fim });
    }
  });
  return unidos.reduce((total, intervalo) => total + intervalo.fim - intervalo.inicio, 0);
}

export function DayUsageDashboard({ agendas, dataSelecionada }) {
  const intervalos = intervalosDoDia(agendas, dataSelecionada);
  const intervalosPosicionados = posicionarIntervalos(intervalos);
  const ocupados = minutosOcupados(intervalos);
  const livres = MINUTOS_NO_DIA - ocupados;
  const percentualOcupado = Math.round((ocupados / MINUTOS_NO_DIA) * 100);
  const faixas = Math.max(1, ...intervalosPosicionados.map(({ faixa }) => faixa + 1));

  return (
    <section className="day-usage" aria-labelledby="day-usage-title">
      <div className="day-usage__header">
        <div>
          <p className="day-usage__eyebrow">DISTRIBUIÇÃO DO DIA</p>
          <h2 id="day-usage-title">{formatarDataSelecionada(dataSelecionada)}</h2>
        </div>
        <div className="day-usage__summary">
          <strong>{formatarDuracao(ocupados)}</strong>
          <span>ocupadas de 24 h</span>
        </div>
      </div>

      <div className="day-usage__totals">
        <span>{formatarDuracao(livres)} livres</span>
        <span>{percentualOcupado}% do dia</span>
      </div>
      <div
        className="day-usage__progress"
        role="progressbar"
        aria-label="Percentual do dia ocupado"
        aria-valuemin="0"
        aria-valuemax="100"
        aria-valuenow={percentualOcupado}
      >
        <span style={{ width: `${(ocupados / MINUTOS_NO_DIA) * 100}%` }} />
      </div>

      <div
        className="day-usage__timeline"
        style={{ height: `${Math.max(64, faixas * 28 + 12)}px` }}
        role="img"
        aria-label={`Agenda de 00:00 a 23:59. ${intervalos.length} tarefas para este dia.`}
      >
        {intervalosPosicionados.map((intervalo) => (
          <div
            className={`day-usage__event${intervalo.status === 'concluida' ? ' day-usage__event--done' : ''}`}
            key={intervalo.id}
            title={`${formatarMinutos(intervalo.inicio)}-${formatarMinutos(intervalo.fim)} ${intervalo.titulo}`}
            style={{
              left: `${(intervalo.inicio / MINUTOS_NO_DIA) * 100}%`,
              width: `${((intervalo.fim - intervalo.inicio) / MINUTOS_NO_DIA) * 100}%`,
              top: `${intervalo.faixa * 28 + 6}px`,
            }}
          >
            {intervalo.titulo}
          </div>
        ))}
        {intervalos.length === 0 && <span className="day-usage__empty">Sem tarefas neste dia</span>}
      </div>
      <div className="day-usage__axis" aria-hidden="true">
        {Array.from({ length: 8 }, (_, index) => index * 3).map((hora) => (
          <span key={hora} style={{ left: `${(hora / 24) * 100}%` }}>
            {String(hora).padStart(2, '0')}:00
          </span>
        ))}
        <span className="day-usage__axis-end">23:59</span>
      </div>

      {intervalos.length > 0 && (
        <ul className="day-usage__list">
          {intervalos.map((intervalo) => (
            <li key={intervalo.id}>
              <time>{formatarMinutos(intervalo.inicio)}–{formatarMinutos(intervalo.fim)}</time>
              <span>{intervalo.titulo}</span>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

function hojeLocal() {
  const hoje = new Date();
  return `${hoje.getFullYear()}-${String(hoje.getMonth() + 1).padStart(2, '0')}-${String(hoje.getDate()).padStart(2, '0')}`;
}

function chaveDataLocal(data) {
  if (!data) return '';
  if (/^\d{4}-\d{2}-\d{2}/.test(data)) return data.slice(0, 10);
  const parsed = new Date(data);
  if (Number.isNaN(parsed.getTime())) return '';
  return `${parsed.getFullYear()}-${String(parsed.getMonth() + 1).padStart(2, '0')}-${String(parsed.getDate()).padStart(2, '0')}`;
}

function CalendarGrid({ agendas, onCreateAgenda, onDeleteAgenda, onDataSelect }) {
  const [error, setError] = useState('');

  const events = agendas.map((agenda) => ({
    id: String(agenda.id_agenda),
    title: agenda.titulo,
    start: agenda.data,
    end: agenda.data_fim || undefined,
    allDay: agenda.dia_inteiro || !agenda.data?.includes('T'),
  }));

  const handleSelect = async (info) => {
    onDataSelect(chaveDataLocal(info.startStr));
    const titulo = prompt('Título do evento:')?.trim();
    if (!titulo) return;

    setError('');
    try {
      await onCreateAgenda({
        titulo,
        data: info.startStr,
        data_fim: info.endStr || null,
        dia_inteiro: info.allDay,
      });
    } catch (requestError) {
      setError(requestError.message);
    }
  };

  const handleEventClick = async (info) => {
    if (confirm(`Remover "${info.event.title}"?`)) {
      setError('');
      try {
        await onDeleteAgenda(info.event.id);
      } catch (requestError) {
        setError(requestError.message);
      }
    }
  };

  return (
    <div className="calendar-wrapper">
      {error && <p role="alert">{error}</p>}
      <FullCalendar
        plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
        height={450}
        initialView="dayGridMonth"
        locale="pt-br"
        events={events}
        selectable={true}
        dateClick={(info) => onDataSelect(chaveDataLocal(info.dateStr))}
        select={handleSelect}
        eventClick={handleEventClick}
        slotMinTime="00:00:00"
        slotMaxTime="24:00:00"
        slotDuration="00:30:00"
        scrollTime="00:00:00"
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