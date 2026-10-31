import { Routes } from '@angular/router';
import { Scr001Component } from './screens/SCR-001/Scr001.component';
import { Scr002Component } from './screens/SCR-002/Scr002.component';
import { Scr003Component } from './screens/SCR-003/Scr003.component';
import { Scr004Component } from './screens/SCR-004/Scr004.component';
import { Scr005Component } from './screens/SCR-005/Scr005.component';
import { Scr006Component } from './screens/SCR-006/Scr006.component';
import { Scr007Component } from './screens/SCR-007/Scr007.component';
import { Scr008Component } from './screens/SCR-008/Scr008.component';
import { Scr009Component } from './screens/SCR-009/Scr009.component';

export const routes: Routes = [
  { path: '', component: Scr001Component },
  { path: 'scr002', component: Scr002Component },
  { path: 'scr003', component: Scr003Component },
  { path: 'scr004', component: Scr004Component },
  { path: 'scr005', component: Scr005Component },
  { path: 'scr006', component: Scr006Component },
  { path: 'scr007', component: Scr007Component },
  { path: 'scr008', component: Scr008Component },
  { path: 'scr009', component: Scr009Component },
  { path: '**', redirectTo: '' }
];
