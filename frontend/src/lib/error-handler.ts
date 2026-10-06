export function handleApiError(error: unknown): string {
  if (error instanceof Error) {
    return error.message;
  }
  if (typeof error === 'string') {
    return error;
  }
  return 'An unexpected error occurred';
}

export function formatApiError(error: unknown) {
  const message = handleApiError(error);
  return {
    title: 'Error',
    message,
    details: error,
  };
}
