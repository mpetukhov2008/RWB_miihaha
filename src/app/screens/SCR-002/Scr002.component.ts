import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-s-c-r-002',
  standalone: true,
  imports: [MatButtonModule, MatProgressSpinnerModule],
  template: `
    <h2>Главный экран водителя (определение зоны)</h2>
    @if (state === 'empty') { <div class="state">Показывается сообщение «Вне платной зоны»</div> }
@if (state === 'loading') { <div class="state">Показывается спиннер при определении геолокации</div> }
@if (state === 'error') { <div class="state">Показывается сообщение об ошибке геолокации или API</div> }
@if (state === 'success') { <div class="state">Показывается название зоны, тариф и кнопка «Начать сессию»</div> }

    <button mat-raised-button (click)="run('getNearbyZone')">Определить зону</button>
<button mat-raised-button (click)="run('startSession')">Начать сессию</button>
<button mat-raised-button (click)="run('None')">История</button>
<button mat-raised-button (click)="run('None')">Уведомления</button>

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
