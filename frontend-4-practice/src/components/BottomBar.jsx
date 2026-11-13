import { formatBottomBar } from '../utils/date.js';

export default function BottomBar({ selectedDate, selectedTime }) {
  const ready = selectedDate && selectedTime;

  return (
    <section className="actions">
      <div className="container actions__inner">
        <div className="actions__info">
          <p className="actions__label">Вы выбрали</p>
          <p className="actions__value">
            {ready ? formatBottomBar(selectedDate, selectedTime) : 'Дата и время не выбраны'}
          </p>
        </div>
        <div className="actions__buttons">
          <button className="btn btn--outline" type="button">Назад</button>
          <button className="btn btn--primary" type="button" disabled={!ready}>Далее</button>
        </div>
      </div>
    </section>
  );
}