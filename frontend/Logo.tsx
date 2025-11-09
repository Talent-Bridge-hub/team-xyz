/**
 * Logo Component for CareerStar
 * 
 * Displays the CareerStar logo with three variations:
 * - full: Logo with text and tagline (for login/register pages)
 * - compact: Logo with text only (for sidebar/header)
 * - icon: Icon only (for small spaces)
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
        return variant === 'icon' ? 'w-8 h-8' : 'h-8';
      case 'md':
        return variant === 'icon' ? 'w-12 h-12' : 'h-12';
      case 'lg':
        return variant === 'icon' ? 'w-16 h-16' : 'h-16';
      case 'xl':
        return variant === 'icon' ? 'w-24 h-24' : 'h-24';
      default:
        return variant === 'icon' ? 'w-12 h-12' : 'h-12';
    }
  }, [size, variant]);

  // Icon only variant
  if (variant === 'icon') {
    return (
      <img
        src="/logo-icon.png"
        alt="CareerStar"
        className={`${sizeClasses} ${className}`}
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
          className={sizeClasses}
        />
        <span className={`font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent ${
          size === 'sm' ? 'text-lg' : size === 'lg' ? 'text-3xl' : size === 'xl' ? 'text-4xl' : 'text-2xl'
        }`}>
          CareerStar
        </span>
      </div>
    );
  }

  // Full variant (logo + text + tagline)
  return (
    <div className={`flex flex-col items-center ${className}`}>
      <img
        src="/logo-full.png"
        alt="CareerStar - Where Potential Meets Opportunity"
        className={sizeClasses}
      />
    </div>
  );
};
