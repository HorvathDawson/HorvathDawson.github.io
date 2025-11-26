import React, { useEffect, useRef } from 'react';
import { parallaxLayers } from '../data/content';

export const ParallaxHeader: React.FC = () => {
  const containerRef = useRef<HTMLDivElement>(null);
  
  // CONFIGURATION
  const MAX_PARALLAX_LAG = 0.85; 

  useEffect(() => {
    let rafId: number;
    const container = containerRef.current;

    const onScroll = () => {
      if (!container) return;

      const scrolled = window.scrollY;

      // Optimization check
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

  // Sort layers (Back to Front)
  const sortedLayers = [...parallaxLayers].sort((a, b) => {
    const depthA = Number(a.id.replace(/\D/g, ''));
    const depthB = Number(b.id.replace(/\D/g, ''));
    return depthA - depthB;
  });

  const maxDepthIndex = sortedLayers.length - 1;

  // --- STYLES ---

  // 1. OUTER WRAPPER
  // - Full Width
  // - Background Texture (visible in margins)
  // - Centers the content
  // - overflow: hidden triggers the clipping for parallax
  const outerWrapperStyle: React.CSSProperties = {
    position: 'relative',
    width: '100%',
    display: 'flex', 
    justifyContent: 'center',
    overflow: 'hidden', 
    zIndex: 0,
    
    // Background Texture
    backgroundImage: 'url("/assets/parallax_header/foreground_color.png")',
    backgroundRepeat: 'repeat', 
    backgroundPosition: 'center',
  };

  // 2. INNER CONTAINER
  // - Wraps tightly around the images
  // - No fixed dimensions; determined by the foreground image
  const innerHeaderStyle: React.CSSProperties = {
    position: 'relative',
    width: 'auto',
    height: 'auto',
  };

  return (
    <div ref={containerRef} style={outerWrapperStyle}>
      <div style={innerHeaderStyle}>
        {sortedLayers.map((layer, index) => {
          const isForeground = index === maxDepthIndex;
          const isBackground = index === 0;
          
          const depthRatio = index / maxDepthIndex; 
          const speed = (1 - depthRatio) * MAX_PARALLAX_LAG;

          // 3. LAYER STYLES
          const layerStyle: React.CSSProperties = {
            // Foreground is relative to push the parent container's size.
            // Backgrounds are absolute to sit behind it.
            position: isForeground ? 'relative' : 'absolute',
            top: 0,
            left: 0,
            
            // These ensure background layers match the foreground layer exactly
            width: '100%',
            height: '100%',
            
            zIndex: index,
            willChange: 'transform',
            
            // Apply warm-white to Layer 0
            backgroundColor: isBackground ? 'var(--warm-white)' : undefined,
          };

          // 4. IMAGE STYLES
          // This is the logic that enforces "80vh OR 100% width"
          const imgStyle: React.CSSProperties = {
            display: 'block',
            // If the screen is TALL: Limit height to 80vh
            maxHeight: '80vh', 
            // If the screen is NARROW: Limit width to 100%
            maxWidth: '100%',  
            // Maintain aspect ratio within those limits
            width: 'auto',
            height: 'auto',
            // Ensure background layers cover the calculated area
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
  );
};

export default ParallaxHeader;