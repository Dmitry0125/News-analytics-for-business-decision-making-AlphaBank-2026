export default function Header() {
  return (
    <header style={{
      backgroundColor: '#EF3124',
      color: 'white',
      padding: '15px 40px',
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      top: 0,             
      zIndex: 1000,       
      boxShadow: '0 2px 8px rgba(0,0,0,0.15)'
    }}>
      <div style={{
        backgroundColor: 'white',
        color: '#EF3124',
        borderRadius: '50%',
        width: '32px',
        height: '32px',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontWeight: '900',
        fontSize: '18px'
      }}>
        А
      </div>
      <span style={{ fontSize: '20px', fontWeight: 'bold', letterSpacing: '0.5px' }}>
        Альфа-Бизнес
      </span>
    </header>
  );
}