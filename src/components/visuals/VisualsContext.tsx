import React from 'react';

export const VisualsForceHoverContext = React.createContext<boolean | undefined>(undefined);

export const useVisualsForceHover = () => React.useContext(VisualsForceHoverContext);

export default VisualsForceHoverContext;
