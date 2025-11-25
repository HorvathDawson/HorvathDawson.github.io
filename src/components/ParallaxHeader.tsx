import React, { useEffect, useRef } from 'react';
import { parallaxLayers } from '../data/content';

// Helper: compute the transform for a given depth index (0..5)
const depthTransform = (depthIndex: number) => {
  const z = -500 + depthIndex * 100; // -500, -400, ... 0
  const scale = 6 - depthIndex; // 6,5,4,3,2,1
  const translateY = `translateY(calc((100vh - 66.6666666667vw) / 5))`;
  return `translateZ(${z}px) scale(${scale}) ${translateY}`;
};

export const ParallaxHeaderCSS: React.FC = () => {
  return (
    <>
      {parallaxLayers.map((layer) => {
        const depth = Number(layer.id.slice(-1));
        const style: React.CSSProperties = {
          position: 'absolute',
          display: 'flex',
          height: '100vh',
          minHeight: '100vh',
          width: '100vw',
          minWidth: '100vw',
          justifyContent: 'center',
          transform: depthTransform(depth),
        };

        const imgStyle: React.CSSProperties = {
          display: 'block',
          width: '100vw',
          minWidth: 500,
          minHeight: '333.3333333333px',
          height: '66.6666666667vw',
        };

        return (
          <div key={layer.id} style={style}>
            <img src={layer.src} alt="" style={imgStyle} />
          </div>
        );
      })}
    </>
  );
};

export const ParallaxHeaderJS: React.FC = () => {
  const containerRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    let raf = 0 as number | null;
    const onScroll = () => {
      if (raf) return;
      raf = requestAnimationFrame(() => {
        const scrolled = window.scrollY || window.pageYOffset;
        // Move each layer at a factor proportional to its depth
        const layers = containerRef.current?.children;
        if (layers) {
          Array.from(layers).forEach((child, i) => {
            const depth = Number((child as HTMLElement).dataset.depth ?? i);
            const speed = (6 - depth) * 0.05; // tuning constant
            const y = scrolled * speed;
            (child as HTMLElement).style.transform = `translate3d(0, ${y}px, 0) translateZ(${ -500 + depth*100 }px) scale(${6 - depth})`;
          });
        }
        raf = 0;
      }) as unknown as number;
    };

    window.addEventListener('scroll', onScroll, { passive: true });
    // kick once
    onScroll();

    return () => {
      window.removeEventListener('scroll', onScroll as EventListener);
      if (raf) cancelAnimationFrame(raf);
    };
  }, []);

  return (
    <div ref={containerRef} style={{ position: 'relative' }}>
      {parallaxLayers.map((layer) => {
        const depth = Number(layer.id.slice(-1));
        const style: React.CSSProperties = {
          position: 'absolute',
          display: 'flex',
          height: '100vh',
          minHeight: '100vh',
          width: '100vw',
          minWidth: '100vw',
          justifyContent: 'center',
          transform: depthTransform(depth),
        };
        const imgStyle: React.CSSProperties = {
          display: 'block',
          width: '100vw',
          minWidth: 500,
          minHeight: '333.3333333333px',
          height: '66.6666666667vw',
        };

        return (
          <div key={layer.id} data-depth={depth} style={style}>
            <img src={layer.src} alt="" style={imgStyle} />
          </div>
        );
      })}
    </div>
  );
};

// Default export maintains compatibility with existing imports — CSS-style inline version
export const ParallaxHeader = ParallaxHeaderCSS;
export default ParallaxHeader;
