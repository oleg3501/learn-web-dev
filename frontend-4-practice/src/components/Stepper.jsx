const STEPS = [
  { label: 'Мастер', state: 'done' },
  { label: 'Услуги', state: 'done' },
  { label: 'Дата и время', state: 'active', number: 3 },
  { label: 'Контакты', state: 'todo', number: 4 },
  { label: 'Подтверждение', state: 'todo', number: 5 },
];

export default function Stepper() {
  return (
    <section className="steps">
      <div className="container steps__inner">
        {STEPS.map((step, index) => (
          <div
            key={index}
            className={`step ${step.state === 'done' ? 'step--done' : ''} ${step.state === 'active' ? 'step--active' : ''}`}
          >
            <div className="step__head">
              <span className="step__circle">
                {step.state === 'done' ? '✓' : step.number}
              </span>
              <span className="step__label">{step.label}</span>
            </div>
            <span className="step__bar" />
          </div>
        ))}
      </div>
    </section>
  );
}
