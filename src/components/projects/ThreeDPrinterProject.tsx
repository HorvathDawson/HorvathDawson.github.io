import React from 'react';
import { BaseProjectItem, type ProjectConfig } from './BaseProjectItem';
import { PrinterDisplay } from '../visuals';

const projectConfig: ProjectConfig = {
  id: '3dprinter',
  category: 'Scholarship',
  title: 'Low-Cost 3D Printer Build',
  description: 'Designed and built a low-cost, functional 3D printer inspired by the Prusa i3 MK2, featuring an Arduino Mega, RAMPS 1.4 board, MDF frame, and custom wiring, balancing quality and cost.'
};

export const ThreeDPrinterProject: React.FC = () => {
  return (
    <BaseProjectItem config={projectConfig} className="3dprinter">
      <PrinterDisplay />
    </BaseProjectItem>
  );
};
