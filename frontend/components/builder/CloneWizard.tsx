'use client';

import React, { useEffect, useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select } from '@/components/ui/select';
import { Dialog } from '@/components/ui/dialog';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Checkbox } from '@/components/ui/checkbox';
import { Progress } from '@/components/ui/progress';
import {
  X,
  ChevronRight,
  ChevronLeft,
  Check,
  AlertCircle,
} from 'lucide-react';

interface CloneWizardProps {
  isOpen: boolean;
  onClose: () => void;
  template: {
    id: string;
    name: string;
    description: string;
    dependencies: string[];
    kind?: string;
  };
  onComplete: () => void;
}

const CloneWizard: React.FC<CloneWizardProps> = ({
  isOpen,
  onClose,
  template,
  onComplete,
}) => {
  const [step, setStep] = useState(1);
  const [projectName, setProjectName] = useState(template.name);
  const [selectedProject, setSelectedProject] = useState('');
  const [resolvedDeps, setResolvedDeps] = useState<string[]>([]);
  const [missingDeps, setMissingDeps] = useState<string[]>([]);
  const [isCloning, setIsCloning] = useState(false);
  const [cloneComplete, setCloneComplete] = useState(false);
  const [dependencyError, setDependencyError] = useState<string | null>(null);

  const totalSteps = 3;

  useEffect(() => {
    if (step === 2 && !isCloning && resolvedDeps.length === 0 && missingDeps.length === 0) {
      let cancelled = false;
      const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const kind = template.kind || 'agent';

      async function resolveDeps() {
        setIsCloning(true);
        setDependencyError(null);
        try {
          const response = await fetch(
            `${API_BASE}/api/v1/blueprints/${kind}/${template.id}/dependencies`
          );
          if (!response.ok) {
            throw new Error(`Dependency resolution failed: ${response.status}`);
          }
          const data = await response.json();
          if (cancelled) return;
          setResolvedDeps(data.resolved || []);
          setMissingDeps(data.missing || []);
        } catch (err) {
          if (!cancelled) {
            setDependencyError(err instanceof Error ? err.message : 'Unknown error');
          }
        } finally {
          if (!cancelled) {
            setIsCloning(false);
          }
        }
      }

      resolveDeps();
      return () => {
        cancelled = true;
      };
    }
  }, [step, template.id, template.kind, isCloning, resolvedDeps.length, missingDeps.length]);

  const handleNext = async () => {
    if (step < totalSteps) {
      setStep(step + 1);
    } else {
      onComplete();
    }
  };

  const handleBack = () => {
    if (step > 1) setStep(step - 1);
  };

  const handleClose = () => {
    setStep(1);
    setCloneComplete(false);
    setResolvedDeps([]);
    setMissingDeps([]);
    setDependencyError(null);
    onClose();
  };

  return (
      <Dialog open={isOpen} onClose={handleClose}>
      <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
        <div className="w-full max-w-lg rounded-lg bg-white shadow-xl">
          <div className="flex items-center justify-between border-b px-6 py-4">
            <div>
              <h2 className="text-lg font-semibold text-gray-900">Clone Template</h2>
              <p className="text-sm text-gray-500">{template.name}</p>
            </div>
            <Button variant="ghost" size="sm" onClick={handleClose}>
              <X className="h-4 w-4" />
            </Button>
          </div>

          <div className="px-6 py-4">
            <div className="mb-6 flex items-center justify-between">
              {Array.from({ length: totalSteps }).map((_, i) => (
                <div key={i} className="flex items-center">
                  <div
                    className={`flex h-8 w-8 items-center justify-center rounded-full text-sm font-medium ${
                      i + 1 <= step
                        ? 'bg-blue-600 text-white'
                        : 'bg-gray-200 text-gray-600'
                    }`}
                  >
                    {i + 1 <= step ? <Check className="h-4 w-4" /> : i + 1}
                  </div>
                  {i < totalSteps - 1 && (
                    <div
                      className={`mx-2 h-0.5 w-12 ${
                        i + 1 < step ? 'bg-blue-600' : 'bg-gray-200'
                      }`}
                    />
                  )}
                </div>
              ))}
            </div>

            <ScrollArea className="h-64">
              {step === 1 && (
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="projectName">Project Name</Label>
                    <Input
                      id="projectName"
                      value={projectName}
                      onChange={(e) => setProjectName(e.target.value)}
                      placeholder="My cloned project"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label htmlFor="project">Target Project</Label>
                    <Select
                      id="project"
                      value={selectedProject}
                      onChange={(e) => setSelectedProject(e.target.value)}
                      options={[
                        { value: 'default', label: 'Default Project' },
                        { value: 'project-1', label: 'Project 1' },
                      ]}
                    />
                  </div>
                </div>
              )}

              {step === 2 && (
                <div className="space-y-4">
                  <h3 className="text-sm font-medium text-gray-700">Dependencies</h3>
                  {dependencyError ? (
                    <div className="rounded-md border border-red-200 bg-red-50 p-3">
                      <p className="text-sm text-red-700">{dependencyError}</p>
                      <Button
                        variant="secondary"
                        size="sm"
                        className="mt-2"
                        onClick={() => {
                          setDependencyError(null);
                          setResolvedDeps([]);
                          setMissingDeps([]);
                        }}
                      >
                        Retry
                      </Button>
                    </div>
                  ) : isCloning ? (
                    <div className="space-y-2">
                      <p className="text-sm text-gray-500">Resolving dependencies...</p>
                      <Progress value={66} />
                    </div>
                  ) : (
                    <div className="space-y-2">
                      {resolvedDeps.length === 0 && missingDeps.length === 0 ? (
                        <p className="text-sm text-gray-500">No dependencies to resolve.</p>
                      ) : (
                        <>
                          {resolvedDeps.map((dep) => (
                            <div key={dep} className="flex items-center gap-2">
                              <Checkbox id={`dep-${dep}`} label={dep} checked readOnly />
                            </div>
                          ))}
                          {missingDeps.map((dep) => (
                            <div key={dep} className="flex items-center gap-2 text-sm text-red-600">
                              <AlertCircle className="h-4 w-4" />
                              <span>Missing: {dep}</span>
                            </div>
                          ))}
                        </>
                      )}
                    </div>
                  )}
                </div>
              )}

              {step === 3 && (
                <div className="space-y-4">
                  {cloneComplete ? (
                    <div className="rounded-md border border-green-200 bg-green-50 p-4">
                      <div className="flex items-center gap-2 text-green-800">
                        <Check className="h-5 w-5" />
                        <span className="font-medium">Clone Complete</span>
                      </div>
                      <p className="mt-2 text-sm text-green-700">
                        Your template has been cloned successfully to project "{projectName}".
                      </p>
                    </div>
                  ) : (
                    <div className="rounded-md border border-blue-200 bg-blue-50 p-4">
                      <div className="flex items-center gap-2 text-blue-800">
                        <AlertCircle className="h-5 w-5" />
                        <span className="font-medium">Ready to Clone</span>
                      </div>
                      <p className="mt-2 text-sm text-blue-700">
                        Click "Next" to clone "{template.name}" to your project.
                      </p>
                    </div>
                  )}
                </div>
              )}
            </ScrollArea>
          </div>

          <div className="flex items-center justify-between border-t px-6 py-4">
            <Button
              variant="ghost"
              onClick={handleBack}
              disabled={step === 1}
            >
              <ChevronLeft className="mr-1 h-4 w-4" />
              Back
            </Button>
            <Button onClick={handleNext} disabled={step === 2 && isCloning}>
              {step === totalSteps ? (
                cloneComplete ? 'Done' : 'Complete'
              ) : (
                <>
                  Next
                  <ChevronRight className="ml-1 h-4 w-4" />
                </>
              )}
            </Button>
          </div>
        </div>
      </div>
    </Dialog>
  );
};

export default CloneWizard;
