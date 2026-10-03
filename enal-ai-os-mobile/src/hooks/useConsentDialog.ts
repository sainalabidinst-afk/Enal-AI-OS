import { useState, useCallback } from 'react';

export function useConsentDialog() {
  const [visible, setVisible] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [onApprove, setOnApprove] = useState<() => void>(() => {});
  const [onDeny, setOnDeny] = useState<() => void>(() => {});

  const open = useCallback((params: { title: string; description: string; onApprove: () => void; onDeny: () => void }) => {
    setTitle(params.title);
    setDescription(params.description);
    setOnApprove(() => params.onApprove);
    setOnDeny(() => params.onDeny);
    setVisible(true);
  }, []);

  const close = useCallback(() => {
    setVisible(false);
  }, []);

  return {
    visible,
    title,
    description,
    open,
    close,
    onApprove,
    onDeny,
  };
}
