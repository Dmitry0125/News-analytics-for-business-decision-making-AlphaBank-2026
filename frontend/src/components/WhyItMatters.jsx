import { Alert } from 'antd';
import { WarningOutlined } from '@ant-design/icons';

export default function WhyItMatters({ai_interpretation}) {
    return (
        <Alert
        message="Почему это важно для вашей компании?"
        description={ai_interpretation.why_it_matters}
        type="warning"
        showIcon
        icon={<WarningOutlined />}
        style={{ marginBottom: '20px' }}
      />
    )
}