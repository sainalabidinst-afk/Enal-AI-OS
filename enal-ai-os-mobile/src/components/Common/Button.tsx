import React from 'react';
import { TouchableOpacity, Text, ActivityIndicator, View } from 'react-native';

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
}

export function Button({ title, onPress, variant = 'primary', size = 'md', disabled, loading }: ButtonProps) {
  const baseStyles = 'rounded-lg items-center justify-center';
  const sizeStyles = {
    sm: 'px-3 py-1.5',
    md: 'px-4 py-2',
    lg: 'px-6 py-3',
  };
  const variantStyles = {
    primary: 'bg-primary',
    secondary: 'bg-secondary',
    danger: 'bg-danger',
    ghost: 'bg-transparent border border-gray-600',
  };

  return (
    <TouchableOpacity
      onPress={onPress}
      disabled={disabled || loading}
      className={`${baseStyles} ${sizeStyles[size]} ${variantStyles[variant]} opacity-${disabled ? 50 : 100}`}
    >
      {loading ? (
        <ActivityIndicator color="#fff" />
      ) : (
        <Text className="text-white font-medium text-sm">{title}</Text>
      )}
    </TouchableOpacity>
  );
}
