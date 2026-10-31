import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-s-c-r-002',
  standalone: true,
  imports: [MatButtonModule, MatProgressSpinnerModule],
  template: `
    <h2>Активная сессия</h2>
    @if (state === 'loading') { <div class="state">Загрузка сессии...</div> }
@if (state === 'error') { <div class="state">Ошибка загрузки</div> }
@if (state === 'success') { <div class="state">Сессия активна</div> }

    <button mat-raised-button (click)="run('completeSession')">Завершить</button>

  `,
  styles: [`.state { padding: 1rem; }`],
})
export class Scr002Component {
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
