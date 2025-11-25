import React, { useEffect, useRef } from 'react';
import { parallaxLayers } from '../data/content';

export const ParallaxHeader: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  
  // CONFIGURATION
  // 0.5 = The furthest back layer moves at 50% speed
  const MAX_PARALLAX_LAG = 1; 

  useEffect(() => {
    let rafId: number;
    const container = containerRef.current;

    const onScroll = () => {
      if (!container) return;

      const scrolled = window.scrollY;

      // Optimization: Stop calculating if we are way past the header
      if (scrolled > container.offsetHeight + 200) return;

      rafId = requestAnimationFrame(() => {
        const layers = container.querySelectorAll<HTMLElement>('[data-parallax-layer]');
        
        layers.forEach((layer) => {
          // Read the speed (0 for foreground, 0.5 for background)
          const speed = parseFloat(layer.dataset.speed || '0');
          
          if (speed !== 0) {
            // DIRECT SYNC: No easing, no lag.
            // We calculate the exact position immediately.
            // Positive Y moves the element DOWN, countering the UPWARD scroll.
            const yPos = scrolled * speed;
            layer.style.transform = `translate3d(0, ${yPos}px, 0)`;
          }
        });
      });
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll(); // Initial align

    return () => {
      window.removeEventListener('scroll', onScroll);
      cancelAnimationFrame(rafId);
    };
  }, []);

  // Sort layers (Back to Front)
  const sortedLayers = [...parallaxLayers].sort((a, b) => {
    const depthA = Number(a.id.replace(/\D/g, ''));
    const depthB = Number(b.id.replace(/\D/g, ''));
    return depthA - depthB;
  });

  const maxDepthIndex = sortedLayers.length - 1;

  // Image Dimensions
  const imgStyle: React.CSSProperties = {
    display: 'block',
    width: '100%',
    height: '66.666vw', 
    minHeight: '333px', 
    objectFit: 'cover',
  };

  return (
    <div 
      ref={containerRef} 
      className="parallax-container"
      style={{ 
        position: 'relative', 
        width: '100%',
        overflow: 'hidden',
        zIndex: 0
      }}
    >
      {sortedLayers.map((layer, index) => {
        const isForeground = index === maxDepthIndex;
        
        // Calculate Speed
        // Foreground (Front) -> Speed 0 (Moves with page)
        // Background (Back)  -> Speed 0.5 (Moves slower than page)
        const depthRatio = index / maxDepthIndex; 
        const speed = (1 - depthRatio) * MAX_PARALLAX_LAG;

        const layerStyle: React.CSSProperties = {
          // Foreground is relative (sets the height). Others are absolute (sit behind).
          position: isForeground ? 'relative' : 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          zIndex: index,
          display: 'flex',
          justifyContent: 'center',
          // 'will-change' tells the browser to optimize this layer for movement
          willChange: 'transform', 
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
  );
};

export default ParallaxHeader;