import { Button } from 'antd';

export default function ChatButton({ onClick }) {
  return (
    <Button 
      type="primary" 
      size="large"
      onClick={onClick}
      className="chat-button"
    >
      Спросить ИИ
    </Button>
  );
}