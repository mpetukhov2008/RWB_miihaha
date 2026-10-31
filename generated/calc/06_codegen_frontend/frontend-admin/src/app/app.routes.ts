import { Routes } from '@angular/router';

import { CalculationFormComponent } from './screens/calculation-form/calculation-form.component';
import { CalculationResultComponent } from './screens/calculation-result/calculation-result.component';

export const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'form',
  },
  {
    path: 'form',
    component: CalculationFormComponent,
    title: 'Форма ввода чисел',
  },
  {
    path: 'result',
    component: CalculationResultComponent,
    title: 'Результат суммирования',
  },
  {
    path: '**',
    redirectTo: 'form',
  },
];
