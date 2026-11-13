import { useState } from 'react';
import Header from './components/Header.jsx';
import Stepper from './components/Stepper.jsx';
import Calendar from './components/Calendar.jsx';
import TimeSlots from './components/TimeSlots.jsx';
import BottomBar from './components/BottomBar.jsx';
import Footer from './components/Footer.jsx';

export default function App() {
  // Состояние (аналог глобальных переменных из нативной версии)
  const [viewDate, setViewDate] = useState(new Date());
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [selectedTime, setSelectedTime] = useState(null);

  // Обработчики (аналог addEventListener)
  const handlePrevMonth = () => {
    setViewDate(prev => new Date(prev.getFullYear(), prev.getMonth() - 1, 1));
  };

  const handleNextMonth = () => {
    setViewDate(prev => new Date(prev.getFullYear(), prev.getMonth() + 1, 1));
  };

  const handleSelectDay = (date) => {
    setSelectedDate(date);
    setSelectedTime(null); // ВАЖНО: сбрасываем время при смене дня
  };

  const handleSelectTime = (time) => {
    setSelectedTime(time);
  };

  return (
    <>
      <Header />
      <main className="page">
        <Stepper />

        <section className="intro">
          <div className="container">
            <p className="intro__eyebrow">Шаг 3 из 5</p>
            <h1 className="intro__title">Выберите дату и время</h1>
            <p className="intro__subtitle">
              Мастер: Дмитрий Орлов · услуги: стрижка и борода, 75 мин
            </p>
          </div>
        </section>

        <section className="booking">
          <div className="container booking__grid">
            <Calendar
              viewDate={viewDate}
              selectedDate={selectedDate}
              onSelectDay={handleSelectDay}
              onPrev={handlePrevMonth}
              onNext={handleNextMonth}
            />
            <TimeSlots
              selectedDate={selectedDate}
              selectedTime={selectedTime}
              onSelectTime={handleSelectTime}
            />
          </div>
        </section>

        <BottomBar
          selectedDate={selectedDate}
          selectedTime={selectedTime}
        />
      </main>
      <Footer />
    </>
  );
}