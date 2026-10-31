import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-s-c-r-005',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatProgressSpinnerModule],
    template: `
    <h2>Результаты обработки видеопотока</h2>
    @if (state === 'empty') { <div class="state">Сегменты ещё не обнаружены. Ссылка на SCR-003.</div> }
@if (state === 'loading') { <div class="state">Загрузка отчёта о временных метках.</div> }
@if (state === 'error') { <div class="state">Ошибка получения отчёта. Кнопка «Повторить».</div> }
@if (state === 'forbidden') { <div class="state">Экран 401: «Требуется авторизация». Кнопка «Войти».</div> }
@if (state === 'success') { <div class="state">Таймлайн исходного видео (150–300 с) с выделенными сегментами. Список сегментов: start_time, end_time, confidence, result_file_id. Кнопки скачивания вырезанных роликов (MP4 H.264).</div> }

    <button mat-raised-button (click)="run('getVideoSegments')">Получить отчёт о сегментах</button>
<button mat-raised-button (click)="run('getDownloadUrl')">Скачать вырезанный ролик</button>
<button mat-raised-button (click)="run('triggerProcessing')">Запустить повторную обработку</button>
<button mat-raised-button (click)="run('None')">Создать новую заявку</button>

  `,
  })
export class Scr005Component {
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
