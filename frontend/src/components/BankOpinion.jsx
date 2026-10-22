import { Typography, Card } from 'antd';
import { BankOutlined } from '@ant-design/icons';

const { Paragraph } = Typography;

export default function WhatHappend({ ai_interpretation }) {
    return (
        <Card
            title={<><BankOutlined style={{ marginRight: '8px', color: '#ef3124' }} /> Мнение экспертов Альфа-Банка</>}
            style={{ marginBottom: '20px', borderLeft: '4px solid #ef3124' }}
        >
            <Paragraph italic>{ai_interpretation.bank_expert_opinion}</Paragraph>
        </Card>
    )
}