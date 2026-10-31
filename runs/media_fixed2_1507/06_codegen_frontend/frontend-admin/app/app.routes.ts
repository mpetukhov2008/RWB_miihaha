import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { Scr001Component } from './screens/SCR-001/Scr001.component';
import { Scr002Component } from './screens/SCR-002/Scr002.component';
import { Scr003Component } from './screens/SCR-003/Scr003.component';
import { Scr004Component } from './screens/SCR-004/Scr004.component';
import { Scr005Component } from './screens/SCR-005/Scr005.component';
import { Scr006Component } from './screens/SCR-006/Scr006.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 's-c-r-001', component: Scr001Component },
  { path: 's-c-r-002', component: Scr002Component },
  { path: 's-c-r-003', component: Scr003Component },
  { path: 's-c-r-004', component: Scr004Component },
  { path: 's-c-r-005', component: Scr005Component },
  { path: 's-c-r-006', component: Scr006Component },
  { path: '**', redirectTo: '' },
];
