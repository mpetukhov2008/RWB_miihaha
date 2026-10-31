import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { Scr001Component } from './screens/SCR-001/Scr001.component';
import { Scr002Component } from './screens/SCR-002/Scr002.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 's-c-r-001', component: Scr001Component },
  { path: 's-c-r-002', component: Scr002Component },
  { path: '**', redirectTo: '' },
];
