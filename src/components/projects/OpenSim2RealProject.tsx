import React from 'react';
import { BaseProjectItem, type ProjectConfig } from './BaseProjectItem';
import { SpinningLeg } from '../visuals';

const projectConfig: ProjectConfig = {
  id: 'opensim2real',
  category: 'Opensource Robotics',
  title: 'OpenSim2Real',
  description: 'Open Sim2Real is a open source project striving to develop a simple inexpensive platform for Sim2Real research.',
  link: 'https://opensim2real.github.io/os2r-superbuild/docs/index.html',
  buttonText: 'Explore More'
};

export const OpenSim2RealProject: React.FC = () => {

  return (
    <BaseProjectItem config={projectConfig} className="project-opensim2real">
      <div className="project-card-media">
        <div className="project-media-frame" style={{ width: 'auto', maxHeight: '100%', aspectRatio: '637/824', margin: '0 auto', position: 'relative' }}>
          <SpinningLeg />
        </div>
      </div>
    </BaseProjectItem>
  );
};
