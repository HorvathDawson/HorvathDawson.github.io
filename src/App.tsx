import { useEffect } from 'react';
import { ParallaxHeader } from './components/ParallaxHeader';
import { AboutMe } from './components/AboutMe';
import { ContactForm } from './components/ContactForm';
import { aboutMeContent } from './data/content';
import {
  OpenSim2RealProject,
  SelfDrivingCarProject,
  Robot253Project,
  A40AustinProject,
  BuellProject,
  FumeExtractorProject,
  Esk8Project,
  ThreeDPrinterProject,
  ResumeProject
} from './components/projects';
import './App.css';

function App() {
  useEffect(() => {
    // Mouse tracking for shuffle effect
    let mouseAnimationFrame: number;

    const handleMouseMove = (event: MouseEvent) => {
      const mouseX = event.clientX;
      const mouseY = event.clientY;

      if (mouseAnimationFrame) return;

      mouseAnimationFrame = requestAnimationFrame(() => {
        const centerX = window.innerWidth / 2;
        const centerY = window.innerHeight / 2;
        const offsetX = (mouseX - centerX) * 0.002;
        const offsetY = (mouseY - centerY) * 0.002;

        if (window.innerWidth > 991) {
          document.querySelectorAll('.project-card-media').forEach((element) => {
            (element as HTMLElement).style.transform = `translate3d(${offsetX}%, ${offsetY}%, 0)`;
          });
        }

        mouseAnimationFrame = 0;
      });
    };

    document.addEventListener('mousemove', handleMouseMove);

    // Scroll-based animations
    let scrollAnimationFrame: number;

    const handleScroll = () => {
      if (scrollAnimationFrame) return;

      scrollAnimationFrame = requestAnimationFrame(() => {
        const windowHeight = window.innerHeight;
        const windowCenterY = windowHeight / 2;
        const maxDistance = windowHeight / 2;

        // Self-driving car laptop screen rotation
        document.querySelectorAll('.project-self-driving-car [data-laptop-screen]').forEach((item) => {
          const rect = item.getBoundingClientRect();
          const itemCenterY = rect.top + rect.height / 2;
          const distanceToCenter = Math.min(0, 1.5 * windowCenterY - itemCenterY);
          let rotation = Math.min(50, -100 * (distanceToCenter / maxDistance));
          rotation = -rotation;

          (item as HTMLElement).style.transform = `rotateX(${rotation}deg)`;
        });

        // A40 Austin car translation
        document.querySelectorAll('.project-a40austin [data-vintage-car]').forEach((car) => {
          const rect = car.getBoundingClientRect();
          const itemCenterY = rect.top + rect.height / 2;
          const distanceToCenter = Math.max(0, itemCenterY - windowCenterY);
          const factor = Math.max(0, distanceToCenter / windowCenterY);

          const baseDistance = -150;
          const angleInDegrees = 30;
          const angleInRadians = (angleInDegrees * Math.PI) / 180;

          const translateX = baseDistance * factor * Math.cos(angleInRadians);
          const translateY = baseDistance * factor * Math.sin(angleInRadians);

          (car as HTMLElement).style.transform = `translate(${translateX}px, ${translateY}px)`;
        });

        // Buell motor parts explosion
        document.querySelectorAll('.project-card').forEach((item) => {
          const rect = item.getBoundingClientRect();
          const itemCenterY = rect.top + rect.height / 2;
          const distanceToCenter = Math.abs(itemCenterY - windowCenterY);
          const factor = Math.max(0, 1 - distanceToCenter / windowCenterY);

          const baseDistance = 30;
          const angleInDegrees = 60;
          const angleInRadians = (angleInDegrees * Math.PI) / 180;

          item.querySelectorAll('[data-part]').forEach((part) => {
            const partAttr = (part as HTMLElement).getAttribute('data-part');
            if (!partAttr) return;
            const partNumber = parseInt(partAttr, 10);
            const distance = baseDistance * partNumber * factor;

            const translateX = distance * Math.cos(angleInRadians);
            const translateY = -distance * Math.sin(angleInRadians);

            (part as HTMLElement).style.transform = `translate(${translateX}px, ${translateY}px)`;
          });
        });

        scrollAnimationFrame = 0;
      });
    };

    const parallaxContainer = document.querySelector('.parallax-container');
    if (parallaxContainer) {
      parallaxContainer.addEventListener('scroll', handleScroll);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      if (parallaxContainer) {
        parallaxContainer.removeEventListener('scroll', handleScroll);
      }
      if (mouseAnimationFrame) {
        cancelAnimationFrame(mouseAnimationFrame);
      }
      if (scrollAnimationFrame) {
        cancelAnimationFrame(scrollAnimationFrame);
      }
    };
  }, []);
  return (
    <div className="parallax-container">
      <ParallaxHeader />
      <div className="parallax-foreground">
        <div className="main-content home">
          <AboutMe content={aboutMeContent} />
          <div className="projects-section">
            <div className="projects-grid">
              <OpenSim2RealProject />
              <SelfDrivingCarProject />
              <Robot253Project />
              <A40AustinProject />
              <BuellProject />
              <FumeExtractorProject />
              <Esk8Project />
              <ThreeDPrinterProject />
              <ResumeProject />
            </div>
            <ContactForm />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
