import { useState, useEffect } from 'react';
import { fetchToday, fetchSlots } from './api.js';
import Header from './components/Header.jsx';
import Stepper from './components/Stepper.jsx';
import Calendar from './components/Calendar.jsx';
import TimeSlots from './components/TimeSlots.jsx';
import BottomBar from './components/BottomBar.jsx';
import Footer from './components/Footer.jsx';

export default function App() {
  const [today, setToday] = useState(null);
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedTime, setSelectedTime] = useState(null);
  const [slots, setSlots] = useState([]);
  const [isLoadingSlots, setIsLoadingSlots] = useState(false);
  const [slotsError, setSlotsError] = useState(null);
  const [globalError, setGlobalError] = useState(null);
  const [viewDate, setViewDate] = useState(new Date());

  // 1. Загружаем "сегодня" при первом рендере
  useEffect(() => {
    fetchToday()
      .then(data => {
        const todayDate = new Date(data.year, data.month, data.day);
        setToday(todayDate);
        setSelectedDate(todayDate);
        setViewDate(todayDate);
      })
      .catch(() => setGlobalError('Не удалось загрузить дату. Обновите страницу.'));
  }, []);

  // 2. Загружаем слоты при смене выбранной даты
  useEffect(() => {
    if (!selectedDate) return;

    setIsLoadingSlots(true);
    setSlotsError(null);
    setSelectedTime(null);

    const targetDate = selectedDate;

    fetchSlots(targetDate.getDate(), targetDate.getMonth(), targetDate.getFullYear())
      .then(data => {
        // Защита от гонок: проверяем, что пользователь не кликнул на другой день
        if (
          selectedDate.getDate() === targetDate.getDate() &&
          selectedDate.getMonth() === targetDate.getMonth() &&
          selectedDate.getFullYear() === targetDate.getFullYear()
        ) {
          setSlots(data.slots);
        }
      })
      .catch(() => {
        if (selectedDate.getTime() === targetDate.getTime()) {
          setSlotsError('Ошибка загрузки расписания. Попробуйте позже.');
        }
      })
      .finally(() => {
        if (selectedDate.getTime() === targetDate.getTime()) {
          setIsLoadingSlots(false);
        }
      });
  }, [selectedDate]);

  const handlePrevMonth = () =>
    setViewDate(prev => new Date(prev.getFullYear(), prev.getMonth() - 1, 1));
  const handleNextMonth = () =>
    setViewDate(prev => new Date(prev.getFullYear(), prev.getMonth() + 1, 1));
  const handleSelectDay = (date) => setSelectedDate(date);
  const handleSelectTime = (time) => setSelectedTime(time);

  // Глобальный экран загрузки
  if (!today && !globalError) {
    return (
      <div style={{ padding: '100px', textAlign: 'center' }}>Загрузка...</div>
    );
  }

  // Глобальная ошибка
  if (globalError) {
    return (
      <div style={{ padding: '100px', textAlign: 'center', color: '#e53e3e' }}>
        {globalError}
      </div>
    );
  }

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
              today={today}
              selectedDate={selectedDate}
              onSelectDay={handleSelectDay}
              onPrev={handlePrevMonth}
              onNext={handleNextMonth}
            />
            <TimeSlots
              selectedDate={selectedDate}
              selectedTime={selectedTime}
              slots={slots}
              isLoading={isLoadingSlots}
              error={slotsError}
              onSelectTime={handleSelectTime}
            />
          </div>
        </section>

        <BottomBar selectedDate={selectedDate} selectedTime={selectedTime} />
      </main>
      <Footer />
    </>
  );
}