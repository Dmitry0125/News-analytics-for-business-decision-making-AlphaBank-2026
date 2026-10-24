import { Select, Typography, ConfigProvider } from 'antd';

const { Text } = Typography;

export default function CompanySelector({ selectedCompanyId, onChange, companies }) {
  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#ff9e9e',
        },
        components: {
          Select: {
            optionSelectedBg: '#fff1f0',
            optionSelectedColor: '#262626',
          },
        },
      }}
    >
      <div style={{ marginBottom: '20px' }}>
        <Text strong style={{ marginRight: '10px' }}>Компания:</Text>
        <Select
          value={selectedCompanyId}
          style={{ width: 350 }}
          onChange={onChange}
          options={companies.map((c) => ({ value: c.id, label: c.name }))}
          variant="outlined"
        />
      </div>
    </ConfigProvider>
  );
}