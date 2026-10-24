import { Typography } from 'antd';
import NewsCard from './NewsCard';
import CompanySelector from './CompanySelector'; // <-- Импорт
import { mockCompanies } from '../data/mockCompanies'; // <-- Импорт моков
import ChatButton from './ChatButton';

const { Title, Text } = Typography;

export default function Dashboard({ insights, companyName, onSelectNews, selectedCompanyId, setSelectedCompanyId }) {
  return (
    <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '0 20px' }}>
      
      <CompanySelector 
        selectedCompanyId={selectedCompanyId}
        onChange={setSelectedCompanyId}
        companies={mockCompanies}
      />

      <Title level={2}>Новостная аналитика</Title>
      <Text type="secondary" style={{ display: 'block', marginBottom: '30px' }}>
        Персональные инсайты для {companyName}
      </Text>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {insights.map((news) => (
          <NewsCard 
            key={news.insight_id} 
            news={news} 
            onClick={() => onSelectNews(news)} 
          />
        ))}
      </div>
      <ChatButton />
    </div>
  );
}