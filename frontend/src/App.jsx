import { useState, useEffect } from 'react';
import { ConfigProvider, Spin, Alert } from 'antd';
import ruRU from 'antd/locale/ru_RU';
import NewsDetail from './components/NewsDetail';
import Header from './components/Header';
import Dashboard from './components/DashBoard';
import ChatButton from './components/ChatButton';
import { ArrowLeftOutlined } from '@ant-design/icons';

function App() {
  const [selectedInsight, setSelectedInsight] = useState(null);
  const [insights, setInsights] = useState([]);
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
        
        // Берем реальную новость (на случай если пришел массив)
        const baseNews = Array.isArray(data) ? data[0] : data;

        // Создаем 3 копии для ленты
const fakeFeed = [
  {
    ...baseNews,
    insight_id: 'news_1',
    news_source: { ...baseNews.news_source, title: "Введение новых экспортных пошлин на металлы со стороны КНР" },
    // Оставляем текст про пошлины как есть
  },
  {
    ...baseNews,
    insight_id: 'news_2',
    news_source: { ...baseNews.news_source, title: "Скачок цен на золото на мировых рынках" },
    // Меняем текст для второй новости
    ai_interpretation: {
      ...baseNews.ai_interpretation,
      what_happened: "Мировые цены на золото выросли на 5% за неделю на фоне геополитической напряженности.",
      why_it_matters: "У вашей компании есть инвестиционный портфель в драгметаллах. Это хороший момент для фиксации прибыли.",
    }
  },
  {
    ...baseNews,
    insight_id: 'news_3',
    news_source: { ...baseNews.news_source, title: "Сохранение ключевой ставки ЦБ на уровне 14%" },
    // Меняем текст для третьей новости
    ai_interpretation: {
      ...baseNews.ai_interpretation,
      what_happened: "Центральный банк сохранил ключевую ставку на уровне 14% годовых.",
      why_it_matters: "Для вашей компании с кредитным портфелем это означает, что кредиты не подешевеют.",
    }
  },
];

        setInsights(fakeFeed);
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
      <Header />
      <div style={{ background: '#f0f2f5', minHeight: '100vh', paddingTop: '20px' }}>
        
        {loading && (
          <div style={{ textAlign: 'center', marginTop: '100px' }}>
            <Spin size="large" description="Загружаем аналитику..." />
          </div>
        )}

        {error && (
          <div style={{ maxWidth: '600px', margin: '50px auto' }}>
            <Alert title="Ошибка" description={error} type="error" showIcon />
          </div>
        )}

        {/* Если ничего не выбрано — показываем Ленту */}
        {!loading && !error && !selectedInsight && (
          <Dashboard insights={insights} onSelectNews={setSelectedInsight} />
        )}

        {/* Если новость выбрана — показываем Деталку */}
        {!loading && !error && selectedInsight && (
          <div style={{ maxWidth: '900px', margin: '0 auto', padding: '0 20px' }}>
            <a 
              onClick={() => setSelectedInsight(null)} 
              style={{ cursor: 'pointer', color: '#08628C', display: 'inline-block', marginBottom: '20px' }}
            >
              <ArrowLeftOutlined /> Назад к дашборду
            </a>
            <NewsDetail insight={selectedInsight} />
          </div>
        )}
      </div>
      <ChatButton/>
    </ConfigProvider>
  );
}

export default App;