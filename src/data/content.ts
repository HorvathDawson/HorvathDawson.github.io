// data/content.ts

export interface ParallaxLayer {
  id: string;
  src: string;
  depth: number;
}

export interface AboutMeContent {
  title: string;
  description: string;
  tentImage: string; // Renamed from 'image'
  logsImage: string; // Added new property
}

export interface Project {
  id: string;
  category: string;
  title: string;
  description: string;
  link?: string;
  downloadable?: boolean;
  buttonText?: string;
  images: {
    foreground?: string;
    background?: string;
    splash?: string;
    gif?: string;
    additionalImages?: Array<{
      src: string;
      className?: string;
      type: 'foreground' | 'background' | 'splash' | 'part';
    }>;
  };
  animations?: {
    type: 'canvas' | 'rotation' | 'translation' | 'parts';
    config?: any;
  };
}

export const parallaxLayers: ParallaxLayer[] = [
  { id: 'layer0', src: '/assets/header/layer-0.png', depth: 0.1 },
  { id: 'layer1', src: '/assets/header/layer-1.png', depth: 0.2 },
  { id: 'layer2', src: '/assets/header/layer-2.png', depth: 0.3 },
  { id: 'layer3', src: '/assets/header/layer-3.png', depth: 0.4 },
  { id: 'layer4', src: '/assets/header/layer-4.png', depth: 0.5 },
  { id: 'layer5', src: '/assets/header/layer-5.png', depth: 0.6 },
];

export const aboutMeContent: AboutMeContent = {
  title: "Hi, I'm Dawson Horvath!",
  description: `I grew up working in a mechanics shop, so I was pulling things apart and putting them back together long before I got into engineering. I studied Engineering Physics at UBC, which covers everything from quantum mechanics to control systems to machine design. Between the shop and the degree, I ended up as a generalist comfortable with a wrench or a compiler. Professionally I do mechatronics and software: robots, imaging pipelines, embedded systems, web apps.

I spend most of my free time outside. I'm a TDI tech diver, and I mountain bike, paraglide, mountaineer, and fish whenever I can. Emperor Ridge on Mount Robson is the standout so far.`,
  tentImage: '/assets/about/tent.png',
  logsImage: '/assets/about/logs.png' // Make sure this file exists in your assets!
};

export const projects: Project[] = [
  {
    id: 'bc-fishing-regulations',
    category: 'Web App',
    title: 'Can I Fish This?',
    description: 'A web app that simplifies BC fishing regulations, helping anglers quickly find what they can fish, where, and when.',
    link: 'https://canifishthis.ca',
    buttonText: 'Visit Site',
    images: {
      foreground: '/assets/projects/bc-fishing-regulations/desktop-colored.svg',
      background: '/assets/projects/bc-fishing-regulations/desktop-outline.svg',
      splash: '/assets/projects/bc-fishing-regulations/website-demo.gif'
    }
  },
  {
    id: 'opensim2real',
    category: 'Opensource Robotics',
    title: 'OpenSim2Real',
    description: 'An open-source platform for sim-to-real reinforcement learning research, built around a low-cost monopod robot. Includes the physical robot, Gazebo simulation with OpenAI Gym environments, and a real-time backend for training on hardware.',
    link: 'https://opensim2real.github.io/os2r-superbuild/docs/index.html',
    buttonText: 'Explore More',
    images: {
      foreground: '/assets/projects/opensim2real/leg-colored-spritesheet.png',
      background: '/assets/projects/opensim2real/leg-outline-spritesheet.png'
    },
    animations: {
      type: 'canvas'
    }
  },
  {
    id: 'a40austin',
    category: 'In Progress',
    title: '1950 A40 Austin',
    description: 'Currently modernizing a 1950 Austin A40 by upgrading its suspension, brakes, and motor, blending modern performance with a classic design.',
    images: {
      foreground: '/assets/projects/a40-austin/colored.png',
      background: '/assets/projects/a40-austin/outline.png'
    },
    animations: {
      type: 'translation'
    }
  },
  {
    id: 'self-driving-car',
    category: 'Simulation',
    title: 'Self Driving Car',
    description: 'Simulated a self-driving robot in Gazebo and ROS using computer vision and machine learning to navigate roads, avoid obstacles, and process license plate data from parked cars.',
    images: {
      foreground: '/assets/projects/self-driving-car/computer-colored.svg',
      background: '/assets/projects/self-driving-car/computer-outline.svg',
      splash: '/assets/projects/self-driving-car/simulation-demo.gif',
      additionalImages: [
        { src: '/assets/projects/self-driving-car/keyboard-colored.svg', className: 'keyboard-foreground', type: 'foreground' },
        { src: '/assets/projects/self-driving-car/keyboard-outline.svg', className: 'keyboard-background', type: 'background' }
      ]
    },
    animations: {
      type: 'rotation',
      config: { axis: 'X', min: -60, max: 60 }
    }
  },
  {
    id: '253robot',
    category: 'Competition',
    title: 'Autonomous Robot',
    description: 'Designed an autonomous robot for the Engineering Physics Robot Competition, featuring a custom drivetrain, SPI communication, control loop and mechanical systems.',
    images: {
      foreground: '/assets/projects/competition-robot/colored.png',
      background: '/assets/projects/competition-robot/outline.png',
      splash: '/assets/projects/competition-robot/glow.png'
    }
  },
  {
    id: 'buell',
    category: 'Fix',
    title: 'Buell Motor Rebuild',
    description: 'Rebuilt a 2008 Buell XB9SX motor by disassembling, inspecting, and replacing worn components, requiring precision and expertise to restore performance and reliability.',
    images: {
      foreground: '/assets/projects/buell-lightning/engine/section-view.gif',
      background: '/assets/projects/buell-lightning/engine/case.png',
      additionalImages: [
        { src: '/assets/projects/buell-lightning/engine/left-cylinder.png', type: 'background' },
        { src: '/assets/projects/buell-lightning/engine/cylinder-barrel.png', type: 'part' },
        { src: '/assets/projects/buell-lightning/engine/rocker-box.png', type: 'part' },
        { src: '/assets/projects/buell-lightning/engine/rocker-box-top.png', type: 'part' },
        { src: '/assets/projects/buell-lightning/engine/push-rods.png', type: 'part' }
      ]
    },
    animations: {
      type: 'parts'
    }
  },
  {
    id: 'fume-extractor',
    category: 'Project',
    title: 'Fume Extractor',
    description: 'Designed and built a low-cost fume extractor arm with an inline fan, counterbalance system, friction joints, and a welded, mobile stand.',
    images: {
      foreground: '/assets/projects/fume-extractor/arm-colored.png',
      background: '/assets/projects/fume-extractor/arm-outline.png',
      splash: '/assets/projects/fume-extractor/glow.png',
      additionalImages: [
        { src: '/assets/projects/fume-extractor/fumes.gif', type: 'splash' }
      ]
    }
  },
  {
    id: 'esk8',
    category: 'Project',
    title: 'DIY E-Sk8',
    description: 'Designed and built a DIY electric skateboard with dual 6374 motors, a custom 10s4p Li-ion battery, and Vedder ESCs, optimized for daily commuting with waterproofing and tailored gearing.',
    images: {
      foreground: '/assets/projects/electric-skateboard/colored.png',
      background: '/assets/projects/electric-skateboard/outline.svg'
    }
  },
  {
    id: '3dprinter',
    category: 'Scholarship',
    title: 'Low-Cost 3D Printer Build',
    description: 'Designed and built a low-cost, functional 3D printer inspired by the Prusa i3 MK2, featuring an Arduino Mega, RAMPS 1.4 board, MDF frame, and custom wiring, balancing quality and cost.',
    images: {
      foreground: '/assets/projects/3d-printer/colored.png',
      background: '/assets/projects/3d-printer/outline.png'
    }
  },
  {
    id: 'resume',
    category: 'Offline Website',
    title: 'Resume',
    description: 'If you feel inclined to take the experience offline.',
    link: '/assets/resume/resume.pdf',
    downloadable: true,
    buttonText: 'Download Resume',
    images: {
      foreground: '/assets/resume/colored.png',
      background: '/assets/resume/outline.png'
    }
  }
];
