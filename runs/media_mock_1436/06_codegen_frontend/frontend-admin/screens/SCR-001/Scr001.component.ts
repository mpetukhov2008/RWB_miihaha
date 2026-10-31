import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-s-c-r-001',
  standalone: true,
  imports: [MatButtonModule, MatProgressSpinnerModule],
  template: `
    <h2>Карта зоны</h2>
    @if (state === 'empty') { <div class="state">Нет данных о зоне</div> }
@if (state === 'loading') { <div class="state">Определяем зону...</div> }
@if (state === 'error') { <div class="state">Ошибка геолокации</div> }
@if (state === 'success') { <div class="state">Зона определена</div> }

    <button mat-raised-button (click)="run('startSession')">Начать сессию</button>

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
