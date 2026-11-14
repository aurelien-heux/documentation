import { InjectionToken } from '@angular/core';

/** What the header needs from the shell around it (avoids a circular import between the two components). */
export interface AitShellApi {
  openDrawer(): void;
  closeDrawer(): void;
}

export const AIT_SHELL = new InjectionToken<AitShellApi>('AIT_SHELL');
