import React from 'react';
import { View, Text, Modal, TouchableOpacity } from 'react-native';
import { Button } from '../Common/Button';

interface ConsentDialogProps {
  visible: boolean;
  title: string;
  description: string;
  onApprove: () => void;
  onDeny: () => void;
}

export function ConsentDialog({ visible, title, description, onApprove, onDeny }: ConsentDialogProps) {
  return (
    <Modal visible={visible} transparent animationType="fade">
      <View className="flex-1 items-center justify-center bg-black/70 p-4">
        <View className="bg-surface rounded-lg p-6 w-full max-w-md border border-gray-800">
          <Text className="text-text-primary text-lg font-semibold mb-2">{title}</Text>
          <Text className="text-text-secondary text-sm mb-6">{description}</Text>
          <View className="flex-row gap-3">
            <Button title="Deny" onPress={onDeny} variant="ghost" className="flex-1" />
            <Button title="Approve" onPress={onApprove} className="flex-1" />
          </View>
        </View>
      </View>
    </Modal>
  );
}
