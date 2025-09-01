"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { Eye, EyeOff, User, Mail, Lock, Building, Phone, MapPin, AlertCircle, CheckCircle } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface RegisterFormProps {
  onSuccess?: (user: any) => void;
  onError?: (error: string) => void;
  redirectTo?: string;
}

interface RegisterData {
  full_name: string;
  email: string;
  username: string;
  password: string;
  confirm_password: string;
  company: string;
  job_title: string;
  phone: string;
  location: string;
  role: string;
}

const USER_ROLES = [
  { value: 'viewer', label: 'Viewer', description: 'Read-only access to projects and reports' },
  { value: 'engineer', label: 'Engineer', description: 'Technical implementation and development' },
  { value: 'manager', label: 'Manager', description: 'Project management and team coordination' },
  { value: 'admin', label: 'Admin', description: 'System administration and user management' }
];

export default function RegisterForm({ onSuccess, onError, redirectTo = '/dashboard' }: RegisterFormProps) {
  const router = useRouter();
  const [formData, setFormData] = useState<RegisterData>({
    full_name: '',
    email: '',
    username: '',
    password: '',
    confirm_password: '',
    company: '',
    job_title: '',
    phone: '',
    location: '',
    role: 'viewer'
  });
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [errors, setErrors] = useState<Partial<RegisterData>>({});
  const [currentStep, setCurrentStep] = useState(1);
  const [isPasswordValid, setIsPasswordValid] = useState(false);

  const validateForm = (): boolean => {
    const newErrors: Partial<RegisterData> = {};

    // Full name validation
    if (!formData.full_name.trim()) {
      newErrors.full_name = 'Full name is required';
    } else if (formData.full_name.trim().length < 2) {
      newErrors.full_name = 'Full name must be at least 2 characters long';
    }

    // Email validation
    if (!formData.email) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    // Username validation
    if (!formData.username) {
      newErrors.username = 'Username is required';
    } else if (formData.username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters long';
    } else if (!/^[a-zA-Z0-9_]+$/.test(formData.username)) {
      newErrors.username = 'Username can only contain letters, numbers, and underscores';
    }

    // Password validation
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (formData.password.length < 8) {
      newErrors.password = 'Password must be at least 8 characters long';
    } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(formData.password)) {
      newErrors.password = 'Password must contain at least one uppercase letter, one lowercase letter, and one number';
    }

    // Confirm password validation
    if (!formData.confirm_password) {
      newErrors.confirm_password = 'Please confirm your password';
    } else if (formData.password !== formData.confirm_password) {
      newErrors.confirm_password = 'Passwords do not match';
    }

    // Company validation
    if (!formData.company.trim()) {
      newErrors.company = 'Company name is required';
    }

    // Job title validation
    if (!formData.job_title.trim()) {
      newErrors.job_title = 'Job title is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    
    // Clear error when user starts typing
    if (errors[name as keyof RegisterData]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
    }

    // Update password validation
    if (name === 'password') {
      const isValid = value.length >= 8 && /(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(value);
      setIsPasswordValid(isValid);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) return;

    setIsLoading(true);
    setErrors({});

    try {
      const response = await fetch('/api/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          full_name: formData.full_name,
          email: formData.email,
          username: formData.username,
          password: formData.password,
          company: formData.company,
          job_title: formData.job_title,
          phone: formData.phone,
          location: formData.location,
          role: formData.role
        }),
      });

      const data = await response.json();

      if (response.ok) {
        onSuccess?.(data.user);
        router.push('/login?message=Registration successful. Please sign in.');
      } else {
        onError?.(data.detail || 'Registration failed. Please try again.');
      }
    } catch (error) {
      console.error('Registration error:', error);
      onError?.('Network error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const getPasswordStrength = (password: string): { score: number; label: string; color: string } => {
    let score = 0;
    if (password.length >= 8) score++;
    if (/[A-Z]/.test(password)) score++;
    if (/[a-z]/.test(password)) score++;
    if (/[0-9]/.test(password)) score++;
    if (/[^A-Za-z0-9]/.test(password)) score++;

    const labels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
    const colors = ['#ef4444', '#f97316', '#eab308', '#22c55e', '#16a34a'];
    
    return {
      score: Math.min(score, 4),
      label: labels[score],
      color: colors[score]
    };
  };

  const passwordStrength = getPasswordStrength(formData.password);

  const nextStep = () => {
    if (currentStep === 1) {
      // Validate step 1
      const step1Errors: Partial<RegisterData> = {};
      if (!formData.full_name.trim()) step1Errors.full_name = 'Full name is required';
      if (!formData.email) step1Errors.email = 'Email is required';
      if (!formData.username) step1Errors.username = 'Username is required';
      if (!formData.password) step1Errors.password = 'Password is required';
      
      if (Object.keys(step1Errors).length === 0) {
        setCurrentStep(2);
      } else {
        setErrors(step1Errors);
      }
    }
  };

  const prevStep = () => {
    setCurrentStep(currentStep - 1);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-white to-purple-50 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-2xl"
      >
        <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
          {/* Header */}
          <div className="text-center mb-8">
            <motion.div
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
              className="w-16 h-16 bg-gradient-to-r from-green-600 to-blue-600 rounded-full flex items-center justify-center mx-auto mb-4"
            >
              <User className="w-8 h-8 text-white" />
            </motion.div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Create Account</h1>
            <p className="text-gray-600">Join CloudMind and start managing your cloud infrastructure</p>
          </div>

          {/* Progress Bar */}
          <div className="mb-8">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">Step {currentStep} of 2</span>
              <span className="text-sm text-gray-500">{currentStep === 1 ? 'Account Details' : 'Profile Information'}</span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2">
              <motion.div
                className="bg-gradient-to-r from-green-600 to-blue-600 h-2 rounded-full"
                initial={{ width: '50%' }}
                animate={{ width: currentStep === 1 ? '50%' : '100%' }}
                transition={{ duration: 0.3 }}
              />
            </div>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {currentStep === 1 ? (
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3 }}
                className="space-y-6"
              >
                {/* Full Name */}
                <div>
                  <label htmlFor="full_name" className="block text-sm font-medium text-gray-700 mb-2">
                    Full Name *
                  </label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type="text"
                      id="full_name"
                      name="full_name"
                      value={formData.full_name}
                      onChange={handleInputChange}
                      className={`w-full pl-10 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${
                        errors.full_name ? 'border-red-300 bg-red-50' : 'border-gray-300'
                      }`}
                      placeholder="Enter your full name"
                    />
                    <AnimatePresence>
                      {errors.full_name && (
                        <motion.div
                          initial={{ opacity: 0, y: -10 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: -10 }}
                          className="flex items-center mt-2 text-sm text-red-600"
                        >
                          <AlertCircle className="w-4 h-4 mr-1" />
                          {errors.full_name}
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                </div>

                {/* Email */}
                <div>
                  <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                    Email Address *
                  </label>
                  <div className="relative">
                    <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleInputChange}
                      className={`w-full pl-10 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${
                        errors.email ? 'border-red-300 bg-red-50' : 'border-gray-300'
                      }`}
                      placeholder="Enter your email address"
                    />
                    <AnimatePresence>
                      {errors.email && (
                        <motion.div
                          initial={{ opacity: 0, y: -10 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: -10 }}
                          className="flex items-center mt-2 text-sm text-red-600"
                        >
                          <AlertCircle className="w-4 h-4 mr-1" />
                          {errors.email}
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                </div>

                {/* Username */}
                <div>
                  <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-2">
                    Username *
                  </label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type="text"
                      id="username"
                      name="username"
                      value={formData.username}
                      onChange={handleInputChange}
                      className={`w-full pl-10 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${
                        errors.username ? 'border-red-300 bg-red-50' : 'border-gray-300'
                      }`}
                      placeholder="Choose a username"
                    />
                    <AnimatePresence>
                      {errors.username && (
                        <motion.div
                          initial={{ opacity: 0, y: -10 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: -10 }}
                          className="flex items-center mt-2 text-sm text-red-600"
                        >
                          <AlertCircle className="w-4 h-4 mr-1" />
                          {errors.username}
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                </div>

                {/* Password */}
                <div>
                  <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                    Password *
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type={showPassword ? 'text' : 'password'}
                      id="password"
                      name="password"
                      value={formData.password}
                      onChange={handleInputChange}
                      className={`w-full pl-10 pr-12 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${
                        errors.password ? 'border-red-300 bg-red-50' : 'border-gray-300'
                      }`}
                      placeholder="Create a strong password"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword(!showPassword)}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                    >
                      {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                    
                    {/* Password Strength Indicator */}
                    {formData.password && (
                      <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        className="mt-2"
                      >
                        <div className="flex items-center space-x-2">
                          <div className="flex-1 bg-gray-200 rounded-full h-2">
                            <div
                              className="h-2 rounded-full transition-all duration-300"
                              style={{
                                width: `${(passwordStrength.score + 1) * 20}%`,
                                backgroundColor: passwordStrength.color
                              }}
                            />
                          </div>
                          <span className="text-xs text-gray-600">{passwordStrength.label}</span>
                        </div>
                      </motion.div>
                    )}
                    
                    <AnimatePresence>
                      {errors.password && (
                        <motion.div
                          initial={{ opacity: 0, y: -10 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: -10 }}
                          className="flex items-center mt-2 text-sm text-red-600"
                        >
                          <AlertCircle className="w-4 h-4 mr-1" />
                          {errors.password}
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                </div>

                {/* Confirm Password */}
                <div>
                  <label htmlFor="confirm_password" className="block text-sm font-medium text-gray-700 mb-2">
                    Confirm Password *
                  </label>
                  <div className="relative">
                    <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type={showConfirmPassword ? 'text' : 'password'}
                      id="confirm_password"
                      name="confirm_password"
                      value={formData.confirm_password}
                      onChange={handleInputChange}
                      className={`w-full pl-10 pr-12 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${
                        errors.confirm_password ? 'border-red-300 bg-red-50' : 'border-gray-300'
                      }`}
                      placeholder="Confirm your password"
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600 transition-colors"
                    >
                      {showConfirmPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                    </button>
                    
                    <AnimatePresence>
                      {errors.confirm_password && (
                        <motion.div
                          initial={{ opacity: 0, y: -10 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: -10 }}
                          className="flex items-center mt-2 text-sm text-red-600"
                        >
                          <AlertCircle className="w-4 h-4 mr-1" />
                          {errors.confirm_password}
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                </div>

                {/* Next Button */}
                <motion.button
                  type="button"
                  onClick={nextStep}
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  className="w-full py-3 px-4 rounded-lg font-medium text-white bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 transition-all duration-200"
                >
                  Next Step
                </motion.button>
              </motion.div>
            ) : (
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.3 }}
                className="space-y-6"
              >
                {/* Company */}
                <div>
                  <label htmlFor="company" className="block text-sm font-medium text-gray-700 mb-2">
                    Company *
                  </label>
                  <div className="relative">
                    <Building className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type="text"
                      id="company"
                      name="company"
                      value={formData.company}
                      onChange={handleInputChange}
                      className={`w-full pl-10 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${
                        errors.company ? 'border-red-300 bg-red-50' : 'border-gray-300'
                      }`}
                      placeholder="Enter your company name"
                    />
                    <AnimatePresence>
                      {errors.company && (
                        <motion.div
                          initial={{ opacity: 0, y: -10 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: -10 }}
                          className="flex items-center mt-2 text-sm text-red-600"
                        >
                          <AlertCircle className="w-4 h-4 mr-1" />
                          {errors.company}
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                </div>

                {/* Job Title */}
                <div>
                  <label htmlFor="job_title" className="block text-sm font-medium text-gray-700 mb-2">
                    Job Title *
                  </label>
                  <div className="relative">
                    <User className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type="text"
                      id="job_title"
                      name="job_title"
                      value={formData.job_title}
                      onChange={handleInputChange}
                      className={`w-full pl-10 pr-4 py-3 border rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 ${
                        errors.job_title ? 'border-red-300 bg-red-50' : 'border-gray-300'
                      }`}
                      placeholder="Enter your job title"
                    />
                    <AnimatePresence>
                      {errors.job_title && (
                        <motion.div
                          initial={{ opacity: 0, y: -10 }}
                          animate={{ opacity: 1, y: 0 }}
                          exit={{ opacity: 0, y: -10 }}
                          className="flex items-center mt-2 text-sm text-red-600"
                        >
                          <AlertCircle className="w-4 h-4 mr-1" />
                          {errors.job_title}
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>
                </div>

                {/* Phone */}
                <div>
                  <label htmlFor="phone" className="block text-sm font-medium text-gray-700 mb-2">
                    Phone Number
                  </label>
                  <div className="relative">
                    <Phone className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type="tel"
                      id="phone"
                      name="phone"
                      value={formData.phone}
                      onChange={handleInputChange}
                      className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                      placeholder="Enter your phone number"
                    />
                  </div>
                </div>

                {/* Location */}
                <div>
                  <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-2">
                    Location
                  </label>
                  <div className="relative">
                    <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                    <input
                      type="text"
                      id="location"
                      name="location"
                      value={formData.location}
                      onChange={handleInputChange}
                      className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                      placeholder="Enter your location"
                    />
                  </div>
                </div>

                {/* Role Selection */}
                <div>
                  <label htmlFor="role" className="block text-sm font-medium text-gray-700 mb-2">
                    Role *
                  </label>
                  <select
                    id="role"
                    name="role"
                    value={formData.role}
                    onChange={handleInputChange}
                    className="w-full py-3 px-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  >
                    {USER_ROLES.map((role) => (
                      <option key={role.value} value={role.value}>
                        {role.label} - {role.description}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Navigation Buttons */}
                <div className="flex space-x-4">
                  <motion.button
                    type="button"
                    onClick={prevStep}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    className="flex-1 py-3 px-4 rounded-lg font-medium text-gray-700 bg-gray-100 hover:bg-gray-200 transition-all duration-200"
                  >
                    Previous
                  </motion.button>
                  <motion.button
                    type="submit"
                    disabled={isLoading}
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    className={`flex-1 py-3 px-4 rounded-lg font-medium text-white transition-all duration-200 ${
                      isLoading
                        ? 'bg-gray-400 cursor-not-allowed'
                        : 'bg-gradient-to-r from-green-600 to-blue-600 hover:from-green-700 hover:to-blue-700'
                    }`}
                  >
                    {isLoading ? (
                      <div className="flex items-center justify-center">
                        <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2" />
                        Creating Account...
                      </div>
                    ) : (
                      'Create Account'
                    )}
                  </motion.button>
                </div>
              </motion.div>
            )}
          </form>

          {/* Footer */}
          <div className="mt-8 text-center">
            <p className="text-sm text-gray-600">
              Already have an account?{' '}
              <button
                type="button"
                className="text-blue-600 hover:text-blue-800 font-medium transition-colors"
              >
                Sign in
              </button>
            </p>
          </div>
        </div>
      </motion.div>
    </div>
  );
} 