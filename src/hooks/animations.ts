import { useEffect, useState, useRef } from 'react';

export const useMouseTracking = () => {
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const animationFrame = useRef<number | null>(null);

  useEffect(() => {
    const handleMouseMove = (event: MouseEvent) => {
      if (animationFrame.current) return;

      animationFrame.current = requestAnimationFrame(() => {
        setMousePosition({ x: event.clientX, y: event.clientY });
        animationFrame.current = null;
      });
    };

    document.addEventListener('mousemove', handleMouseMove);
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      if (animationFrame.current) {
        cancelAnimationFrame(animationFrame.current);
      }
    };
  }, []);

  return mousePosition;
};

export const useScrollAnimation = () => {
  const [scrollPosition, setScrollPosition] = useState(0);
  const animationFrame = useRef<number | null>(null);

  useEffect(() => {
    const handleScroll = () => {
      if (animationFrame.current) return;

      animationFrame.current = requestAnimationFrame(() => {
        setScrollPosition(window.scrollY);
        animationFrame.current = null;
      });
    };

    window.addEventListener('scroll', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
      if (animationFrame.current) {
        cancelAnimationFrame(animationFrame.current);
      }
    };
  }, []);

  return scrollPosition;
};

export const useIntersectionObserver = (
  options: IntersectionObserverInit = {}
) => {
  const [isInView, setIsInView] = useState(false);
  const [entry, setEntry] = useState<IntersectionObserverEntry>();
  const elementRef = useRef<HTMLElement>(null);

  useEffect(() => {
    const element = elementRef.current;
    if (!element) return;

    const observer = new IntersectionObserver(([entry]) => {
      setIsInView(entry.isIntersecting);
      setEntry(entry);
    }, options);

    observer.observe(element);

    return () => observer.disconnect();
  }, [options]);

  return { ref: elementRef, isInView, entry };
};
