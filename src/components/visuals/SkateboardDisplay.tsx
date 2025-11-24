import React from 'react';

export interface SkateboardDisplayProps {
  className?: string;
}

export const SkateboardDisplay: React.FC<SkateboardDisplayProps> = ({ 
  className = '' 
}) => {
  return (
    <div className={`project-card-media ${className}`}>
      <img
        src="/assets/projects/esk8/foreground.png"
        alt=""
        className="foreground-layer"
        loading="lazy"
        style={{ opacity: 0 }}
      />
      <img
        src="/assets/projects/esk8/background.svg"
        alt=""
        className="background-layer"
        loading="lazy"
        style={{ opacity: 1 }}
      />
    </div>
  );
};
