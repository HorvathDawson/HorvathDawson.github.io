import React from 'react';

export interface PrinterDisplayProps {
  className?: string;
}

export const PrinterDisplay: React.FC<PrinterDisplayProps> = ({ 
  className = '' 
}) => {
  return (
    <div className={`printer-display ${className}`.trim()} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}>
      <div style={{ width: 1000, height: 700, maxWidth: '100%', maxHeight: '100%', position: 'relative' }}>
        <img
          src="/assets/projects/3dprinter/foreground.png"
          alt=""
          className="foreground-layer"
          loading="lazy"
          style={{ opacity: 0, position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain' }}
        />
        <img
          src="/assets/projects/3dprinter/background.png"
          alt=""
          className="background-layer"
          loading="lazy"
          style={{ opacity: 1, position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain' }}
        />
      </div>
    </div>
  );
};
