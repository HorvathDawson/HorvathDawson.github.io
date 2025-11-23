import React, { useEffect, useRef } from 'react';
import { BaseProjectItem, ProjectImageContainer, type ProjectConfig } from './BaseProjectItem';

declare global {
  interface Window {
    gifler: any;
  }
}

const projectConfig: ProjectConfig = {
  id: 'opensim2real',
  category: 'Opensource Robotics',
  title: 'OpenSim2Real',
  description: 'Open Sim2Real is a open source project striving to develop a simple inexpensive platform for Sim2Real research.',
  link: 'https://opensim2real.github.io/os2r-superbuild/docs/index.html',
  buttonText: 'Explore More'
};

export const OpenSim2RealProject: React.FC = () => {
  const canvas1Ref = useRef<HTMLCanvasElement>(null);
  const canvas2Ref = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!window.gifler || !canvas1Ref.current || !canvas2Ref.current) return;

    const canvas1 = canvas1Ref.current;
    const canvas2 = canvas2Ref.current;

    let gif1, gif2;
    gif1 = window.gifler('/assets/projects/opensim2real/leg-spin-body-small.gif');
    gif2 = window.gifler('/assets/projects/opensim2real/leg-spin-edge-small.gif');

    gif1.get((animation: any) => {
      animation.animateInCanvas(canvas1, (frameCtx: any) => {
        frameCtx.drawImage(animation.image, 0, 0, canvas1.width, canvas1.height);
      });
    });

    gif2.get((animation: any) => {
      animation.animateInCanvas(canvas2, (frameCtx: any) => {
        frameCtx.drawImage(animation.image, 0, 0, canvas2.width, canvas2.height);
      });
    });
  }, []);

  return (
    <BaseProjectItem config={projectConfig} className="openSim2Real">
      <ProjectImageContainer>
        <img
          src="/assets/projects/opensim2real/leg-spin-body-small.gif"
          alt=""
          className="foreground"
          loading="lazy"
          style={{ opacity: 0, display: 'none' }}
        />
        <img
          src="/assets/projects/opensim2real/leg-spin-edge-small.gif"
          alt=""
          className="background"
          loading="lazy"
          style={{ opacity: 1, display: 'none' }}
        />
        <canvas
          ref={canvas1Ref}
          id="opensim2real-canvas1"
          className="foreground"
          style={{ opacity: 0 }}
        />
        <canvas
          ref={canvas2Ref}
          id="opensim2real-canvas2"
          className="background"
          style={{ opacity: 1 }}
        />
      </ProjectImageContainer>
    </BaseProjectItem>
  );
};
