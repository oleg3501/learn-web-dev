export async function fetchToday() {
  const res = await fetch('/api/booking/today');
  if (!res.ok) throw new Error('Ошибка загрузки текущей даты');
  return res.json();
}

export async function fetchSlots(day, month, year) {
  const res = await fetch(`/api/slots?day=${day}&month=${month}&year=${year}`);
  if (!res.ok) throw new Error('Ошибка загрузки слотов');
  return res.json();
}