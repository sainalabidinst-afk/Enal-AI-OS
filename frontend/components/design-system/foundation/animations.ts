export const animations = {
  duration: {
    instant: "0ms",
    fast: "150ms",
    normal: "200ms",
    slow: "300ms",
    slower: "500ms",
  },
  easing: {
    linear: "linear",
    ease: "ease",
    easeIn: "ease-in",
    easeOut: "ease-out",
    easeInOut: "ease-in-out",
  },
  keyframes: {
    fadeIn: {
      from: { opacity: "0" },
      to: { opacity: "1" },
    },
    slideInRight: {
      from: { transform: "translateX(100%)" },
      to: { transform: "translateX(0)" },
    },
    slideInUp: {
      from: { transform: "translateY(100%)" },
      to: { transform: "translateY(0)" },
    },
    spin: {
      from: { transform: "rotate(0deg)" },
      to: { transform: "rotate(360deg)" },
    },
    pulse: {
      "0%, 100%": { opacity: "1" },
      "50%": { opacity: "0.5" },
    },
  },
} as const;

export type AnimationDuration = typeof animations.duration;
export type AnimationEasing = typeof animations.easing;
export type AnimationKeyframes = typeof animations.keyframes;
