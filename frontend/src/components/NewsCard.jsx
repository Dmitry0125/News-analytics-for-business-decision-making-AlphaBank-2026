import { Card, Tag, Typography, Button } from 'antd';
import { ArrowRightOutlined } from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;

export default function NewsCard({ news, onClick}) {
  const risk = news.risk_level;
  let tagColor = 'gray'
  let tagText = 'ЗАГРУЗКА'
  if (risk === 'High Risk' || risk === 'ВЫСОКИЙ РИСК') {
    tagColor = 'red';
    tagText = 'ВЫСОКИЙ РИСК';
  } else if (risk === 'Opportunity' || risk === 'ВОЗМОЖНОСТЬ') {
    tagColor = 'green';
    tagText = 'ВОЗМОЖНОСТЬ';
  } else if (risk === 'Medium Risk' || risk === 'СРЕДНИЙ РИСК') {
    tagColor = 'orange';
    tagText = 'СРЕДНИЙ РИСК';
  }

  return (
    <Card 
      hoverable 
      style={{ width: '100%', borderRadius: '8px', cursor: 'pointer' }}
      onClick={onClick}
    >
      {/* Верхняя часть: Заголовок и плашка */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '10px' }}>
        <Title level={4} style={{ margin: 0, paddingRight: '20px' }}>
          {news.news_source.title}
        </Title>
        <Tag color={tagColor} style={{ margin: 0, fontWeight: 'bold', flexShrink: 0 }}>
          {tagText}
        </Tag>
      </div>

      {/* Средняя часть: Дата и текст */}
      <Text type="secondary" style={{ fontSize: '13px', display: 'block', marginBottom: '10px' }}>
        {news.news_source.publish_date ? new Date(news.news_source.publish_date).toLocaleDateString('ru-RU') : 'Дата не указана'} 
        {' • '} 
        {news.news_source.source_name || 'Коммерсантъ'}
      </Text>
      
      <Paragraph ellipsis={{ rows: 2 }} style={{ margin: 0, color: '#555'}}>
        {news.ai_interpretation.what_happened}
      </Paragraph>

      {/* Нижняя часть: Кнопка */}
      <div style={{ display: 'flex', justifyContent: 'flex-end'}}>
        <Button type="link" className='more-detailed'>
          Подробнее <ArrowRightOutlined />
        </Button>
      </div>

    </Card>
  );
}