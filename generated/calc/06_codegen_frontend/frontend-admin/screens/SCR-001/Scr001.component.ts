import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-s-c-r-001',
  standalone: true,
  imports: [MatButtonModule, MatProgressSpinnerModule],
  template: `
    <h2>Форма ввода чисел</h2>
    @if (state === 'empty') { <div class="state">Форма с пустыми полями для ввода первого и второго числа</div> }
@if (state === 'loading') { <div class="state">Показ индикатора загрузки при отправке данных</div> }
@if (state === 'error') { <div class="state">Показ сообщения об ошибке при некорректном вводе или ошибке API</div> }
@if (state === 'success') { <div class="state">Форма с валидными значениями, готовая к отправке</div> }

    <button mat-raised-button (click)="run('createCalculation')">Вычислить сумму</button>
<button mat-raised-button (click)="run('None')">Очистить форму</button>

  `,
  styles: [`.state { padding: 1rem; }`],
})
export class Scr001Component {
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
