// ==========================================
// 1. КОНСТАНТЫ И ДАННЫЕ
// ==========================================
const MONTHS_NOMINATIVE = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
const MONTHS_GENITIVE = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'];
const DAYS_OF_WEEK = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];

// Имитация базы данных занятых слотов (для демонстрации обновления)
function getMockSlotsForDate(date) {
  const baseSlots = ['10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00'];
  // Для простоты: в чётные дни заняты 12:00 и 15:00, в нечётные 11:00 и 14:00
  const isEvenDay = date.getDate() % 2 === 0;
  const occupiedTimes = isEvenDay ? ['12:00', '15:00'] : ['11:00', '14:00'];
  
  return baseSlots.map(time => ({
    time,
    isOccupied: occupiedTimes.includes(time)
  }));
}

// ==========================================
// 2. СОСТОЯНИЕ (STATE)
// ==========================================
const state = {
  viewDate: new Date(),       // Дата, которую сейчас показывает календарь
  selectedDate: null,         // Выбранная пользователем дата (объект Date)
  selectedTime: null          // Выбранное время (строка)
};

// ==========================================
// 3. ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
// ==========================================
// Проверка, является ли дата прошлой (раньше сегодняшней)
function isDatePast(year, month, day) {
  const today = new Date();
  today.setHours(0, 0, 0, 0); // Обнуляем время для корректного сравнения
  const checkDate = new Date(year, month, day);
  return checkDate < today;
}

// Форматирование даты для нижней панели
function formatDateForBottomBar(date, time) {
  const dayName = DAYS_OF_WEEK[date.getDay()];
  const dayNum = date.getDate();
  const monthName = MONTHS_GENITIVE[date.getMonth()];
  const year = date.getFullYear();
  return `${dayName}, ${dayNum} ${monthName} ${year} • ${time}`;
}

// ==========================================
// 4. РЕНДЕРИНГ (ОТРИСОВКА)
// ==========================================
function renderCalendar() {
  const year = state.viewDate.getFullYear();
  const month = state.viewDate.getMonth();
  
  // Обновляем заголовок месяца
  document.getElementById('current-month-year').textContent = 
    `${MONTHS_NOMINATIVE[month]} ${year}`;

  const calendarGrid = document.getElementById('calendar-days');
  calendarGrid.innerHTML = ''; // Очищаем перед перерисовкой

  // Первый день месяца и количество дней в месяце
  const firstDayOfMonth = new Date(year, month, 1);
  const daysInMonth = new Date(year, month + 1, 0).getDate();
  
  // Сдвиг для понедельника (в JS 0 = Воскресенье, нам нужно 0 = Понедельник)
  let startDayIndex = firstDayOfMonth.getDay() - 1;
  if (startDayIndex === -1) startDayIndex = 6;

  // Пустые ячейки до начала месяца
  for (let i = 0; i < startDayIndex; i++) {
    const emptyCell = document.createElement('div');
    calendarGrid.appendChild(emptyCell);
  }

  // Заполняем дни
  const today = new Date();
  today.setHours(0, 0, 0, 0);

  for (let day = 1; day <= daysInMonth; day++) {
    const btn = document.createElement('button');
    btn.className = 'day';
    btn.textContent = day;
    btn.type = 'button';
    btn.dataset.day = day; // Сохраняем день в data-атрибут

    const currentDateObj = new Date(year, month, day);

    // Проверка на "сегодня"
    if (currentDateObj.getTime() === today.getTime()) {
      btn.classList.add('day--today');
    }

    // Проверка на выбранную дату
    if (state.selectedDate && 
        state.selectedDate.getDate() === day && 
        state.selectedDate.getMonth() === month && 
        state.selectedDate.getFullYear() === year) {
      btn.classList.add('day--selected');
    }

    // Проверка на прошлую дату
    if (isDatePast(year, month, day)) {
      btn.classList.add('day--past');
      btn.disabled = true;
    }

    calendarGrid.appendChild(btn);
  }
}

function renderTimeSlots() {
  const slotsContainer = document.getElementById('time-slots');
  const headerDate = document.getElementById('selected-date-header');
  slotsContainer.innerHTML = '';

  if (!state.selectedDate) {
    headerDate.textContent = 'Выберите дату в календаре';
    return;
  }

  // Обновляем заголовок панели времени
  headerDate.textContent = `${state.selectedDate.getDate()} ${MONTHS_GENITIVE[state.selectedDate.getMonth()]}`;

  const slots = getMockSlotsForDate(state.selectedDate);

  slots.forEach(slot => {
    const btn = document.createElement('button');
    btn.className = 'slot';
    btn.type = 'button';
    btn.textContent = slot.time;
    btn.dataset.time = slot.time;

    if (slot.isOccupied) {
      btn.classList.add('slot--occupied');
      btn.disabled = true;
      btn.innerHTML = `${slot.time}<small>занято</small>`;
    }

    if (state.selectedTime === slot.time) {
      btn.classList.add('slot--selected');
    }

    slotsContainer.appendChild(btn);
  });

  updateBottomBar();
}

function updateBottomBar() {
  const bottomBarText = document.getElementById('bottom-bar-text');
  const nextBtn = document.getElementById('next-step-btn');

  if (state.selectedDate && state.selectedTime) {
    bottomBarText.textContent = formatDateForBottomBar(state.selectedDate, state.selectedTime);
    nextBtn.disabled = false; // Активируем кнопку "Далее"
  } else {
    bottomBarText.textContent = 'Дата и время не выбраны';
    nextBtn.disabled = true;
  }
}

// ==========================================
// 5. ОБРАБОТЧИКИ СОБЫТИЙ (Event Delegation)
// ==========================================
function setupEventListeners() {
  // 1. Переключение месяцев
  document.getElementById('prev-month').addEventListener('click', () => {
    state.viewDate.setMonth(state.viewDate.getMonth() - 1);
    renderCalendar();
  });

  document.getElementById('next-month').addEventListener('click', () => {
    state.viewDate.setMonth(state.viewDate.getMonth() + 1);
    renderCalendar();
  });

  // 2. Клик по дню (Делегирование: вешаем на родителя, ловим клик на .day)
  document.getElementById('calendar-days').addEventListener('click', (event) => {
    const dayBtn = event.target.closest('.day');
    if (!dayBtn || dayBtn.disabled) return; // Игнорируем пустые клетки и прошлые дни

    const day = parseInt(dayBtn.dataset.day, 10);
    const month = state.viewDate.getMonth();
    const year = state.viewDate.getFullYear();

    // Обновляем состояние
    state.selectedDate = new Date(year, month, day);
    state.selectedTime = null; // СБРАСЫВАЕМ время при смене дня!

    // Перерисовываем
    renderCalendar(); // Чтобы обновился класс .day--selected
    renderTimeSlots(); // Чтобы показать слоты для нового дня
  });

  // 3. Клик по слоту времени (Делегирование)
  document.getElementById('time-slots').addEventListener('click', (event) => {
    const slotBtn = event.target.closest('.slot');
    if (!slotBtn || slotBtn.disabled) return;

    state.selectedTime = slotBtn.dataset.time;
    
    // Перерисовываем только слоты (для обновления класса .slot--selected) и нижнюю панель
    renderTimeSlots();
  });
}

// ==========================================
// 6. ИНИЦИАЛИЗАЦИЯ
// ==========================================
function init() {
  // По умолчанию выбираем сегодня (или завтра, если хотите)
  state.selectedDate = new Date();
  state.viewDate = new Date(); // Календарь открыт на текущем месяце
  
  renderCalendar();
  renderTimeSlots();
  setupEventListeners();
}

// Запускаем после полной загрузки DOM
document.addEventListener('DOMContentLoaded', init);