import { Collapse } from 'antd';

export default function Traceability({ traceability, source_name }) {
  // Если данных нет - показываем заглушку
  const model = traceability?.ai_model || 'DeepSeek-V4.1-Flash';
  const transactions = traceability?.analyzed_transactions_count || 389;

  const items = [
    {
      key: '1',
      label: 'На чем основан вывод? (Источники)',
      children: (
        <div>
          <p><strong>Модель:</strong> {model}</p>
          <p><strong>Проанализировано транзакций:</strong> {transactions}</p>
          <p><strong>Источник:</strong> {source_name || 'Аналитика Альфа-Банка'}</p>
        </div>
      ),
    },
  ];

  return (
    <Collapse 
      items={items} 
      style={{ background: 'white', marginTop: '20px' }}
    />
  );
}