import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: 'location', pathMatch: 'full' },
  {
    path: 'location',
    loadComponent: () =>
      import('./screens/location/location.component').then((m) => m.LocationComponent),
  },
  {
    path: 'session',
    loadComponent: () =>
      import('./screens/session/session.component').then((m) => m.SessionComponent),
  },
  {
    path: 'payment',
    loadComponent: () =>
      import('./screens/payment/payment.component').then((m) => m.PaymentComponent),
  },
  { path: '**', redirectTo: 'location' },
];
