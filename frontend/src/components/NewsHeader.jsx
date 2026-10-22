import { Typography } from 'antd';

const { Title, Text } = Typography;

export default function CompanyHeader({news_source}) {
  return (
    <div>
        <Title level={2}>{news_source.title}</Title>
        <Text type="secondary" style={{ display: 'block', marginBottom: '30px' }}>
            Дата публикации: {new Date(news_source.publish_date).toLocaleDateString('ru-RU')}
        </Text>
    </div>
  );
}