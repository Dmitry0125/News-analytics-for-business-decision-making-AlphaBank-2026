import { Divider } from 'antd';
import NativeAd from './NativeAd.jsx';
import NewsHeader from './NewsHeader.jsx'
import WhatHappend from './WhatHapppend.jsx';
import WhyItMatters from './WhyItMatters.jsx';
import BankOpinion from './BankOpinion.jsx';
import RecommendedActions from './RecommendedActions.jsx';
import Traceability from './Traceability.jsx';
import ChatButton from './ChatButton.jsx';


export default function NewsDetail({ insight }) {
  if (!insight) return null;

  const { target_company, news_source, ai_interpretation, native_ad, risk_level } = insight;

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', paddingBottom: '20px'}}>

      <Divider />

      {/* Заголовок новости */}
      <NewsHeader news_source={news_source} risk_level={risk_level}/>

      {/* Что произошло */}
      <WhatHappend ai_interpretation={ai_interpretation}/>

      {/* Почему это важно */}
      <WhyItMatters ai_interpretation={ai_interpretation}/>

      {/* Мнение Альфа-Банка */}
      <BankOpinion ai_interpretation={ai_interpretation}/>

      {/* Действия */}
      <RecommendedActions ai_interpretation={ai_interpretation}/>

      {/* Реклама */}
      <NativeAd adData={native_ad} />

      {/* Трассируемость */}
      <Traceability ai_interpretation={ai_interpretation}/>
        
      {/* Спросить ИИ */}
      <ChatButton/>

    </div>
  );
}