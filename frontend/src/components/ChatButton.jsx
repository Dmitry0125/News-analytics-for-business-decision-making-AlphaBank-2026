import { Button } from 'antd';

export default function ChatButton({ onClick }) {
  return (
    <Button 
      type="primary" 
      size="large"
      onClick={onClick}
      className="chat-button"
      style={{ 
        position: 'fixed', 
        bottom: '30px', 
        right: '30px', 
        zIndex: 9999,
        height: '50px',
        padding: '0 25px',
        borderRadius: '25px',
        fontWeight: 'bold'
      }}
    >
      Спросить ИИ
    </Button>
  );
}