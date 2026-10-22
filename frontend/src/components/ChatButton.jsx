import { Button } from 'antd';

export default function ChatButton({ onClick }) {
  return (
    <Button 
      type="primary" 
      size="large"
      onClick={onClick} // Мы добавили сюда клик, чтобы потом открывать чат
      style={{ 
        position: 'fixed', 
        bottom: '30px', 
        right: '30px', 
        zIndex: 1000,
        height: '50px',
        padding: '0 25px',
        borderRadius: '25px',
        background: '#ef3124',
        borderColor: '#ef3124',
        boxShadow: '0 4px 12px rgba(0,0,0,0.2)'
      }}
    >
      Спросить ИИ
    </Button>
  );
}