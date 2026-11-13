import { MONTHS_GENITIVE } from '../utils/date.js';

export default function TimeSlots({ selectedDate, selectedTime, slots, isLoading, error, onSelectTime }) {
  const dateLabel = selectedDate
    ? `${selectedDate.getDate()} ${MONTHS_GENITIVE[selectedDate.getMonth()]}`
    : 'Выберите дату в календаре';

  if (isLoading) {
    return (
      <div className="card time-panel">
        <h2 className="time-panel__title">Свободное время</h2>
        <p className="time-panel__date">{dateLabel}</p>
        <div style={{ padding: '40px', textAlign: 'center', color: '#666' }}>
          Загрузка слотов...
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card time-panel">
        <h2 className="time-panel__title">Свободное время</h2>
        <div style={{ padding: '40px', textAlign: 'center', color: '#e53e3e' }}>
          {error}
        </div>
      </div>
    );
  }

  return (
    <div className="card time-panel">
      <h2 className="time-panel__title">Свободное время</h2>
      <p className="time-panel__date">{dateLabel}</p>
      <div className="time-slots">
        {slots.map(slot => {
          const classes = ['slot'];
          if (!slot.available) classes.push('slot--occupied');
          if (selectedTime === slot.time) classes.push('slot--selected');

          return (
            <button
              key={slot.time}
              type="button"
              className={classes.join(' ')}
              disabled={!slot.available}
              onClick={() => onSelectTime(slot.time)}
            >
              {!slot.available ? <>{slot.time}<small>занято</small></> : slot.time}
            </button>
          );
        })}
      </div>
    </div>
  );
}