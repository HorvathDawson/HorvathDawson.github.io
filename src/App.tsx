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

    // Cleanup
    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      if (mouseAnimationFrame) {
        cancelAnimationFrame(mouseAnimationFrame);
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
