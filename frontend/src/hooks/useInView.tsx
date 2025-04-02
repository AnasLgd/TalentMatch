
import { useEffect, useRef, useState } from 'react';

interface InViewOptions {
  threshold?: number;
  rootMargin?: string;
}

export const useInView = <T extends HTMLElement>(options: InViewOptions = {}) => {
  const [inView, setInView] = useState(false);
  const ref = useRef<T>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        setInView(entry.isIntersecting);
      },
      {
        threshold: options.threshold || 0,
        rootMargin: options.rootMargin || '0px',
      }
    );

    const currentRef = ref.current;

    if (currentRef) {
      observer.observe(currentRef);
    }

    return () => {
      if (currentRef) {
        observer.unobserve(currentRef);
      }
    };
  }, [options.threshold, options.rootMargin]);

  return { ref, inView };
};
