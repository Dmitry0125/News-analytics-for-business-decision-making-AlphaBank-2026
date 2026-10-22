import { Typography, Tag } from 'antd';
import { LinkOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

export default function NewsHeader({ news_source, risk_level }) {
  const sourceUrl = news_source?.source_url || '#';
  const sourceName = news_source?.source_name || 'Первоисточник';
  
  // Определяем цвет и текст плашки
  const isRisk = risk_level === 'High Risk' || risk_level === 'ВЫСОКИЙ РИСК'; 
  const tagColor = isRisk ? 'green' : 'red';
  const tagText = isRisk ? 'ВОЗМОЖНОСТЬ' : 'ВЫСОКИЙ РИСК';

  return (
    <>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '20px' }}>
        <Title level={2} style={{ marginTop: 0, marginBottom: '10px' }}>
          {news_source?.title}
        </Title>
        <Tag color={tagColor} style={{ marginTop: '8px', fontSize: '14px', padding: '4px 12px', fontWeight: 'bold', flexShrink: 0 }}>
          {tagText}
        </Tag>
      </div>
      
      <div style={{ display: 'flex', gap: '20px', alignItems: 'center', marginBottom: '30px' }}>
        <Text type="secondary">
          Дата публикации: {news_source?.publish_date ? new Date(news_source.publish_date).toLocaleDateString('ru-RU') : 'Дата не указана'}
        </Text>
        
        <a href={sourceUrl} target="_blank" rel="noopener noreferrer" style={{ color: '#08628C', textDecoration: 'none' }}>
          <LinkOutlined style={{ marginRight: '4px' }} />
          Читать источник ({sourceName})
        </a>
      </div>
    </>
  );
}