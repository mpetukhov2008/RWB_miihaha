import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-s-c-r-006',
  standalone: true,
  imports: [MatButtonModule, MatProgressSpinnerModule],
  template: `
    <h2>Уведомления</h2>
    @if (state === 'empty') { <div class="state">Показывается сообщение «Уведомлений нет»</div> }
@if (state === 'loading') { <div class="state">Показывается спиннер при загрузке списка</div> }
@if (state === 'error') { <div class="state">Показывается сообщение об ошибке загрузки</div> }
@if (state === 'success') { <div class="state">Показывается список уведомлений с типом, текстом и временем</div> }

    <button mat-raised-button (click)="run('listNotifications')">Загрузить уведомления</button>
<button mat-raised-button (click)="run('markNotificationRead')">Отметить прочитанным</button>

  `,
  styles: [`.state { padding: 1rem; }`],
})
export class Scr006Component {
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
