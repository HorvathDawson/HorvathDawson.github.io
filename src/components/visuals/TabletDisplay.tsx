import React from 'react';

export interface TabletDisplayProps {
    className?: string;
}

export const TabletDisplay: React.FC<TabletDisplayProps> = ({ 
    className = '' 
}) => {
    return (
        <div className={`tablet-display-container ${className}`.trim()} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}>
            <div style={{ width: 720, height: 1040, maxWidth: '100%', maxHeight: '100%', position: 'relative' }}>
                <img
                    src="/assets/resume/foreground.png"
                    alt=""
                    className="foreground-layer"
                    loading="lazy"
                    style={{ opacity: 0, position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain' }}
                />
                <img
                    src="/assets/resume/background.png"
                    alt=""
                    className="background-layer"
                    loading="lazy"
                    style={{ opacity: 1, position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain' }}
                />
                {/* resume splash sits above tablet and is handled via .resume-splash in the component or global styles */}
                <div
                    className="resume-splash splash-layer"
                    style={{
                        opacity: 0,
                        position: 'absolute',
                        left: '23.6%',
                        right: '13.3%',
                        top: '8.2%',
                        bottom: '6%',
                        height: '82.3%',
                        width: '53.2%',
                        backgroundImage: 'url(/assets/resume/resume.png)',
                        backgroundSize: 'cover',
                        backgroundRepeat: 'no-repeat',
                        backgroundPosition: 'center center',
                        zIndex: 2147483647,
                        transform: 'translateZ(0) rotateX(54deg) rotate(44.9deg)'
                    }}
                >
                {/* overlay layer equivalent to :after */}
                <div style={{ position: 'absolute', inset: 0, backgroundColor: 'var(--purple)', opacity: 0.5 }} />
                </div>
            </div>
        </div>
    );
};
