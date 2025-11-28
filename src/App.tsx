import React, { useEffect } from 'react';
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

  // --- NEW: SEO Metadata & Console Easter Eggs ---
  useEffect(() => {
    // 1. SEO / Metadata Injection
    document.title = "Dawson's Portfolio | Engineering & Design";

    const metaDesc = document.querySelector('meta[name="description"]');
    if (metaDesc) {
      metaDesc.setAttribute('content', 'Portfolio of Dawson: A showcase of robotics, software engineering, self-driving cars, and DIY fabrication projects.');
    } else {
      const meta = document.createElement('meta');
      meta.name = "description";
      meta.content = "Portfolio of Dawson: A showcase of robotics, software engineering, self-driving cars, and DIY fabrication projects.";
      document.head.appendChild(meta);
    }

    // 2. Console Easter Egg
    const styles = [
      'color: #ff4500',
      'background: #2a2a2a',
      'font-size: 14px',
      'padding: 10px',
      'border-radius: 5px',
      'border: 2px solid #ff8c00'
    ].join(';');

    const funMessage = `
    (
      )
     ( )  .   
      |  /_\  
    __|__/_|__ 
   /_________\ 
     |     |   
   
   Hey there, explorer! 🌲 
   If you're looking at this, you probably enjoy code as much as I do.
   
   Feel free to poke around the source or reach out via the contact form!
    `;

    console.log(`%c 🏕️ Welcome to the Portfolio! `, styles);
    console.log(funMessage);
    console.log("Built with React, TypeScript, and a lot of coffee ☕");

  }, []);
  // ----------------------------------------------

  useEffect(() => {
    // Mouse tracking for shuffle effect (Project Cards)
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

  // 1. CONTAINER STYLE
  // Removed "height: 100vh" and "overflow: auto". 
  // We want the Window to scroll, not this div.
  const appContainerStyle: React.CSSProperties = {
    backgroundColor: '#FEDCC8', // Background color behind parallax layers
    minHeight: '100vh',
    width: '100vw',
    position: 'relative',
    overflowX: 'hidden', // Prevents horizontal scrollbar if images are wide
  };

  // 2. CONTENT STYLE
  // This sits strictly BELOW the header.
  // We add zIndex to ensure it sits on top of any background artifacts.
  const mainContentStyle: React.CSSProperties = {
    backgroundImage: 'url("/assets/parallax_header/foreground_color.png")',
    backgroundRepeat: 'repeat-y', // Changed to repeat or no-repeat depending on your image
    backgroundPosition: 'top center',
    // backgroundSize: 'cover',
    position: 'relative',
    zIndex: 10, // Ensures content sits on top of the bottom of the parallax header
    width: '100%',
    paddingTop: '50px', // Spacing between header and first text
    paddingBottom: '0px'
  };

  return (
    <div className="app-container" style={appContainerStyle}>

      {/* The Header sits at the top. 
        Because we fixed ParallaxHeader.tsx to use 'relative' positioning 
        for the foreground, it will naturally push the content below it down.
      */}
      <ParallaxHeader />

      {/* Main Content Area */}
      <div className="parallax-foreground" style={mainContentStyle}>
        <div className="main-content home">
          <AboutMe content={aboutMeContent} />

          <div className="projects-content">
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
    </div>
  );
}

export default App;