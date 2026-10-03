import React from 'react';
import { View, Text, TouchableOpacity, FlatList } from 'react-native';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { ROUTES, RootStackParamList } from '../navigation/routes';

type HomeScreenProps = {
  navigation: NativeStackNavigationProp<RootStackParamList, 'Home'>;
};

const MENU_ITEMS = [
  { id: '1', title: 'Chat', route: ROUTES.CHAT as keyof RootStackParamList, description: 'Talk to Jenny AI' },
  { id: '2', title: 'Observability', route: ROUTES.OBSERVABILITY as keyof RootStackParamList, description: 'Traces & logs' },
  { id: '3', title: 'Settings', route: ROUTES.SETTINGS as keyof RootStackParamList, description: 'App configuration' },
];

export function HomeScreen({ navigation }: HomeScreenProps) {
  const renderItem = ({ item }: { item: typeof MENU_ITEMS[0] }) => (
    <TouchableOpacity
      className="bg-surface rounded-lg p-4 mb-3 border border-gray-800"
      onPress={() => navigation.navigate(item.route)}
    >
      <Text className="text-text-primary text-base font-semibold mb-1">{item.title}</Text>
      <Text className="text-text-secondary text-sm">{item.description}</Text>
    </TouchableOpacity>
  );

  return (
    <View className="flex-1 bg-background p-4">
      <Text className="text-text-primary text-2xl font-bold mb-2">Enal AI OS</Text>
      <Text className="text-text-secondary text-sm mb-6">Mobile Beta v3.2.0</Text>
      <FlatList data={MENU_ITEMS} keyExtractor={(item) => item.id} renderItem={renderItem} />
    </View>
  );
}
