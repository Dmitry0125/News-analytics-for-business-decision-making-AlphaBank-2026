import { Card } from 'antd';
import { BulbOutlined } from '@ant-design/icons';

export default function CompanyHeader({ ai_interpretation }) {
  return (
    <Card title={<><BulbOutlined style={{ marginRight: '8px' }} /> Рекомендуемые действия</>} style={{ marginBottom: '20px' }}>
        <ul style={{ paddingLeft: '20px', margin: 0 }}>
          {ai_interpretation.suggested_actions.map((action, index) => (
            <li key={index} style={{ marginBottom: '8px' }}>{action}</li>
          ))}
        </ul>
      </Card>
  );
}