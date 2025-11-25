import React from 'react';
import { useVisualsForceHover } from './VisualsContext';

export interface PrinterDisplayProps {
  className?: string;
}
export interface PrinterDisplayProps {
  className?: string;
  forceHover?: boolean;
}

export const PrinterDisplay: React.FC<PrinterDisplayProps> = ({ 
  className = '',
  forceHover
}) => {
  const contextForce = useVisualsForceHover();
  const effectiveForceHover = forceHover ?? contextForce ?? false;
  return (
    <div data-printer-display className={className} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}>
      <div style={{ width: 1000, height: 700, maxWidth: '100%', maxHeight: '100%', position: 'relative' }}>
        <img
          src="/assets/projects/3dprinter/foreground.png"
          alt=""
          className="foreground-layer"
          loading="lazy"
          style={{ opacity: effectiveForceHover ? 1 : 0, position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain' }}
        />
        <img
          src="/assets/projects/3dprinter/background.png"
          alt=""
          className="background-layer"
          loading="lazy"
          style={{ opacity: effectiveForceHover ? 0 : 1, position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain' }}
        />
      </div>
    </div>
  );
};
