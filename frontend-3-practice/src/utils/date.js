export const MONTHS_NOMINATIVE = [
  'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
  'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
];

export const MONTHS_GENITIVE = [
  'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
  'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
];

export const DAYS_OF_WEEK = [
  'Воскресенье', 'Понедельник', 'Вторник', 'Среда',
  'Четверг', 'Пятница', 'Суббота'
];

// Сравнение двух дат (0 если равны, <0 если date1 раньше, >0 если позже)
export function compareDates(date1, date2) {
  const a = new Date(date1); a.setHours(0, 0, 0, 0);
  const b = new Date(date2); b.setHours(0, 0, 0, 0);
  return a.getTime() - b.getTime();
}

// Можно ли выбрать день (не раньше сегодня)
export function isDateSelectable(day, month, year, today) {
  const checkDate = new Date(year, month, day);
  return compareDates(checkDate, today) >= 0;
}

// Сетка календаря: массив недель, каждая неделя — массив дней (или null для пустых ячеек)
export function buildCalendarGrid(year, month) {
  const firstDay = new Date(year, month, 1);
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  // Сдвиг: в JS 0 = Воскресенье, нам нужно Пн = 0
  let startOffset = firstDay.getDay() - 1;
  if (startOffset === -1) startOffset = 6;

  const cells = [];
  for (let i = 0; i < startOffset; i++) cells.push(null);
  for (let d = 1; d <= daysInMonth; d++) cells.push(d);
  while (cells.length % 7 !== 0) cells.push(null);

  const weeks = [];
  for (let i = 0; i < cells.length; i += 7) {
    weeks.push(cells.slice(i, i + 7));
  }
  return weeks;
}

// Мок-данные занятых слотов (как в нативной версии)
export function getSlotsForDate(date) {
  const base = ['10:00', '11:00', '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00', '18:00', '19:00'];
  const isEvenDay = date.getDate() % 2 === 0;
  const occupied = isEvenDay ? ['12:00', '15:00'] : ['11:00', '14:00'];
  return base.map(time => ({ time, isOccupied: occupied.includes(time) }));
}

// Форматирование для нижней панели
export function formatBottomBar(date, time) {
  const dayName = DAYS_OF_WEEK[date.getDay()];
  const dayNum = date.getDate();
  const monthName = MONTHS_GENITIVE[date.getMonth()];
  const year = date.getFullYear();
  return `${dayName}, ${dayNum} ${monthName} ${year} • ${time}`;
}