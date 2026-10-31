import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-s-c-r-004',
  standalone: true,
  imports: [MatButtonModule, MatProgressSpinnerModule],
  template: `
    <h2>Итоги завершённой сессии</h2>
    @if (state === 'success') { <div class="state">Показывается время начала/окончания, длительность, итоговая стоимость и статус оплаты</div> }

    <button mat-raised-button (click)="run('None')">На главный экран</button>
<button mat-raised-button (click)="run('None')">В историю</button>

  `,
  styles: [`.state { padding: 1rem; }`],
})
export class Scr004Component {
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
