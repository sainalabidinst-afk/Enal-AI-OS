'use client';

import VoiceAgentBuilder from '@/components/builder/VoiceAgentBuilder';

const defaultAgent = {
  name: '',
  sttProvider: 'whisper',
  ttsProvider: 'elevenlabs',
  voice: 'alloy',
  language: 'en-US',
  temperature: 0.7,
  maxTokens: 1024,
  prompt: '',
};

export default function VoiceBuilderPage() {
  return <VoiceAgentBuilder agent={defaultAgent} onChange={() => {}} />;
}
