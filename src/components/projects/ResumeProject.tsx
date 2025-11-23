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
    <BaseProjectItem config={projectConfig} className="resume">
      <div className="project-portfolio__item-image resume">
        <div className="tablet-div">
          <ProjectImage
            src="/assets/resume/foreground.png"
            className="foreground"
            style={{ opacity: 0 }}
          />
          <ProjectImage
            src="/assets/resume/background.png"
            className="background"
            style={{ opacity: 1 }}
          />
          <div 
            className="tablet-screen splash"
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
