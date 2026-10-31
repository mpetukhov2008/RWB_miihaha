import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-s-c-r-007',
  standalone: true,
  imports: [MatButtonModule, MatProgressSpinnerModule],
  template: `
    <h2>Главный экран администратора</h2>
    @if (state === 'forbidden') { <div class="state">Показывается сообщение «Доступ запрещён» для не-админа</div> }
@if (state === 'success') { <div class="state">Показывается навигация: Зоны, Сессии</div> }

    <button mat-raised-button (click)="run('None')">К зонам</button>
<button mat-raised-button (click)="run('None')">К сессиям</button>

  `,
  styles: [`.state { padding: 1rem; }`],
})
export class Scr007Component {
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
