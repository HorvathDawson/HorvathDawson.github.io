import React, { useEffect, useRef } from 'react';
import { parallaxLayers } from '../data/content';

export const ParallaxHeader: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  const layerRefs = useRef<(HTMLDivElement | null)[]>([]); 

  // CONFIGURATION
  const MAX_PARALLAX_LAG = 0.85; 
  const ANIMATION_DURATION = '90s'; 
  const NIGHT_COLOR = '#0f172a'; 

  const latestScrollY = useRef(0);
  const rafId = useRef<number | null>(null);

  useEffect(() => {
    const onScroll = () => {
      latestScrollY.current = window.scrollY;
    };

    window.addEventListener('scroll', onScroll, { passive: true });

    const animate = () => {
      if (!containerRef.current) return;
      
      const currentScroll = latestScrollY.current;

      if (currentScroll < containerRef.current.offsetHeight + 200) {
        layerRefs.current.forEach((layer) => {
          if (layer) {
            const speed = parseFloat(layer.dataset.speed || '0');
            if (speed !== 0) {
              const yPos = currentScroll * speed;
              layer.style.transform = `translate3d(0, ${yPos}px, 0)`; 
            }
          }
        });
      }
      rafId.current = requestAnimationFrame(animate);
    };

    animate();

    return () => {
      window.removeEventListener('scroll', onScroll);
      if (rafId.current) cancelAnimationFrame(rafId.current);
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
    backgroundImage: 'url("/assets/parallax_header/foreground_color.png")',
    backgroundRepeat: 'repeat', 
    backgroundPosition: 'center',
  };

  const innerHeaderStyle: React.CSSProperties = {
    position: 'relative',
    width: 'auto', 
    height: 'auto',
  };

  const skyLayerStyle: React.CSSProperties = {
    position: 'absolute',
    top: 0,
    left: 0,
    width: '100%', 
    height: '100%',
    zIndex: -1, 
    animation: `dayNightCycle ${ANIMATION_DURATION} ease-in-out infinite`,
    backgroundColor: 'var(--warm-white)', 
  };

  return (
    <>
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
          
          {/* Sky Layer inside the wrapper */}
          <div style={skyLayerStyle} />

          {sortedLayers.map((layer, index) => {
            const isForeground = index === maxDepthIndex;
            const depthRatio = index / maxDepthIndex; 
            const speed = (1 - depthRatio) * MAX_PARALLAX_LAG;

            const layerStyle: React.CSSProperties = {
              position: isForeground ? 'relative' : 'absolute',
              top: 0,
              left: 0,
              width: '100%',
              height: '100%',
              zIndex: index, 
              willChange: 'transform', 
              pointerEvents: 'none', 
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
                // FIX: Added curly braces to avoid implicit return
                ref={(el) => {
                  layerRefs.current[index] = el;
                }}
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