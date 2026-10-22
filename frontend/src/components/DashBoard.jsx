import { Typography } from 'antd';
import NewsCard from './NewsCard';

const { Title, Text } = Typography;

export default function Dashboard({ insights, onSelectNews }) {
  return (
    <div style={{ maxWidth: '1100px', margin: '0 auto', padding: '0 20px' }}>
      <Title level={2}>Новостная аналитика</Title>
      <Text type="secondary" style={{ display: 'block', marginBottom: '30px' }}>
        Персональные инсайты для АО "Череповецкий металлургический завод"
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
    </div>
  );
}