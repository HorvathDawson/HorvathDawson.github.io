import React, { useRef, useEffect } from 'react';

export interface LaptopWithScreenProps {
  className?: string;
}

export const LaptopWithScreen: React.FC<LaptopWithScreenProps> = ({ 
  className = ''
}) => {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    if (!container) return;

    const handleMouseEnter = () => {
      const foregrounds = container.querySelectorAll('.foreground-layer') as NodeListOf<HTMLElement>;
      const backgrounds = container.querySelectorAll('.background-layer') as NodeListOf<HTMLElement>;
      const screens = container.querySelectorAll('.computer-screen') as NodeListOf<HTMLElement>;
      
      foregrounds.forEach(el => el.style.opacity = '1');
      backgrounds.forEach(el => el.style.opacity = '0');
      screens.forEach(el => el.style.opacity = '1');
    };

    const handleMouseLeave = () => {
      const foregrounds = container.querySelectorAll('.foreground-layer') as NodeListOf<HTMLElement>;
      const backgrounds = container.querySelectorAll('.background-layer') as NodeListOf<HTMLElement>;
      const screens = container.querySelectorAll('.computer-screen') as NodeListOf<HTMLElement>;
      
      foregrounds.forEach(el => el.style.opacity = '0');
      backgrounds.forEach(el => el.style.opacity = '1');
      screens.forEach(el => el.style.opacity = '0');
    };

    container.addEventListener('mouseenter', handleMouseEnter);
    container.addEventListener('mouseleave', handleMouseLeave);

    return () => {
      container.removeEventListener('mouseenter', handleMouseEnter);
      container.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, []);



  return (
    <div 
      ref={containerRef}
      className={`laptop-with-screen ${className}`.trim()}
      style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}
    >
      {/* intrinsic frame: 1000x700 */}
      <div style={{ width: 1000, height: 700, maxWidth: '100%', maxHeight: '100%', position: 'relative' }}>
        {/* Laptop Screen */}
        <div className="laptop-screen" style={{ position: 'absolute', inset: 0 }}>
        <img
          src="/assets/projects/self-driving-car/computer-foreground.svg"
          alt="Self-driving car computer foreground"
          className="foreground-layer"
          loading="lazy"
          style={{ opacity: 0 }}
        />
        <img
          src="/assets/projects/self-driving-car/computer-background.svg"
          alt="Self-driving car computer background"
          className="background-layer"
          loading="lazy"
          style={{ opacity: 1 }}
        />
        <div
          className="computer-screen splash-layer"
          style={{ opacity: 0, position: 'absolute', inset: 0 }}
        />
      </div>
      
  {/* Laptop Keyboard */}
  <div className="laptop-keyboard" style={{ position: 'absolute', left: 0, right: 0, bottom: 0 }}>
        <img
          src="/assets/projects/self-driving-car/computer-keys-foreground.svg"
          alt="Self-driving car keyboard foreground"
          className="foreground-layer"
          loading="lazy"
          style={{ opacity: 0, position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain' }}
        />
        <img
          src="/assets/projects/self-driving-car/computer-keys-background.svg"
          alt="Self-driving car keyboard background"
          className="background-layer"
          loading="lazy"
          style={{ opacity: 1, position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain' }}
        />
        </div>
      </div>
    </div>
  );
};
