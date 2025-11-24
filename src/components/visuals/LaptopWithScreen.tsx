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
    >
      {/* Laptop Screen */}
      <div className="laptop-screen">
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
          style={{ opacity: 0 }}
        />
      </div>
      
      {/* Laptop Keyboard */}
      <div className="laptop-keyboard">
        <img
          src="/assets/projects/self-driving-car/computer-keys-foreground.svg"
          alt="Self-driving car keyboard foreground"
          className="foreground-layer"
          loading="lazy"
          style={{ opacity: 0 }}
        />
        <img
          src="/assets/projects/self-driving-car/computer-keys-background.svg"
          alt="Self-driving car keyboard background"
          className="background-layer"
          loading="lazy"
          style={{ opacity: 1 }}
        />
      </div>
    </div>
  );
};
