import React from 'react';

export interface SkateboardDisplayProps {
  className?: string;
}

export const SkateboardDisplay: React.FC<SkateboardDisplayProps> = ({ 
  className = '' 
}) => {
  return (
    <div className={`skateboard-display ${className}`.trim()} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}>
      <div style={{ width: 900, height: 600, maxWidth: '100%', maxHeight: '100%', position: 'relative' }}>
        <img
          src="/assets/projects/esk8/foreground.png"
          alt=""
          className="foreground-layer"
          loading="lazy"
          style={{ opacity: 0, position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain' }}
        />
        <img
          src="/assets/projects/esk8/background.svg"
          alt=""
          className="background-layer"
          loading="lazy"
          style={{ opacity: 1, position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain' }}
        />
      </div>
    </div>
  );
};
