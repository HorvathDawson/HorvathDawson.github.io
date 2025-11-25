import React, { useRef, useEffect } from 'react';
import { useVisualsForceHover } from './VisualsContext';

export interface RobotDisplayProps {
  className?: string;
  forceHover?: boolean;
}

export const RobotDisplay: React.FC<RobotDisplayProps> = ({ 
  className = '',
  forceHover
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const contextForce = useVisualsForceHover();
  const effectiveForceHover = forceHover ?? contextForce ?? false;

  // Hover behavior is handled by BaseProjectItem via VisualsForceHoverContext.
  // Visuals should only read `effectiveForceHover` and render accordingly.

  // size and position props are intentionally ignored — visuals fill the media viewport

  const containerStyles = {
    position: 'absolute' as const,
    inset: 0 as const,
    width: '100%',
    height: '100%'
  };

  // intrinsic frame size: visual authors should treat 800x600 as the design canvas
  const intrinsicFrameStyles = {
    width: 800,
    height: 600,
    maxWidth: '100%',
    maxHeight: '100%',
    position: 'relative' as const
  };

  const imageStyles = {
    position: 'absolute' as const,
    top: 0,
    left: 0,
    width: '100%',
    height: '100%',
    objectFit: 'contain' as const,
    transition: 'opacity 0.3s ease',
  };

  // initial styles reflect forceHover prop: if true, show foreground + splash
  const initialForegroundOpacity = effectiveForceHover ? 1 : 0;
  const initialBackgroundOpacity = effectiveForceHover ? 0 : 1;
  const initialSplashOpacity = effectiveForceHover ? 1 : 0;

  return (
    <div 
      ref={containerRef}
      data-robot-display
      className={className}
      style={containerStyles}
    >
      <div style={intrinsicFrameStyles}>
        <div style={{ position: 'relative', width: '100%', height: '100%' }}>
        {/* Robot foreground - shows on hover */}
        <img
          src="/assets/projects/253robot/foreground.png"
          alt="Robot 253 foreground"
          className="foreground-layer"
          loading="lazy"
          style={{ ...imageStyles, opacity: initialForegroundOpacity }}
        />
        {/* Robot background - shows by default */}
        <img
          src="/assets/projects/253robot/background2.png"
          alt="Robot 253 background"
          className="background-layer"
          loading="lazy"
          style={{ ...imageStyles, opacity: initialBackgroundOpacity }}
        />
        {/* Robot splash overlay - shows on hover */}
        <img
          src="/assets/projects/253robot/splash.png"
          alt="Robot 253 splash"
          className="splash-layer"
          loading="lazy"
          style={{ ...imageStyles, opacity: initialSplashOpacity }}
        />
      </div>
    </div>
    </div>
  );
};
