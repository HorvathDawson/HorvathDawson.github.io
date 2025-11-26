import React from 'react';

interface AboutMeProps {
  content: {
    title: string;
    description: string;
    tentImage: string;
    logsImage: string;
  };
}

export const AboutMe: React.FC<AboutMeProps> = ({ content }) => {
  return (
    <section className="about-section">
      <style>
        {`
          /* --- LAYOUT --- */
          .about-section {
            position: relative;
            min-height: 700px; 
            margin-bottom: 150px;
            display: flex;
            flex-direction: column;
            align-items: center;
            overflow-x: visible; 
          }

          .about-content {
            max-width: 800px;
            padding: 60px 20px;
            text-align: center;
            position: relative;
            z-index: 10; 
          }

          .about-title {
            font-size: 40px;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 24px;
            word-break: break-word;
          }

          .about-paragraph {
            margin-bottom: 1.5em;
            font-size: 18px;
            line-height: 1.6;
          }

          /* --- MAIN GROUP WRAPPER --- */
          .about-image-responsive {
            position: absolute;
            z-index: -1; 
            
            width: 90%;
            max-width: 450px;
            min-width: 250px;
            aspect-ratio: 1/1;
            height: auto;

            inset: -30% 0 0 55%;
          }

          .tent-img {
            display: block;
            width: 100%;
            height: 100%;
            object-fit: contain;
            opacity: 0.9; 
          }

          /* --- CAMPFIRE GROUP --- */
          /* This container controls the SIZE of the entire campfire (logs + fire) */
          .campfire-group {
            position: absolute;
            z-index: 2;
            
            right: 95%; 
            bottom: 30%; 
            
            /* The fire scales relative to this width now */
            width: 180px; 
            height: auto;
            
            display: flex;
            justify-content: center;
            align-items: flex-end;
          }

          .logs-img {
            width: 100%; /* Take full width of group */
            height: auto;
            display: block;
            position: relative;
            z-index: 1; 
          }

          /* --- CSS FLAME --- */
          .fire-pit {
            position: absolute;
            z-index: 2; 
            
            /* SCALING LOGIC: 
               Width is % of the campfire-group. 
               Bottom is % to align with log image. */
            width: 50%;
            aspect-ratio: 1 / 1; 
            bottom: 40%; /* Sits slightly inside the logs */
            left: 50%;
            transform: translateX(-50%);
          }

          .flame {
            position: absolute;
            bottom: 0;
            left: 50%;
            border-radius: 50% 0 50% 50%;
            transform: translateX(-50%) rotate(-45deg);
          }

          /* Bloom / Glow */
          .glow-base {
            position: absolute;
            width: 150%;
            height: 150%;
            left: -25%;
            top: -25%;
            background: radial-gradient(circle, rgba(255,100,0,0.4) 0%, rgba(255,60,0,0) 70%);
            filter: blur(20px);
            animation: pulse-glow 3s infinite alternate;
          }

          /* Colors defined by percentages of the fire-pit container */
          .flame-red {
            width: 100%;
            height: 100%;
            background: #ff4500;
            box-shadow: 0 0 20px #ff4500;
            animation: burn 1s infinite alternate ease-in-out;
            z-index: 1;
          }

          .flame-orange {
            width: 75%;
            height: 75%;
            background: #ff8c00;
            box-shadow: 0 0 15px #ff8c00;
            animation: burn 1.5s infinite alternate-reverse ease-in-out;
            bottom: 5%;
            z-index: 2;
          }

          .flame-yellow {
            width: 50%;
            height: 50%;
            background: #ffd700;
            box-shadow: 0 0 10px #ffd700;
            animation: burn 2s infinite alternate ease-in-out;
            bottom: 10%;
            z-index: 3;
          }

          @keyframes burn {
            0% { transform: translateX(-50%) rotate(-45deg) scale(1); }
            100% { transform: translateX(-50%) rotate(-45deg) scale(1.1) translate(2px, -2px); }
          }
          
          @keyframes pulse-glow {
            0% { opacity: 0.4; transform: scale(1); }
            100% { opacity: 0.7; transform: scale(1.2); }
          }

          /* --- MEDIA QUERIES --- */
          
          @media screen and (max-width: 850px) {
            .about-image-responsive {
              inset: -20% 0 0 25%;
              opacity: 0.5; 
            }
          }

          @media screen and (max-width: 590px) {
            .about-section {
               min-height: auto; 
            }
            
            .tent-img {
              z-index: 5;
               margin: 0 auto; 
            }
            
            .campfire-group {
               right: auto;
               left: 10%; 
               bottom: 20px;
               /* Make logs slightly smaller on mid-mobile so they don't block text */
               width: 140px; 
            }
          }

          @media screen and (max-width: 450px) {
            .about-image-responsive {
              inset: -100px 0 0 0;
            }
            
            .campfire-group {
               right: auto;
               left: -5%; /* Pull slightly left */
               bottom: 20px;
               
               /* Defines size of logs AND fire together */
               width: 30%; 
               min-width: 80px; /* Don't get too tiny */
            }
          }
        `}
      </style>

      {/* TEXT CONTENT */}
      <div className="about-content">
        <h1 className="about-title">{content.title}</h1>
        <div className="about-description">
          {content.description.split('\n\n').map((paragraph, index) => (
            <p key={index} className="about-paragraph">
              {paragraph}
            </p>
          ))}
        </div>
      </div>

      {/* MAIN GROUP WRAPPER */}
      <div className="about-image-responsive">

        {/* CAMPFIRE */}
        <div className="campfire-group">
          <div className="fire-pit">
            <div className="glow-base"></div>
            <div className="flame flame-red"></div>
            <div className="flame flame-orange"></div>
            <div className="flame flame-yellow"></div>
          </div>
          <img
            src={content.logsImage}
            alt="Campfire logs"
            loading="lazy"
            className="logs-img"
          />
        </div>

        {/* TENT IMAGE */}
        <img
          src={content.tentImage}
          alt="Tent scene"
          loading="lazy"
          className="tent-img"
        />
      </div>
    </section>
  );
};