import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-s-c-r-009',
  standalone: true,
  imports: [MatButtonModule, MatProgressSpinnerModule],
  template: `
    <h2>Сессии (админ)</h2>
    @if (state === 'empty') { <div class="state">Показывается сообщение «Сессий нет»</div> }
@if (state === 'loading') { <div class="state">Показывается спиннер при загрузке списка</div> }
@if (state === 'error') { <div class="state">Показывается сообщение об ошибке</div> }
@if (state === 'forbidden') { <div class="state">Показывается сообщение «Доступ запрещён»</div> }
@if (state === 'success') { <div class="state">Показывается список сессий с фильтрами по зоне и статусу</div> }

    <button mat-raised-button (click)="run('adminListSessions')">Загрузить сессии</button>

  `,
  styles: [`.state { padding: 1rem; }`],
})
export class Scr009Component {
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
