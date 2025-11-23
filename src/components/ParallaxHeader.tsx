import React from 'react';
import { parallaxLayers } from '../data/content';

export const ParallaxHeader: React.FC = () => {
  return (
    <>
      {parallaxLayers.map((layer) => (
        <div
          key={layer.id}
          className={`parallax-layer parallax-layer-depth-${layer.id.slice(-1)}`}
        >
          <img src={layer.src} alt="" />
        </div>
      ))}
    </>
  );
};

export default ParallaxHeader;
