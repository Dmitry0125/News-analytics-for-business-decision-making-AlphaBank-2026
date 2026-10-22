import { Typography, Button } from 'antd';
import { ShareAltOutlined } from '@ant-design/icons';

const { Title, Text } = Typography;

export default function CompanyHeader({ target_company }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
      <div>
        <Title level={4} style={{ margin: 0 }}>
          {target_company.org_type} (ОКВЭД: {target_company.okved_code})
        </Title>
        <Text type="secondary">
          {target_company.city} | {target_company.okved_name}
        </Text>
      </div>
      <Button icon={<ShareAltOutlined />}>Поделиться</Button>
    </div>
  );
}