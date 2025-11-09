/**
 * Logo Component for CareerStar
 * 
 * Displays the CareerStar logo with three variations:
 * - full: Logo with text and tagline (for login/register pages)
 * - compact: Logo with text only (for sidebar/header)
 * - icon: Icon only (for small spaces)
 * 
 * Uses optimized 500x500px PNG files
 */

import { useMemo } from 'react';

interface LogoProps {
  variant?: 'full' | 'compact' | 'icon';
  className?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
}

export const Logo = ({ variant = 'compact', className = '', size = 'md' }: LogoProps) => {
  const sizeClasses = useMemo(() => {
    switch (size) {
      case 'sm':
        return 'h-10 w-auto';
      case 'md':
        return 'h-14 w-auto';
      case 'lg':
        return 'h-20 w-auto';
      case 'xl':
        return 'h-32 w-auto';
      default:
        return 'h-14 w-auto';
    }
  }, [size]);

  // Icon only variant - just the star
  if (variant === 'icon') {
    return (
      <img
        src="/logo-icon.png"
        alt="CareerStar"
        className={`${className || sizeClasses} object-contain`}
        loading="eager"
      />
    );
  }

  // Compact variant (logo + text)
  if (variant === 'compact') {
    return (
      <div className={`flex items-center gap-3 ${className}`}>
        <img
          src="/logo-icon.png"
          alt="CareerStar Icon"
          className="h-10 w-10 object-contain"
          loading="eager"
        />
        <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          CareerStar
        </span>
      </div>
    );
  }

  // Full variant (logo + text + tagline)
  return (
    <img
      src="/logo-full.png"
      alt="CareerStar - Where Potential Meets Opportunity"
      className={`${className || sizeClasses} object-contain drop-shadow-lg`}
      loading="eager"
    />
  );
};
