import React, { useEffect, useRef } from 'react';
import { parallaxLayers } from '../data/content';

export const ParallaxHeader: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  
  // CONFIGURATION
  const MAX_PARALLAX_LAG = 0.85; 
  const ANIMATION_DURATION = '90s'; // Over a minute
  const NIGHT_COLOR = '#0f172a'; // Deep midnight blue

  useEffect(() => {
    let rafId: number;
    const container = containerRef.current;

    const onScroll = () => {
      if (!container) return;

      const scrolled = window.scrollY;
      if (scrolled > container.offsetHeight + 200) return;

      rafId = requestAnimationFrame(() => {
        const layers = container.querySelectorAll<HTMLElement>('[data-parallax-layer]');
        layers.forEach((layer) => {
          const speed = parseFloat(layer.dataset.speed || '0');
          if (speed !== 0) {
            const yPos = scrolled * speed;
            layer.style.transform = `translate3d(0, ${yPos}px, 0)`;
          }
        });
      });
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); 

    return () => {
      window.removeEventListener('scroll', onScroll);
      cancelAnimationFrame(rafId);
    };
  }, []);

  const sortedLayers = [...parallaxLayers].sort((a, b) => {
    const depthA = Number(a.id.replace(/\D/g, ''));
    const depthB = Number(b.id.replace(/\D/g, ''));
    return depthA - depthB;
  });

  const maxDepthIndex = sortedLayers.length - 1;

  // --- STYLES ---

  const outerWrapperStyle: React.CSSProperties = {
    position: 'relative',
    width: '100%',
    display: 'flex', 
    justifyContent: 'center',
    overflow: 'hidden', 
    zIndex: 0,
    // Background Texture (The "Margins")
    backgroundImage: 'url("/assets/parallax_header/foreground_color.png")',
    backgroundRepeat: 'repeat', 
    backgroundPosition: 'center',
  };

  const innerHeaderStyle: React.CSSProperties = {
    position: 'relative',
    width: 'auto',
    height: 'auto',
  };

  return (
    <>
      {/* 1. Define the Animation Keyframes */}
      <style>
        {`
          @keyframes dayNightCycle {
            0% { background-color: var(--warm-white); }
            50% { background-color: ${NIGHT_COLOR}; } 
            100% { background-color: var(--warm-white); }
          }
        `}
      </style>

      <div className="parallax-header-container" ref={containerRef} style={outerWrapperStyle}>
        <div style={innerHeaderStyle}>
          {sortedLayers.map((layer, index) => {
            const isForeground = index === maxDepthIndex;
            const isBackground = index === 0;
            
            const depthRatio = index / maxDepthIndex; 
            const speed = (1 - depthRatio) * MAX_PARALLAX_LAG;

            const layerStyle: React.CSSProperties = {
              position: isForeground ? 'relative' : 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
              zIndex: index,
              willChange: 'transform, background-color', // Optimize for color change too
              
              // 2. Apply Animation ONLY to the background layer (Layer 0)
              animation: isBackground 
                ? `dayNightCycle ${ANIMATION_DURATION} ease-in-out infinite` 
                : undefined,
                
              // Fallback color if animation fails to load
              backgroundColor: isBackground ? 'var(--warm-white)' : undefined,
            };

            const imgStyle: React.CSSProperties = {
              display: 'block',
              maxHeight: '100vh', 
              maxWidth: '100%',  
              width: 'auto',
              height: 'auto',
              objectFit: 'cover', 
            };

            return (
              <div
                key={layer.id}
                data-parallax-layer
                data-speed={isForeground ? 0 : speed}
                style={layerStyle}
              >
                <img src={layer.src} alt="" style={imgStyle} />
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
};

export default ParallaxHeader;