import React from 'react';
import { useVisualsForceHover } from './VisualsContext';

export interface VintageCarDisplayProps {
  className?: string;
}
export interface VintageCarDisplayProps {
  className?: string;
  forceHover?: boolean;
}

export const VintageCarDisplay: React.FC<VintageCarDisplayProps> = ({ 
  className = '',
  forceHover
}) => {
  const contextForce = useVisualsForceHover();
  const effectiveForceHover = forceHover ?? contextForce ?? false;
  return (
    <div data-vintage-car className={className} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}>
      <div style={{ width: 1000, height: 600, maxWidth: '100%', maxHeight: '100%', position: 'relative' }}>
        <img
          src="/assets/projects/a40austin/foreground.png"
          alt=""
          className="foreground-layer"
          loading="lazy"
          style={{ opacity: effectiveForceHover ? 1 : 0, position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain' }}
        />
        <img
          src="/assets/projects/a40austin/background.png"
          alt=""
          className="background-layer"
          loading="lazy"
          style={{ opacity: effectiveForceHover ? 0 : 1, position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain' }}
        />
      </div>
    </div>
  );
};
