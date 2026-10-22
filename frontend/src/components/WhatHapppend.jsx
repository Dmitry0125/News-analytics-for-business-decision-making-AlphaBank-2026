import { Typography, Card } from 'antd';

const { Paragraph } = Typography;

export default function WhatHappend({ai_interpretation}) {
    return (
        <Card title="Что произошло?" style={{ marginBottom: '20px' }}>
            <Paragraph>{ai_interpretation.what_happened}</Paragraph>
        </Card>
    )
}