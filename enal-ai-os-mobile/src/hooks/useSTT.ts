import { useState, useCallback } from 'react';
import { Audio } from 'expo-av';
import * as Speech from 'expo-speech';

export function useSTT() {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');

  const startListening = useCallback(async () => {
    try {
      const { status } = await Audio.requestPermissionsAsync();
      if (status !== 'granted') {
        throw new Error('Microphone permission not granted');
      }

      setIsListening(true);
      // TODO: Implement actual STT using expo-speech or react-native-voice
      // For now, this is a placeholder
      setTranscript('Listening...');
    } catch (error) {
      console.error('STT error:', error);
      setIsListening(false);
    }
  }, []);

  const stopListening = useCallback(() => {
    setIsListening(false);
    setTranscript('');
  }, []);

  return {
    isListening,
    transcript,
    startListening,
    stopListening,
  };
}

export function useTTS() {
  const speak = useCallback((text: string) => {
    try {
      Speech.speak(text, {
        language: 'id-ID',
        pitch: 1.25,
        rate: 0.85,
      });
    } catch (error) {
      console.error('TTS error:', error);
    }
  }, []);

  const stop = useCallback(() => {
    Speech.stop();
  }, []);

  return {
    speak,
    stop,
  };
}
