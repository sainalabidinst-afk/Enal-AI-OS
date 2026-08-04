export interface EulaState {
  accepted_eula: boolean;
  accepted_version: string | null;
  accepted_at: string | null;
}

export const EULA_CURRENT_VERSION = "1.0.0";
