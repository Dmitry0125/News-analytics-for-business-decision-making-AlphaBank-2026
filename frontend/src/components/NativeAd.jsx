import { Card, Typography, Button, Space } from 'antd';
const { Paragraph } = Typography;

export default function NativeAd({ adData }) {
  return (
    <Card
      title={adData.title}
      style={{ marginBottom: '20px', background: '#f0f5ff', borderColor: '#adc6ff' }}
    >
      <Paragraph>{adData.description}</Paragraph>
      <Space>
        <Button type="primary" style={{ background: '#ef3124', borderColor: '#ef3124' }}>
          Подключить
        </Button>
      </Space>
    </Card>
  );
}