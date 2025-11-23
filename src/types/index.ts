export interface Project {
  id: string;
  category: string;
  title: string;
  description: string;
  link?: string;
  downloadable?: boolean;
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
  buttonText?: string;
}

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

export interface ContactFormData {
  fullName: string;
  email: string;
  message: string;
}
