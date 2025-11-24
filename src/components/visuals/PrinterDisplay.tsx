import React from 'react';

export interface PrinterDisplayProps {
  className?: string;
}

export const PrinterDisplay: React.FC<PrinterDisplayProps> = ({ 
  className = '' 
}) => {
  return (
    <div className={`project-card-media ${className}`}>
      <img
        src="/assets/projects/3dprinter/foreground.png"
        alt=""
        className="foreground-layer"
        loading="lazy"
        style={{ opacity: 0 }}
      />
      <img
        src="/assets/projects/3dprinter/background.png"
        alt=""
        className="background-layer"
        loading="lazy"
        style={{ opacity: 1 }}
      />
    </div>
  );
};
