'use client';

import React, { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Slider } from '@/components/ui/slider';
import { Tabs, TabPanel } from '@/components/ui/tabs';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  Mic,
  MicOff,
  Phone,
  PhoneOff,
  Settings,
  Save,
  Play,
  History,
  Volume2,
} from 'lucide-react';

interface VoiceAgentBuilderProps {
  agent: {
    id?: string;
    name: string;
    sttProvider: string;
    ttsProvider: string;
    voice: string;
    language: string;
    temperature: number;
    maxTokens: number;
    prompt: string;
  };
  onChange: (agent: VoiceAgentBuilderProps['agent']) => void;
  onSave?: () => void;
  onRun?: () => void;
}

const sttProviders = [
  { value: 'whisper', label: 'OpenAI Whisper' },
  { value: 'deepgram', label: 'Deepgram' },
  { value: 'google', label: 'Google Speech-to-Text' },
];

const ttsProviders = [
  { value: 'elevenlabs', label: 'ElevenLabs' },
  { value: 'azure', label: 'Azure TTS' },
  { value: 'openai', label: 'OpenAI TTS' },
];

const voices = [
  { value: 'alloy', label: 'Alloy' },
  { value: 'echo', label: 'Echo' },
  { value: 'fable', label: 'Fable' },
  { value: 'onyx', label: 'Onyx' },
  { value: 'nova', label: 'Nova' },
  { value: 'shimmer', label: 'Shimmer' },
];

const languages = [
  { value: 'en-US', label: 'English (US)' },
  { value: 'id-ID', label: 'Indonesian' },
  { value: 'es-ES', label: 'Spanish' },
  { value: 'fr-FR', label: 'French' },
  { value: 'de-DE', label: 'German' },
  { value: 'ja-JP', label: 'Japanese' },
];

const VoiceAgentBuilder: React.FC<VoiceAgentBuilderProps> = ({
  agent,
  onChange,
  onSave,
  onRun,
}) => {
  const [isRecording, setIsRecording] = useState(false);
  const [callDuration, setCallDuration] = useState(0);
  const [isInCall, setIsInCall] = useState(false);
  const [activeTab, setActiveTab] = React.useState('config');
  const intervalRef = useRef<number | null>(null);

  const update = (patch: Partial<VoiceAgentBuilderProps['agent']>) => {
    onChange({ ...agent, ...patch });
  };

  const startCall = () => {
    setIsInCall(true);
    setCallDuration(0);
    intervalRef.current = window.setInterval(() => {
      setCallDuration((d) => d + 1);
    }, 1000);
  };

  const endCall = () => {
    setIsInCall(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  useEffect(() => {
    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, []);

  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const tabs = [
    { id: 'config', label: 'Configuration' },
    { id: 'call', label: 'Call' },
    { id: 'history', label: 'History' },
  ];

  return (
    <div className="flex h-screen w-full flex-col bg-gray-50">
      <header className="flex items-center justify-between border-b bg-white px-4 py-2">
        <div className="flex items-center gap-2">
          <Volume2 className="h-5 w-5 text-purple-600" />
          <h1 className="text-lg font-semibold text-gray-800">Voice Agent Builder</h1>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="secondary" size="sm" onClick={onSave}>
            <Save className="mr-1 h-4 w-4" />
            Save
          </Button>
          <Button size="sm" onClick={onRun}>
            <Play className="mr-1 h-4 w-4" />
            Test
          </Button>
        </div>
      </header>

      <div className="flex flex-1 overflow-hidden">
        <div className="flex-1 overflow-y-auto p-6">
          <Tabs tabs={tabs} activeTab={activeTab} onChange={setActiveTab} className="w-full" />

          {activeTab === 'config' && (
            <div className="mt-4 space-y-4">
              <div className="rounded-lg border bg-white p-4 shadow-sm">
                <h3 className="mb-4 text-sm font-semibold text-gray-700">General</h3>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="name">Agent Name</Label>
                    <Input
                      id="name"
                      value={agent.name}
                      onChange={(e) => update({ name: e.target.value })}
                      placeholder="My Voice Agent"
                    />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="prompt">System Prompt</Label>
                    <Textarea
                      id="prompt"
                      value={agent.prompt}
                      onChange={(e) => update({ prompt: e.target.value })}
                      placeholder="You are a helpful voice assistant..."
                      rows={6}
                    />
                  </div>
                </div>
              </div>

              <div className="rounded-lg border bg-white p-4 shadow-sm">
                <h3 className="mb-4 text-sm font-semibold text-gray-700">Speech Providers</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label htmlFor="sttProvider">STT Provider</Label>
                    <Select
                      id="sttProvider"
                      value={agent.sttProvider}
                      onChange={(e) => update({ sttProvider: e.target.value })}
                      options={sttProviders}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="ttsProvider">TTS Provider</Label>
                    <Select
                      id="ttsProvider"
                      value={agent.ttsProvider}
                      onChange={(e) => update({ ttsProvider: e.target.value })}
                      options={ttsProviders}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="voice">Voice</Label>
                    <Select
                      id="voice"
                      value={agent.voice}
                      onChange={(e) => update({ voice: e.target.value })}
                      options={voices}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="language">Language</Label>
                    <Select
                      id="language"
                      value={agent.language}
                      onChange={(e) => update({ language: e.target.value })}
                      options={languages}
                    />
                  </div>
                </div>
              </div>

              <div className="rounded-lg border bg-white p-4 shadow-sm">
                <h3 className="mb-4 text-sm font-semibold text-gray-700">Model Settings</h3>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="temperature">
                      Temperature: {agent.temperature.toFixed(1)}
                    </Label>
                    <Slider
                      min={0}
                      max={2}
                      step={0.1}
                      value={[agent.temperature]}
                      onValueChange={([value]) => update({ temperature: value })}
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="maxTokens">Max Tokens</Label>
                    <Input
                      id="maxTokens"
                      type="number"
                      value={agent.maxTokens}
                      onChange={(e) => update({ maxTokens: parseInt(e.target.value, 10) || 1024 })}
                    />
                  </div>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'call' && (
            <div className="mt-4">
              <div className="rounded-lg border bg-white p-6 shadow-sm">
                <div className="flex flex-col items-center justify-center space-y-4">
                  <div className="text-center">
                    <div className="text-4xl font-mono font-bold text-gray-800">
                      {formatDuration(callDuration)}
                    </div>
                    <div className="mt-1 text-sm text-gray-500">
                      {isInCall ? 'Connected' : 'Not in call'}
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    {!isInCall ? (
                      <Button size="lg" onClick={startCall}>
                        <Phone className="mr-2 h-5 w-5" />
                        Start Call
                      </Button>
                    ) : (
                      <>
                      <Button
                        size="lg"
                        variant={isRecording ? 'danger' : 'primary'}
                        onClick={() => setIsRecording(!isRecording)}
                      >
                          {isRecording ? (
                            <>
                              <MicOff className="mr-2 h-5 w-5" />
                              Stop Recording
                            </>
                          ) : (
                            <>
                              <Mic className="mr-2 h-5 w-5" />
                              Record
                            </>
                          )}
                        </Button>
                        <Button size="lg" variant="danger" onClick={endCall}>
                          <PhoneOff className="mr-2 h-5 w-5" />
                          End Call
                        </Button>
                      </>
                    )}
                  </div>

                  {isRecording && (
                    <div className="flex items-center gap-2 text-red-600">
                      <div className="h-3 w-3 animate-pulse rounded-full bg-red-600" />
                      <span className="text-sm font-medium">Recording...</span>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {activeTab === 'history' && (
            <div className="mt-4">
              <div className="rounded-lg border bg-white shadow-sm">
                <div className="border-b px-4 py-3">
                  <h3 className="text-sm font-semibold text-gray-700">Call History</h3>
                </div>
                <ScrollArea className="h-96">
                  <div className="space-y-2 p-4">
                    <div className="rounded-md border p-3">
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="text-sm font-medium text-gray-800">Call #1</div>
                          <div className="text-xs text-gray-500">2026-10-03 10:30</div>
                        </div>
                        <div className="text-sm text-gray-600">02:45</div>
                      </div>
                    </div>
                    <div className="rounded-md border p-3">
                      <div className="flex items-center justify-between">
                        <div>
                          <div className="text-sm font-medium text-gray-800">Call #2</div>
                          <div className="text-xs text-gray-500">2026-10-03 09:15</div>
                        </div>
                        <div className="text-sm text-gray-600">01:20</div>
                      </div>
                    </div>
                  </div>
                </ScrollArea>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default VoiceAgentBuilder;
