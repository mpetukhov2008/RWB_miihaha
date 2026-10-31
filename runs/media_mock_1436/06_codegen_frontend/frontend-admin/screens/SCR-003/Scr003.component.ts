import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-s-c-r-003',
  standalone: true,
  imports: [MatButtonModule, MatProgressSpinnerModule],
  template: `
    <h2>История</h2>
    @if (state === 'empty') { <div class="state">Сессий пока нет</div> }
@if (state === 'loading') { <div class="state">Загрузка истории...</div> }
@if (state === 'error') { <div class="state">Ошибка загрузки</div> }
@if (state === 'success') { <div class="state">История загружена</div> }

    <button mat-raised-button (click)="run('listSessions')">Обновить</button>

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
