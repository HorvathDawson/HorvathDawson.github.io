import React from 'react';

export interface TabletDisplayProps {
    className?: string;
    forceHover?: boolean;
}

export const TabletDisplay: React.FC<TabletDisplayProps> = ({ 
    className = '',
    forceHover
}) => {
    const effectiveForceHover = forceHover ?? false;

    return (
        <div data-tablet-display className={className} style={{ position: 'absolute', inset: 0, width: '100%', height: '100%' }}>
            <div style={{ width: 720, height: 1040, maxWidth: '100%', maxHeight: '100%', position: 'relative' }}>
                <img
                    src="/assets/resume/foreground.png"
                    alt=""
                    className="foreground-layer"
                    loading="lazy"
                    style={{ opacity: effectiveForceHover ? 1 : 0, position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain' }}
                />
                <img
                    src="/assets/resume/background.png"
                    alt=""
                    className="background-layer"
                    loading="lazy"
                    style={{ opacity: effectiveForceHover ? 0 : 1, position: 'absolute', inset: 0, width: '100%', height: '100%', objectFit: 'contain' }}
                />
                {/* resume splash sits above tablet and is handled via .resume-splash in the component or global styles */}
                        <div
                            data-resume-splash
                            className="splash-layer"
                    style={{
                                opacity: effectiveForceHover ? 1 : 0,
                                position: 'absolute',
                                top: '50%',
                                left: '50%',
                                transform: 'translate(-50%, -50%) rotateX(54deg) rotate(44.9deg)',
                                aspectRatio: '1 / 1.4142',
                                width: '50.6%',
                                height: 'auto',
                                backgroundImage: 'url(/assets/resume/resume.png)',
                                backgroundSize: 'cover',
                                backgroundRepeat: 'no-repeat',
                                backgroundPosition: 'center center',
                                zIndex: 2147483647,
                    }}
                >
                {/* overlay layer equivalent to :after */}
                <div style={{ position: 'absolute', inset: 0, backgroundColor: 'var(--purple)', opacity: 0.5 }} />
                </div>
            </div>
            </div>
    );
};
