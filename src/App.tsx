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
  const parallaxContainerStyle: React.CSSProperties = {
    backgroundColor: '#FEDCC8',
    perspectiveOrigin: 'center',
    perspective: '100px',
    height: '100vh',
    overflowX: 'hidden',
    overflowY: 'auto',
    position: 'relative',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    display: 'flex'
  };

  const parallaxForegroundStyle: React.CSSProperties = {
    backgroundImage: 'url("/assets/parallax_header/foreground_color.png")',
    backgroundRepeat: 'no-repeat',
    backgroundPosition: 'center center',
    backgroundSize: 'cover',
    position: 'relative',
    top: 'calc(max(100vw, 500px) * 0.6666666667 * 0.99)',
    height: 'max-content',
    width: '100vw',
    minWidth: '100%',
    minHeight: '200vh',
    zIndex: 2,
    paddingTop: '100px'
  };
  // Match the layer-5 transform so the foreground aligns with the closest layer
  parallaxForegroundStyle.transform = `translateZ(0px) scale(1) translateY(calc((100vh - 66.6666666667vw) / 5))`;

  return (
    <div className="parallax-container" style={parallaxContainerStyle}>
      <ParallaxHeader />
      <div className="parallax-foreground" style={parallaxForegroundStyle}>
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
