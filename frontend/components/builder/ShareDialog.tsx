'use client';

import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select } from '@/components/ui/select';
import { Dialog } from '@/components/ui/dialog';
import { Checkbox } from '@/components/ui/checkbox';
import { ScrollArea } from '@/components/ui/scroll-area';
import {
  X,
  Share2,
  Globe,
  Lock,
  Users,
  Copy,
  Check,
} from 'lucide-react';

interface ShareDialogProps {
  isOpen: boolean;
  onClose: () => void;
  agent: {
    id: string;
    name: string;
  };
  onShare?: (config: ShareConfig) => void;
}

interface ShareConfig {
  visibility: 'private' | 'internal' | 'public';
  allowedRoles: string[];
  allowClone: boolean;
}

const ShareDialog: React.FC<ShareDialogProps> = ({
  isOpen,
  onClose,
  agent,
  onShare,
}) => {
  const [visibility, setVisibility] = useState<ShareConfig['visibility']>('internal');
  const [allowedRoles, setAllowedRoles] = useState<string[]>([]);
  const [allowClone, setAllowClone] = useState(true);
  const [shareLink, setShareLink] = useState('');
  const [copied, setCopied] = useState(false);

  const handleShare = () => {
    const config: ShareConfig = { visibility, allowedRoles, allowClone };
    const link = `https://enal-ai-os.com/marketplace/${agent.id}`;
    setShareLink(link);
    onShare?.(config);
  };

  const copyToClipboard = () => {
    navigator.clipboard.writeText(shareLink);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const roles = [
    { value: 'admin', label: 'Admin' },
    { value: 'builder', label: 'Builder' },
    { value: 'viewer', label: 'Viewer' },
  ];

  return (
      <Dialog open={isOpen} onClose={onClose}>
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
        <div className="w-full max-w-md rounded-lg bg-white shadow-xl">
          <div className="flex items-center justify-between border-b px-6 py-4">
            <div className="flex items-center gap-2">
              <Share2 className="h-5 w-5 text-blue-600" />
              <h2 className="text-lg font-semibold text-gray-900">Share Agent</h2>
            </div>
            <Button variant="ghost" size="sm" onClick={onClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>

          <ScrollArea className="max-h-[70vh] px-6 py-4">
            <div className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="visibility">Visibility</Label>
                <Select
                  id="visibility"
                  value={visibility}
                  onChange={(e) => setVisibility(e.target.value as ShareConfig['visibility'])}
                  options={[
                    { value: 'private', label: 'Private (only me)' },
                    { value: 'internal', label: 'Internal (team)' },
                    { value: 'public', label: 'Public (marketplace)' },
                  ]}
                />
              </div>

              <div className="space-y-2">
                <Label>Allowed Roles</Label>
                <div className="space-y-2">
                  {roles.map((role) => (
                    <div key={role.value} className="flex items-center gap-2">
                      <Checkbox
                        id={`role-${role.value}`}
                        label={role.label}
                        checked={allowedRoles.includes(role.value)}
                        onChange={(e) => {
                          if (e.target.checked) {
                            setAllowedRoles([...allowedRoles, role.value]);
                          } else {
                            setAllowedRoles(allowedRoles.filter((r) => r !== role.value));
                          }
                        }}
                      />
                    </div>
                  ))}
                </div>
              </div>

              <div className="flex items-center gap-2">
                <Checkbox
                  id="allowClone"
                  label="Allow cloning"
                  checked={allowClone}
                  onChange={(e) => setAllowClone(e.target.checked)}
                />
              </div>

              {shareLink && (
                <div className="space-y-2">
                  <Label>Share Link</Label>
                  <div className="flex items-center gap-2">
                    <Input value={shareLink} readOnly />
                    <Button variant="secondary" size="sm" onClick={copyToClipboard}>
                      {copied ? (
                        <Check className="h-4 w-4" />
                      ) : (
                        <Copy className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>

          <div className="flex items-center justify-end gap-2 border-t px-6 py-4">
            <Button variant="ghost" onClick={onClose}>
              Cancel
            </Button>
            <Button onClick={handleShare}>
              <Share2 className="mr-2 h-4 w-4" />
              Share
            </Button>
          </div>
        </div>
      </div>
    </Dialog>
  );
};

export default ShareDialog;
