import React from 'react';
import { BaseProjectItem, type ProjectConfig } from './BaseProjectItem';

const projectConfig: ProjectConfig = {
  id: '3dprinter',
  category: 'Scholarship',
  title: 'Low-Cost 3D Printer Build',
  description: 'Designed and built a low-cost, functional 3D printer inspired by the Prusa i3 MK2, featuring an Arduino Mega, RAMPS 1.4 board, MDF frame, and custom wiring, balancing quality and cost.'
};

export const ThreeDPrinterProject: React.FC = () => {
  return (
    <BaseProjectItem config={projectConfig} className="3dprinter">
      <div className="project-portfolio__item-image">
        <div className="project-portfolio__item-image-container">
          <img
            src="/assets/projects/3dprinter/foreground.png"
            alt=""
            className="foreground"
            loading="lazy"
            style={{ opacity: 0 }}
          />
          <img
            src="/assets/projects/3dprinter/background.png"
            alt=""
            className="background"
            loading="lazy"
            style={{ opacity: 1 }}
          />
        </div>
      </div>
    </BaseProjectItem>
  );
};
