import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-s-c-r-004',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatProgressSpinnerModule],
    template: `
    <h2>Результаты обработки фотоотчета</h2>
    @if (state === 'empty') { <div class="state">Результаты ещё не готовы. Ссылка на SCR-003.</div> }
@if (state === 'loading') { <div class="state">Загрузка данных заявки и результатов.</div> }
@if (state === 'error') { <div class="state">Ошибка получения результатов. Кнопка «Повторить».</div> }
@if (state === 'forbidden') { <div class="state">Экран 401: «Требуется авторизация». Кнопка «Войти».</div> }
@if (state === 'success') { <div class="state">Карточка результата: процент схожести, статус верификации («Соответствует макету» / «Не соответствует» / «Низкое качество»). Превью исходного фото и эталонного макета. Список result_file_ids с кнопками скачивания.</div> }

    <button mat-raised-button (click)="run('getApplication')">Получить результаты заявки</button>
<button mat-raised-button (click)="run('getDownloadUrl')">Скачать итоговый файл</button>
<button mat-raised-button (click)="run('triggerProcessing')">Запустить повторную обработку</button>
<button mat-raised-button (click)="run('None')">Создать новую заявку</button>

  `,
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
