import { useState, useEffect } from 'react';
import { ConfigProvider, Spin, Alert, Select } from 'antd';
import ruRU from 'antd/locale/ru_RU';
import NewsDetail from './components/NewsDetail';
import Header from './components/Header';
import Dashboard from './components/DashBoard';
import ChatButton from './components/ChatButton';
import { ArrowLeftOutlined } from '@ant-design/icons';
import { mockCompanies } from './data/mockCompanies';

function App() {
  const [selectedCompanyId, setSelectedCompanyId] = useState('COMP_A_15_BILLION');
  const [selectedInsight, setSelectedInsight] = useState(null);
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Находим текущую компанию из мока
  const currentCompany = mockCompanies.find(c => c.id === selectedCompanyId) || mockCompanies[0];

  useEffect(() => {
    // Имитируем загрузку
    setLoading(true);
    setSelectedInsight(null); // Сбрасываем выбранную новость при смене компании

    setTimeout(() => {
      setInsights(currentCompany.news);
      setLoading(false);
    }, 500);
  }, [selectedCompanyId]);

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
          <Dashboard
            insights={insights}
            companyName={currentCompany.name}
            onSelectNews={setSelectedInsight}
            selectedCompanyId={selectedCompanyId}
            setSelectedCompanyId={setSelectedCompanyId}
          />
        )}

        {/* Если новость выбрана — показываем Деталку */}
        {!loading && !error && selectedInsight && (
          <div style={{ maxWidth: '900px', margin: '0 auto', padding: '0 20px' }}>
            <a
              onClick={() => setSelectedInsight(null)}
              style={{ cursor: 'pointer', display: 'inline-block' }}
              className='back'
            >
              <ArrowLeftOutlined /> Назад к дашборду
            </a>
            <NewsDetail insight={selectedInsight} />
          </div>
        )}
      </div>
    </ConfigProvider>
  );
}

export default App;