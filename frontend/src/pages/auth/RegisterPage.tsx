import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useToast } from '../../contexts/ToastContext';
import { Spinner } from '../../components/common/LoadingComponents';
import { Logo } from '../../components/common/Logo';

export const RegisterPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    full_name: '',
  });
  const [isLoading, setIsLoading] = useState(false);
  const [showPasswordRequirements, setShowPasswordRequirements] = useState(false);
  
  const { register } = useAuth();
  const navigate = useNavigate();
  const { showSuccess, showError, showWarning } = useToast();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }));
  };

  // Password strength checks
  const passwordChecks = {
    minLength: formData.password.length >= 8,
    hasUppercase: /[A-Z]/.test(formData.password),
    hasNumber: /[0-9]/.test(formData.password),
    passwordsMatch: formData.password && formData.password === formData.confirmPassword,
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Client-side validation with specific messages
    if (!formData.full_name.trim()) {
      showWarning('Please enter your full name.');
      return;
    }

    if (!formData.email.trim()) {
      showWarning('Please enter your email address.');
      return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      showWarning('Please enter a valid email address.');
      return;
    }

    if (formData.password.length < 8) {
      showWarning('Password must be at least 8 characters long.');
      return;
    }

    if (!/[A-Z]/.test(formData.password)) {
      showWarning('Password must contain at least one uppercase letter.');
      return;
    }

    if (!/[0-9]/.test(formData.password)) {
      showWarning('Password must contain at least one number.');
      return;
    }

    if (formData.password !== formData.confirmPassword) {
      showWarning('Passwords do not match. Please try again.');
      return;
    }

    setIsLoading(true);

    try {
      const { confirmPassword, ...registerData } = formData;
      await register(registerData);
      showSuccess('Account created successfully! Welcome to CareerStar.');
      navigate('/dashboard');
    } catch (err: any) {
      // Handle specific error messages from backend
      const errorDetail = err.response?.data?.detail;
      const errorMessage = err.response?.data?.error?.message;
      const errorDetails = err.response?.data?.error?.details;
      
      if (errorDetail === 'Email already registered') {
        showError('This email is already registered. Please sign in or use a different email.');
      } else if (errorMessage) {
        // Show validation errors from backend
        if (errorDetails && Array.isArray(errorDetails)) {
          const messages = errorDetails.map((e: any) => e.msg || e.message).join(', ');
          showError(`Registration failed: ${messages}`);
        } else {
          showError(errorMessage);
        }
      } else {
        showError(errorDetail || 'Registration failed. Please try again.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        {/* Logo Section - Improved */}
        <div className="text-center space-y-6 mb-8">
          <div className="flex justify-center">
            <Logo variant="full" className="w-72 h-auto" />
          </div>
          <div>
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white">
              Create Your Account
            </h2>
            <p className="mt-2 text-base text-gray-600 dark:text-gray-400">
              Join CareerStar and start your career journey
            </p>
          </div>
        </div>
        
        {/* Form Card */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-gray-700">
          <form className="space-y-6" onSubmit={handleSubmit}>
            <div>
              <label htmlFor="full_name" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Full Name
              </label>
              <input
                id="full_name"
                name="full_name"
                type="text"
                required
                value={formData.full_name}
                onChange={handleChange}
                className="appearance-none block w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg placeholder-gray-400 dark:placeholder-gray-500 text-gray-900 dark:text-white bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                placeholder="John Doe"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Email address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                autoComplete="email"
                required
                value={formData.email}
                onChange={handleChange}
                className="appearance-none block w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg placeholder-gray-400 dark:placeholder-gray-500 text-gray-900 dark:text-white bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                placeholder="you@example.com"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Password
              </label>
              <input
                id="password"
                name="password"
                type="password"
                autoComplete="new-password"
                required
                value={formData.password}
                onChange={handleChange}
                onFocus={() => setShowPasswordRequirements(true)}
                className="appearance-none block w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg placeholder-gray-400 dark:placeholder-gray-500 text-gray-900 dark:text-white bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                placeholder="••••••••"
              />
              {showPasswordRequirements && formData.password && (
                <div className="mt-2 space-y-1 text-xs">
                  <div className={`flex items-center gap-1 ${passwordChecks.minLength ? 'text-green-600 dark:text-green-400' : 'text-gray-500 dark:text-gray-400'}`}>
                    <span>{passwordChecks.minLength ? '✓' : '○'}</span>
                    <span>At least 8 characters</span>
                  </div>
                  <div className={`flex items-center gap-1 ${passwordChecks.hasUppercase ? 'text-green-600 dark:text-green-400' : 'text-gray-500 dark:text-gray-400'}`}>
                    <span>{passwordChecks.hasUppercase ? '✓' : '○'}</span>
                    <span>One uppercase letter</span>
                  </div>
                  <div className={`flex items-center gap-1 ${passwordChecks.hasNumber ? 'text-green-600 dark:text-green-400' : 'text-gray-500 dark:text-gray-400'}`}>
                    <span>{passwordChecks.hasNumber ? '✓' : '○'}</span>
                    <span>One number</span>
                  </div>
                </div>
              )}
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                autoComplete="new-password"
                required
                value={formData.confirmPassword}
                onChange={handleChange}
                className="appearance-none block w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg placeholder-gray-400 dark:placeholder-gray-500 text-gray-900 dark:text-white bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                placeholder="••••••••"
              />
              {formData.confirmPassword && (
                <div className={`mt-2 text-xs flex items-center gap-1 ${passwordChecks.passwordsMatch ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                  <span>{passwordChecks.passwordsMatch ? '✓' : '✗'}</span>
                  <span>{passwordChecks.passwordsMatch ? 'Passwords match' : 'Passwords do not match'}</span>
                </div>
              )}
            </div>

          <div>
            <button
              type={"submit" as const}
              disabled={isLoading}
              className="group relative w-full flex justify-center items-center gap-2 py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-md hover:shadow-lg"
            >
              {isLoading && <Spinner size="sm" className="border-white border-t-transparent" />}
              {isLoading ? 'Creating account...' : 'Sign up'}
            </button>
          </div>

          <div className="text-center pt-4 border-t border-gray-200 dark:border-gray-700">
            <p className="text-sm text-gray-600 dark:text-gray-400">
              Already have an account?{' '}
              <Link to="/login" className="font-semibold text-blue-600 dark:text-blue-400 hover:text-blue-500 dark:hover:text-blue-300 transition-colors">
                Sign in
              </Link>
            </p>
          </div>
        </form>
        </div>
      </div>
    </div>
  );
};
