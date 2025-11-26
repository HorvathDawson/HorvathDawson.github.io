import React from 'react';

interface AboutMeProps {
  content: {
    title: string;
    description: string;
    image: string;
  };
}

export const AboutMe: React.FC<AboutMeProps> = ({ content }) => {
  const styles: Record<string, React.CSSProperties> = {
    section: {
      marginBottom: '150px',
      height: 'auto',
      position: 'relative',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
    },
    contentWrapper: {
      maxWidth: '800px',
      padding: '20px',
      zIndex: 1,
      position: 'relative',
    },
    title: {
      fontSize: '40px',
      fontWeight: 700,
      lineHeight: '46px',
      wordBreak: 'break-word',
      hyphens: 'auto',
    },
    // .about-description class is preserved in CSS as requested, 
    // but specific overrides can go here if needed.
    
    imageContainer: {
      position: 'absolute',
      width: '90%',
      maxWidth: '450px',
      minWidth: '250px',
      zIndex: -1,
      aspectRatio: '1/1',
      height: 'auto',
      // inset is handled by the internal <style> tag below for responsiveness
    },
    img: {
      display: 'inline-block',
      width: '100%',
      height: '100%',
      position: 'absolute',
      top: 0,
    }
  };

  return (
    <>
      <style>
        {`
          /* Default positioning */
          .about-image-responsive {
            inset: -40% 0 0 50%;
          }
          /* Media Queries moved from CSS */
          @media screen and (max-width: 850px) {
            .about-image-responsive {
              inset: -20% 0 0 25%;
            }
          }
          @media screen and (max-width: 590px) {
            .about-image-responsive {
              inset: -150px 0 0 0;
            }
          }
          @media screen and (max-width: 450px) {
            .about-image-responsive {
              inset: -100px 0 0 0;
            }
          }
        `}
      </style>

      <div className="about-section" style={styles.section}>
        <div className="about-content" style={styles.contentWrapper}>
          <h1 className="section-title" style={styles.title}>
            {content.title}
          </h1>
          {/* Kept class 'about-description' as requested */}
          <p className="about-description">
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
        
        <div 
          className="about-image about-image-responsive" 
          style={styles.imageContainer}
        >
          <img 
            src={content.image} 
            alt="About me" 
            loading="lazy" 
            style={styles.img}
          />
        </div>
      </div>
    </>
  );
};