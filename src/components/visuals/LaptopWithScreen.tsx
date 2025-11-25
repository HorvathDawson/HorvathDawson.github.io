import React, { useRef, useEffect } from 'react';

export interface LaptopWithScreenProps {
  className?: string;
}

export const LaptopWithScreen: React.FC<LaptopWithScreenProps> = ({
  className = ''
}) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const contentRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const container = containerRef.current;
    const content = contentRef.current;
    if (!container || !content) return;

    const updateSize = () => {
      if (!container || !content) return;
      const parent = container.parentElement;
      if (!parent) return;

      const parentRect = parent.getBoundingClientRect();
      const parentWidth = parentRect.width;
      const parentHeight = parentRect.height;

      if (parentWidth === 0 || parentHeight === 0) return;

      const targetAspectRatio = 1000 / 700; // 10/7
      const parentAspectRatio = parentWidth / parentHeight;

      let width, height;

      if (parentAspectRatio > targetAspectRatio) {
        // Parent is wider than target: constrain by height
        height = parentHeight;
        width = height * targetAspectRatio;
      } else {
        // Parent is taller than target: constrain by width
        width = parentWidth;
        height = width / targetAspectRatio;
      }

      content.style.width = `${width}px`;
      content.style.height = `${height}px`;
    };

    const observer = new ResizeObserver(updateSize);
    if (container.parentElement) {
      observer.observe(container.parentElement);
    }

    window.addEventListener('resize', updateSize);
    requestAnimationFrame(updateSize);

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
      observer.disconnect();
      window.removeEventListener('resize', updateSize);
      container.removeEventListener('mouseenter', handleMouseEnter);
      container.removeEventListener('mouseleave', handleMouseLeave);
    };
  }, []);

  return (
    <div
      ref={containerRef}
      className={`laptop-with-screen ${className}`.trim()}
      style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', overflow: 'hidden' }}
    >
      {/* Sized content container */}
      <div
        ref={contentRef}
        style={{
          position: 'relative',
          // Aspect ratio fallback
          aspectRatio: '10 / 7',
          perspective: '1000px',
          transformStyle: 'preserve-3d',
        }}
      >

        {/* Laptop Screen Group 
              Original: top: 50, left: 150, width: 700, height: 450 (Ref: 1000x700)
              % Top: 7.14%, Left: 15%, Width: 70%, Height: 64.28%
          */}
        <div className="laptop-screen" style={{
          position: 'absolute',
          top: '7.14%',
          left: '15%',
          width: '70%',
          height: '64.28%',
          transformOrigin: '50% 100%',
          transformStyle: 'preserve-3d',
        }}>
          <img
            src="/assets/projects/self-driving-car/computer-foreground.svg"
            alt="Self-driving car computer foreground"
            className="foreground-layer"
            loading="lazy"
            style={{ opacity: 0, position: 'absolute', inset: 0, width: '100%', height: '100%' }}
          />
          <img
            src="/assets/projects/self-driving-car/computer-background.svg"
            alt="Self-driving car computer background"
            className="background-layer"
            loading="lazy"
            style={{ opacity: 1, position: 'absolute', inset: 0, width: '100%', height: '100%' }}
          />
          {/* Splash Screen - Adjusted to fit inside the monitor bezel */}
          <div
            className="computer-screen splash-layer"
            style={{
              opacity: 0,
              position: 'absolute',
              top: '6%',
              left: '6%',
              width: '88%',
              height: '80%',
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              backgroundImage: 'url(/assets/projects/self-driving-car/screen.gif)',
              zIndex: 6
            }}
          />
        </div>

        {/* Laptop Keyboard Group 
              Original: top: 480, left: 100, width: 800, height: 200
              % Top: 68.57%, Left: 10%, Width: 80%, Height: 28.57%
          */}
        <div className="laptop-keyboard" style={{ position: 'absolute', top: '68.57%', left: '10%', width: '80%', height: '28.57%' }}>
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
