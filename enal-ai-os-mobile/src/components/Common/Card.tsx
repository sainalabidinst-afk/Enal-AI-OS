import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

interface CardProps {
  children: React.ReactNode;
  title?: string;
  description?: string;
}

export function Card({ children, title, description }: CardProps) {
  return (
    <View className="bg-surface rounded-lg p-4 mb-4 border border-gray-800">
      {(title || description) && (
        <View className="mb-2">
          {title && <Text className="text-text-primary font-semibold text-base mb-1">{title}</Text>}
          {description && <Text className="text-text-secondary text-sm">{description}</Text>}
        </View>
      )}
      {children}
    </View>
  );
}
