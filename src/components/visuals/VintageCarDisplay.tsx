import React from 'react';

export interface VintageCarDisplayProps {
  className?: string;
}

export const VintageCarDisplay: React.FC<VintageCarDisplayProps> = ({ 
  className = '' 
}) => {
  return (
    <div className={`project-card-media ${className}`}>
      <img
        src="/assets/projects/a40austin/foreground.png"
        alt=""
        className="foreground-layer"
        loading="lazy"
        style={{ opacity: 0 }}
      />
      <img
        src="/assets/projects/a40austin/background.png"
        alt=""
        className="background-layer"
        loading="lazy"
        style={{ opacity: 1 }}
      />
    </div>
  );
};
