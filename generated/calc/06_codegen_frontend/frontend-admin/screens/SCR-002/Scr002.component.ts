import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-s-c-r-002',
  standalone: true,
  imports: [MatButtonModule, MatProgressSpinnerModule],
  template: `
    <h2>Результат суммирования</h2>
    @if (state === 'empty') { <div class="state">Результат ещё не вычислен</div> }
@if (state === 'loading') { <div class="state">Показ индикатора загрузки при ожидании ответа API</div> }
@if (state === 'error') { <div class="state">Показ сообщения об ошибке при сбое вычисления</div> }
@if (state === 'success') { <div class="state">Отображение результата суммы двух чисел</div> }

    <button mat-raised-button (click)="run('None')">Новое вычисление</button>

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
