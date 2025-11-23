import React from 'react';
import type { AboutMeContent } from '../data/content';

interface AboutMeProps {
  content: AboutMeContent;
}

export const AboutMe: React.FC<AboutMeProps> = ({ content }) => {
  return (
    <div className="about-me">
      <div className="about-me__text">
        <h1 className="heading-3">{content.title}</h1>
        <p className="paragraph-2">
          {content.description.split('\n\n').map((paragraph: string, index: number) => (
            <React.Fragment key={index}>
              {paragraph}
              {index < content.description.split('\n\n').length - 1 && (
                <>
                  <br />
                  <br />
                </>
              )}
            </React.Fragment>
          ))}
        </p>
      </div>
      <div className="about-me__image">
        <img src={content.image} alt="About me" loading="lazy" />
      </div>
    </div>
  );
};

export default AboutMe;
