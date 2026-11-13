import { MONTHS_GENITIVE, getSlotsForDate } from '../utils/date.js';

export default function TimeSlots({ selectedDate, selectedTime, onSelectTime }) {
  const slots = selectedDate ? getSlotsForDate(selectedDate) : [];

  return (
    <div className="card time-panel">
      <h2 className="time-panel__title">Свободное время</h2>
      <p className="time-panel__date">
        {selectedDate
          ? `${selectedDate.getDate()} ${MONTHS_GENITIVE[selectedDate.getMonth()]}`
          : 'Выберите дату в календаре'}
      </p>

      <div className="time-slots">
        {slots.map(slot => {
          const classes = ['slot'];
          if (slot.isOccupied) classes.push('slot--occupied');
          if (selectedTime === slot.time) classes.push('slot--selected');

          return (
            <button
              key={slot.time}
              type="button"
              className={classes.join(' ')}
              disabled={slot.isOccupied}
              onClick={() => onSelectTime(slot.time)}
            >
              {slot.isOccupied ? (
                <>{slot.time}<small>занято</small></>
              ) : slot.time}
            </button>
          );
        })}
      </div>
    </div>
  );
}