import React from 'react';
import { BaseProjectItem, type ProjectConfig } from './BaseProjectItem';
import { TabletDisplay } from '../visuals';

const projectConfig: ProjectConfig = {
  id: 'resume',
  category: 'Offline Website',
  title: 'Resume',
  description: 'If you feel inclined to take the experience offline.',
  link: '/assets/resume/resume.pdf',
  buttonText: 'Download Resume',
  downloadable: true
};

export const ResumeProject: React.FC = () => {
  return (
    <BaseProjectItem config={projectConfig} className="project-resume">
      <div className="project-card-media">
        <div className="project-media-frame" style={{ height: '100%', maxHeight: '100%', aspectRatio: '3/4', margin: '0 auto', position: 'relative' }}>
          <TabletDisplay />
        </div>
      </div>
    </BaseProjectItem>
  );
};
