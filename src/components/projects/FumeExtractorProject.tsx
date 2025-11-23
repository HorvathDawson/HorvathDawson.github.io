import React from 'react';
import { BaseProjectItem, type ProjectConfig } from './BaseProjectItem';

const projectConfig: ProjectConfig = {
  id: 'fume-extractor',
  category: 'Project',
  title: 'Fume Extractor',
  description: 'Designed and built a low-cost fume extractor arm with an inline fan, counterbalance system, friction joints, and a welded, mobile stand.'
};

export const FumeExtractorProject: React.FC = () => {
  return (
    <BaseProjectItem config={projectConfig} className="fume-extractor">
      <div className="project-portfolio__item-image fume-extractor">
        <div className="project-portfolio__item-image-container">
          <img
            src="/assets/projects/fume-extractor/arm.png"
            alt=""
            className="foreground"
            loading="lazy"
            style={{ opacity: 0 }}
          />
          <img
            src="/assets/projects/fume-extractor/arm-edge.png"
            alt=""
            className="background"
            loading="lazy"
            style={{ opacity: 1 }}
          />
          <img
            src="/assets/projects/fume-extractor/splash.png"
            alt=""
            className="splash"
            loading="lazy"
            style={{ opacity: 0 }}
          />
          <img
            src="/assets/projects/fume-extractor/fumes.gif"
            alt=""
            className="splash fumes"
            loading="lazy"
            style={{ opacity: 0 }}
          />
        </div>
      </div>
    </BaseProjectItem>
  );
};
