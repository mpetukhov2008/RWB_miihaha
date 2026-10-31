import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-s-c-r-001',
  standalone: true,
  imports: [MatButtonModule, MatProgressSpinnerModule],
  template: `
    <h2>Вход в систему</h2>
    @if (state === 'loading') { <div class="state">Показывается спиннер при отправке формы</div> }
@if (state === 'error') { <div class="state">Показывается сообщение об ошибке при неверных данных (401/422)</div> }
@if (state === 'success') { <div class="state">Пользователь перенаправляется на главный экран по роли</div> }

    <button mat-raised-button (click)="run('login')">Войти</button>

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
