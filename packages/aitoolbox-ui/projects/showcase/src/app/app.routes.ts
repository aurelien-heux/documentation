import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', pathMatch: 'full', redirectTo: 'runs' },
  { path: 'runs', loadComponent: () => import('./runs.page').then((m) => m.RunsPage), title: 'Runs · AIToolbox' },
  { path: 'components', loadComponent: () => import('./components.page').then((m) => m.ComponentsPage), title: 'Components · AIToolbox' },
];
