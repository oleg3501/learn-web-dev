import { MONTHS_NOMINATIVE, buildCalendarGrid, isDateSelectable, compareDates } from '../utils/date.js';

export default function Calendar({ viewDate, selectedDate, onSelectDay, onPrev, onNext }) {
  const year = viewDate.getFullYear();
  const month = viewDate.getMonth();
  const weeks = buildCalendarGrid(year, month);
  const today = new Date();

  return (
    <div className="card calendar">
      <div className="calendar__header">
        <h2 className="calendar__title">{MONTHS_NOMINATIVE[month]} {year}</h2>
        <div className="calendar__nav">
          <button className="calendar__btn" type="button" onClick={onPrev}>‹</button>
          <button className="calendar__btn" type="button" onClick={onNext}>›</button>
        </div>
      </div>

      <div className="calendar__weekdays">
        <span>Пн</span><span>Вт</span><span>Ср</span><span>Чт</span>
        <span>Пт</span><span>Сб</span><span>Вс</span>
      </div>

      <div className="calendar__days">
        {weeks.map((week, wi) =>
          week.map((day, di) => {
            const key = `${wi}-${di}`;
            if (day === null) return <div key={key} />;

            const dayDate = new Date(year, month, day);
            const isToday = compareDates(dayDate, today) === 0;
            const isSelected = selectedDate &&
              selectedDate.getFullYear() === year &&
              selectedDate.getMonth() === month &&
              selectedDate.getDate() === day;
            const isPast = !isDateSelectable(day, month, year, today);

            const classes = ['day'];
            if (isToday) classes.push('day--today');
            if (isSelected) classes.push('day--selected');
            if (isPast) classes.push('day--past');

            return (
              <button
                key={key}
                type="button"
                className={classes.join(' ')}
                disabled={isPast}
                onClick={() => onSelectDay(dayDate)}
              >
                {day}
              </button>
            );
          })
        )}
      </div>

      <div className="calendar__legend">
        <span className="legend-item">
          <span className="legend-dot legend-dot--selected" /> Выбрано
        </span>
        <span className="legend-item">
          <span className="legend-dot legend-dot--today" /> Сегодня
        </span>
      </div>
    </div>
  );
}