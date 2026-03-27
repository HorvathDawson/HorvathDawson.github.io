import { useSyncExternalStore } from 'react';

/**
 * Centralized breakpoint definitions.
 * These match the CSS media-query breakpoints used in App.css.
 *
 *   mobile:  0 – 479px
 *   tablet:  480 – 991px
 *   desktop: 992px+
 */
export const BREAKPOINTS = {
  mobile: 479,
  tablet: 991,
} as const;

type Breakpoint = 'mobile' | 'tablet' | 'desktop';

function getBreakpoint(): Breakpoint {
  const w = window.innerWidth;
  if (w <= BREAKPOINTS.mobile) return 'mobile';
  if (w <= BREAKPOINTS.tablet) return 'tablet';
  return 'desktop';
}

// Shared mutable snapshot so every subscriber reads the same value.
let current: Breakpoint = typeof window !== 'undefined' ? getBreakpoint() : 'desktop';

const listeners = new Set<() => void>();

if (typeof window !== 'undefined') {
  window.addEventListener('resize', () => {
    const next = getBreakpoint();
    if (next !== current) {
      current = next;
      listeners.forEach((l) => l());
    }
  });
}

function subscribe(cb: () => void) {
  listeners.add(cb);
  return () => { listeners.delete(cb); };
}

function getSnapshot() {
  return current;
}

/**
 * React hook — returns 'mobile' | 'tablet' | 'desktop'.
 * Re-renders the component only when the breakpoint tier changes.
 */
export function useBreakpoint(): Breakpoint {
  return useSyncExternalStore(subscribe, getSnapshot, () => 'desktop' as Breakpoint);
}

/** Convenience booleans */
export function useIsMobile() { return useBreakpoint() === 'mobile'; }
export function useIsTablet() { return useBreakpoint() === 'tablet'; }
export function useIsDesktop() { return useBreakpoint() === 'desktop'; }
