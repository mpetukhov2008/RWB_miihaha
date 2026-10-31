import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-s-c-r-003',
  standalone: true,
  imports: [MatButtonModule, MatProgressSpinnerModule],
  template: `
    <h2>Активная сессия</h2>
    @if (state === 'loading') { <div class="state">Показывается спиннер при загрузке данных активной сессии</div> }
@if (state === 'error') { <div class="state">Показывается сообщение об ошибке при недоступности сессии</div> }
@if (state === 'success') { <div class="state">Показывается таймер, текущая стоимость, зона и кнопка «Завершить сессию»</div> }

    <button mat-raised-button (click)="run('getActiveSession')">Загрузить активную сессию</button>
<button mat-raised-button (click)="run('endSession')">Завершить сессию</button>

  `,
  styles: [`.state { padding: 1rem; }`],
})
export class Scr003Component {
  state = 'loading';
  constructor(private api: ApiService) {
    setTimeout(() => (this.state = 'success'), 300);
  }
  run(operationId: string) {
    this.api.call(operationId).subscribe({
      next: () => (this.state = 'success'),
      error: () => (this.state = 'error'),
    });
  }
}
