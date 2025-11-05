import { useTheme } from '../../contexts/ThemeContext';
import { SunIcon, MoonIcon } from '@heroicons/react/24/outline';
import { motion } from 'framer-motion';

export const ThemeToggle = () => {
  const { theme, toggleTheme } = useTheme();

  return (
    <motion.button
      onClick={toggleTheme}
      className="relative p-2 rounded-xl bg-gradient-to-br from-electric-cyan/20 to-stellar-purple/20 dark:from-electric-cyan/10 dark:to-stellar-purple/10 backdrop-blur-md border border-white/20 dark:border-white/10 shadow-glass hover:shadow-glow-cyan transition-all duration-300 group"
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      aria-label="Toggle theme"
    >
      <motion.div
        initial={false}
        animate={{
          rotate: theme === 'dark' ? 0 : 180,
          scale: theme === 'dark' ? 1 : 0,
        }}
        transition={{ duration: 0.3, ease: 'easeInOut' }}
        className="absolute inset-0 flex items-center justify-center"
      >
        <MoonIcon className="w-5 h-5 text-electric-cyan group-hover:text-cosmic-gold transition-colors duration-300" />
      </motion.div>
      
      <motion.div
        initial={false}
        animate={{
          rotate: theme === 'light' ? 0 : 180,
          scale: theme === 'light' ? 1 : 0,
        }}
        transition={{ duration: 0.3, ease: 'easeInOut' }}
        className="absolute inset-0 flex items-center justify-center"
      >
        <SunIcon className="w-5 h-5 text-amber-gold group-hover:text-cosmic-gold transition-colors duration-300" />
      </motion.div>
      
      {/* Invisible spacer to maintain button size */}
      <div className="w-5 h-5 opacity-0">
        <SunIcon className="w-5 h-5" />
      </div>
      
      {/* Glow effect */}
      <div className="absolute inset-0 rounded-xl bg-gradient-to-br from-electric-cyan/0 to-stellar-purple/0 group-hover:from-electric-cyan/30 group-hover:to-stellar-purple/30 transition-all duration-300 blur-xl -z-10" />
    </motion.button>
  );
};
