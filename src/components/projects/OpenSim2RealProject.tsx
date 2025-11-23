import React from 'react';
import { BaseProjectItem, type ProjectConfig } from './BaseProjectItem';

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
      <div className="project-card-image project-opensim2real">
        <div className="project-card-media">
          {/* Body spin animation - shows on hover */}
          <img
            src="/assets/projects/opensim2real/leg-spin-body-small.gif"
            alt=""
            className="foreground-layer"
            loading="lazy"
            style={{ opacity: 0 }}
          />
          {/* Edge spin animation - shows by default */}
          <img
            src="/assets/projects/opensim2real/leg-spin-edge-small.gif"
            alt=""
            className="background-layer"
            loading="lazy"
            style={{ opacity: 1 }}
          />
        </div>
      </div>
    </BaseProjectItem>
  );
};
