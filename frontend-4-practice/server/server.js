import { database } from './database.js';

const DELAY_MS = 800;

export function setupServerMiddleware(server) {
  server.middlewares.use('/api/booking/today', async (req, res) => {
    await new Promise(r => setTimeout(r, DELAY_MS));
    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify(database.today));
  });

  server.middlewares.use('/api/slots', async (req, res) => {
    await new Promise(r => setTimeout(r, DELAY_MS));
    const url = new URL(req.url, 'http://localhost');
    const day = parseInt(url.searchParams.get('day'));
    const month = parseInt(url.searchParams.get('month'));
    const year = parseInt(url.searchParams.get('year'));

    if (!day || !year) {
      res.statusCode = 400;
      res.end(JSON.stringify({ error: 'Bad request' }));
      return;
    }

    // Меняем доступность в зависимости от даты (для наглядности)
    const isEvenDay = day % 2 === 0;
    const slots = database.slots.map(s => ({
      ...s,
      available: isEvenDay ? s.available : !s.available
    }));

    res.setHeader('Content-Type', 'application/json');
    res.end(JSON.stringify({
      date: `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`,
      slots
    }));
  });
}