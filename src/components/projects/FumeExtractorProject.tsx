import React from 'react';
import { BaseProjectItem, type ProjectConfig } from './BaseProjectItem';
import { FumeExtractorArm } from '../visuals';

const projectConfig: ProjectConfig = {
  id: 'fume-extractor',
  category: 'Project',
  title: 'Fume Extractor',
  description: 'Designed and built a low-cost fume extractor arm with an inline fan, counterbalance system, friction joints, and a welded, mobile stand.'
};

export const FumeExtractorProject: React.FC = () => {
  return (
    <BaseProjectItem config={projectConfig} className="project-fume-extractor">
      <div className="project-card-media">
        <div className="project-media-frame" style={{ width: 'auto', height: '100%', aspectRatio: '4/3', margin: '0 auto', position: 'relative' }}>
          <FumeExtractorArm />
        </div>
      </div>
    </BaseProjectItem>
  );
};
