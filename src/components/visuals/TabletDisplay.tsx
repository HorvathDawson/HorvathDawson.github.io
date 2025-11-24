import React from 'react';

export interface TabletDisplayProps {
  className?: string;
}

export const TabletDisplay: React.FC<TabletDisplayProps> = ({ 
  className = '' 
}) => {
  return (
    <div className={`tablet-frame ${className}`}>
      <img
        src="/assets/resume/foreground.png"
        alt=""
        className="foreground-layer"
        loading="lazy"
        style={{ opacity: 0 }}
      />
      <img
        src="/assets/resume/background.png"
        alt=""
        className="background-layer"
        loading="lazy"
        style={{ opacity: 1 }}
      />
      <div 
        className="tablet-display splash-layer"
        style={{ 
          opacity: 0,
          backgroundImage: 'url(/assets/resume/resume_rotated.png)',
          backgroundSize: 'cover',
          backgroundRepeat: 'no-repeat',
          backgroundPosition: 'center center'
        }}
      />
    </div>
  );
};
