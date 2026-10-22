import { useState, useEffect } from 'react';
import { ConfigProvider, Spin, Alert } from 'antd';
import ruRU from 'antd/locale/ru_RU';
import NewsDetail from './components/NewsDetail';
import Header from './components/Header';

function App() {
  const [insight, setInsight] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const companyId = 'COMP_A_15_BILLION'; 

  useEffect(() => {
    setLoading(true);
    setError(null);

    fetch(`http://localhost:8000/api/v1/insights?company_id=${companyId}&role=CEO`)
      .then((response) => {
        if (!response.ok) throw new Error(`Ошибка сервера: ${response.status}`);
        return response.json();
      })
      .then((data) => {
        console.log("ДАННЫЕ ОТ СЕРВЕРА:", data); 
        
        // Сервер отдает один объект, поэтому просто передаем его в состояние
        if (data && typeof data === 'object') {
          setInsight(data);
        } else {
          setError('Не удалось распознать формат данных');
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError(err.message);
        setLoading(false);
      });
  }, [companyId]);

  return (
    <ConfigProvider locale={ruRU}>
      {/* Шапка Альфа Бизнес */}
      <Header />
      
      <div style={{ background: '#f0f2f5', minHeight: '100vh', paddingTop: '20px' }}>
        
        {loading && (
          <div style={{ textAlign: 'center', marginTop: '100px' }}>
            <Spin size="large" tip="Загружаем аналитику..." />
          </div>
        )}

        {error && (
          <div style={{ maxWidth: '600px', margin: '50px auto' }}>
            <Alert message="Ошибка" description={error} type="error" showIcon />
          </div>
        )}

        {!loading && !error && insight && (
          <NewsDetail insight={insight} />
        )}

      </div>
    </ConfigProvider>
  );
}

export default App;