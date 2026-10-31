import { Routes } from '@angular/router';
import { Scr001Component } from './screens/scr-001/scr-001.component';
import { Scr002Component } from './screens/scr-002/scr-002.component';
import { Scr003Component } from './screens/scr-003/scr-003.component';

export const routes: Routes = [
  { path: '', component: Scr001Component },
  { path: 'upload', component: Scr002Component },
  { path: 'status/:id', component: Scr003Component },
  { path: '**', redirectTo: '' }
];
