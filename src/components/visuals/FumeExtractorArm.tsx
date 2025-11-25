import React, { useRef } from 'react';
import { useVisualsForceHover } from './VisualsContext';

export interface FumeExtractorArmProps {
  className?: string;
  forceHover?: boolean;
}

export const FumeExtractorArm: React.FC<FumeExtractorArmProps> = ({ 
  className = '',
  forceHover
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const contextForce = useVisualsForceHover();
  const effectiveForceHover = forceHover ?? contextForce ?? false;

  // Hover behavior is handled by BaseProjectItem via VisualsForceHoverContext.
  // Visuals should only read `effectiveForceHover` and render accordingly.

  return (
    <div 
      ref={containerRef}
      className={`fume-extractor-arm ${className}`.trim()}
      style={{ 
        position: 'absolute',
        inset: 0,
        width: '100%',
        height: '100%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        overflow: 'visible'
      }}
    >
      <div
        style={{
          width: 'auto',
          height: '100%',
          aspectRatio: '317 / 327',
          position: 'relative',
          maxWidth: '100%',
          maxHeight: '100%',
        }}
      >
        {/* Arm foreground - shows on hover */}
        <img
          src="/assets/projects/fume-extractor/arm.png"
          alt="Fume extractor arm"
          className="foreground-layer"
          loading="lazy"
          style={{ 
            opacity: effectiveForceHover ? 1 : 0,
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            objectFit: 'contain',
            zIndex: 5
          }}
        />
      {/* Arm edge - shows by default */}
      <img
        src="/assets/projects/fume-extractor/arm-edge.png"
        alt="Fume extractor arm edge"
        className="background-layer"
        loading="lazy"
        style={{ 
          opacity: effectiveForceHover ? 0 : 1,
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          objectFit: 'contain',
          zIndex: 4
        }}
      />
      {/* Splash overlay - shows on hover */}
      <img
        src="/assets/projects/fume-extractor/splash.png"
        alt="Fume extractor splash"
        className="splash-layer"
        loading="lazy"
        style={{ 
          opacity: effectiveForceHover ? 1 : 0,
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          objectFit: 'contain',
          zIndex: 4
        }}
      />
        {/* Fume animation - shows on hover */}
        <img
          src="/assets/projects/fume-extractor/fumes.gif"
          alt="Fume animation"
          className="splash-layer"
          loading="lazy"
          style={{ 
            opacity: effectiveForceHover ? 1 : 0,
            position: 'relative',
            width: '20%',
            height: '20%',
            minHeight: 0,
            top: '65%',
            left: '90%',
            transform: 'translate(-50%, -50%) rotate(80deg)',
            objectFit: 'contain',
            zIndex: 6
          }}
        />
      </div>
    </div>
  );
};
