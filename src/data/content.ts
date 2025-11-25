// Type definitions
export interface ParallaxLayer {
  id: string;
  src: string;
  depth: number;
}

export interface AboutMeContent {
  title: string;
  description: string;
  image: string;
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
  { id: 'layer0', src: '/assets/parallax_header/Layer__0.png', depth: 0.1 },
  { id: 'layer1', src: '/assets/parallax_header/Layer__1.png', depth: 0.2 },
  { id: 'layer2', src: '/assets/parallax_header/Layer__2.png', depth: 0.3 },
  { id: 'layer3', src: '/assets/parallax_header/Layer__3.png', depth: 0.4 },
  { id: 'layer4', src: '/assets/parallax_header/Layer__4.png', depth: 0.5 },
  { id: 'layer5', src: '/assets/parallax_header/Layer__5.png', depth: 0.6 },
];

export const aboutMeContent: AboutMeContent = {
  title: "Hi, I'm Dawson Horvath!",
  description: `I'm a mechatronic and software engineer with a degree in Engineering Physics, who is driven by a passion for designing innovative robotics and software systems. From building cell screening robots to crafting advanced imaging pipelines, I thrive at tackling complex challenges.

Outside of work, I'm an outdoor enthusiast and athlete. Whether it's scuba diving, mountain biking, climbing, or practicing martial arts like Brazilian jiu-jitsu and Muay Thai, I'm constantly seeking new adventures that push my limits and inspire my creativity. The perseverance and problem-solving I've honed through these activities directly influence my approach to engineering.`,
  image: '/assets/about_me/tent.png'
};

export const projects: Project[] = [
  {
    id: 'opensim2real',
    category: 'Opensource Robotics',
    title: 'OpenSim2Real',
    description: 'Open Sim2Real is a open source project striving to develop a simple inexpensive platform for Sim2Real research.',
    link: 'https://opensim2real.github.io/os2r-superbuild/docs/index.html',
    buttonText: 'Explore More',
    images: {
      foreground: '/assets/projects/opensim2real/leg-spin-body-small.gif',
      background: '/assets/projects/opensim2real/leg-spin-edge-small.gif'
    },
    animations: {
      type: 'canvas'
    }
  },
  {
    id: 'self-driving-car',
    category: 'Simulation',
    title: 'Self Driving Car',
    description: 'Simulated a self-driving robot in Gazebo and ROS using computer vision and machine learning to navigate roads, avoid obstacles, and process license plate data from parked cars.',
    images: {
      foreground: '/assets/projects/self-driving-car/computer-foreground.svg',
      background: '/assets/projects/self-driving-car/computer-background.svg',
      splash: '/assets/projects/self-driving-car/screen.gif',
      additionalImages: [
        { src: '/assets/projects/self-driving-car/computer-keys-foreground.svg', className: 'keyboard-foreground', type: 'foreground' },
        { src: '/assets/projects/self-driving-car/computer-keys-background.svg', className: 'keyboard-background', type: 'background' }
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
      foreground: '/assets/projects/253robot/foreground.png',
      background: '/assets/projects/253robot/background2.png',
      splash: '/assets/projects/253robot/splash.png'
    }
  },
  {
    id: 'a40austin',
    category: 'In Progress',
    title: '1950 A40 Austin',
    description: 'Currently modernizing a 1950 Austin A40 by upgrading its suspension, brakes, and motor, blending modern performance with a classic design.',
    images: {
      foreground: '/assets/projects/a40austin/foreground.png',
      background: '/assets/projects/a40austin/background.png'
    },
    animations: {
      type: 'translation'
    }
  },
  {
    id: 'buell',
    category: 'Fix',
    title: 'Buell Motor Rebuild',
    description: 'Rebuilt a 2008 Buell XB9SX motor by disassembling, inspecting, and replacing worn components, requiring precision and expertise to restore performance and reliability.',
    images: {
      foreground: '/assets/projects/buell/motor_images/section-view.gif',
      background: '/assets/projects/buell/motor_images/case.png',
      additionalImages: [
        { src: '/assets/projects/buell/motor_images/left-cylinder.png', type: 'background' },
        { src: '/assets/projects/buell/motor_images/cylinder-barrel.png', type: 'part' },
        { src: '/assets/projects/buell/motor_images/rocker-box.png', type: 'part' },
        { src: '/assets/projects/buell/motor_images/rocker-box-top.png', type: 'part' },
        { src: '/assets/projects/buell/motor_images/push-rods.png', type: 'part' }
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
      foreground: '/assets/projects/fume-extractor/arm.png',
      background: '/assets/projects/fume-extractor/arm-edge.png',
      splash: '/assets/projects/fume-extractor/splash.png',
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
      foreground: '/assets/projects/esk8/foreground.png',
      background: '/assets/projects/esk8/background.svg'
    }
  },
  {
    id: '3dprinter',
    category: 'Scholarship',
    title: 'Low-Cost 3D Printer Build',
    description: 'Designed and built a low-cost, functional 3D printer inspired by the Prusa i3 MK2, featuring an Arduino Mega, RAMPS 1.4 board, MDF frame, and custom wiring, balancing quality and cost.',
    images: {
      foreground: '/assets/projects/3dprinter/foreground.png',
      background: '/assets/projects/3dprinter/background.png'
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
      foreground: '/assets/resume/foreground.png',
      background: '/assets/resume/background.png'
    }
  }
];
