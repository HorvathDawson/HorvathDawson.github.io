import React from 'react';
import { BaseProjectItem, ProjectImage, type ProjectConfig } from './BaseProjectItem';

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
      <div className="project-card-image project-resume">
        <div className="tablet-frame">
          <ProjectImage
            src="/assets/resume/foreground.png"
            className="foreground-layer"
            style={{ opacity: 0 }}
          />
          <ProjectImage
            src="/assets/resume/background.png"
            className="background-layer"
            style={{ opacity: 1 }}
          />
          <div 
            className="tablet-display splash-layer"
            style={{ 
              opacity: 0,
              backgroundImage: 'url(/assets/resume/resume_rotated.png)',
              backgroundSize: 'cover',
              backgroundRepeat: 'no-repeat',
              backgroundPosition: 'center center'
            }}
          />
        </div>
      </div>
    </BaseProjectItem>
  );
};
