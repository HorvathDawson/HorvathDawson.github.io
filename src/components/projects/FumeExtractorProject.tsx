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
    <BaseProjectItem config={projectConfig} className="project-fume-extractor">
      <div className="project-card-image project-fume-extractor">
        <div className="project-card-media">
          <img
            src="/assets/projects/fume-extractor/arm.png"
            alt=""
            className="foreground-layer"
            loading="lazy"
            style={{ opacity: 0 }}
          />
          <img
            src="/assets/projects/fume-extractor/arm-edge.png"
            alt=""
            className="background-layer"
            loading="lazy"
            style={{ opacity: 1 }}
          />
          <img
            src="/assets/projects/fume-extractor/splash.png"
            alt=""
            className="splash-layer"
            loading="lazy"
            style={{ opacity: 0 }}
          />
          <img
            src="/assets/projects/fume-extractor/fumes.gif"
            alt=""
            className="splash-layer fume-animation"
            loading="lazy"
            style={{ opacity: 0 }}
          />
        </div>
      </div>
    </BaseProjectItem>
  );
};
