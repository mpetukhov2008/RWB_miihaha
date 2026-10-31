import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-s-c-r-006',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatProgressSpinnerModule],
    template: `
    <h2>Скачивание итогового файла</h2>
    @if (state === 'empty') { <div class="state">Файл не выбран.</div> }
@if (state === 'loading') { <div class="state">Получение presigned URL и загрузка файла.</div> }
@if (state === 'error') { <div class="state">Ошибка скачивания (ссылка истекла, файл не найден). Кнопка «Получить новую ссылку».</div> }
@if (state === 'forbidden') { <div class="state">Экран 401: «Требуется авторизация». Кнопка «Войти».</div> }
@if (state === 'success') { <div class="state">Файл скачан. Кнопки «Открыть» и «Вернуться к результатам».</div> }

    <button mat-raised-button (click)="run('getDownloadUrl')">Получить ссылку для скачивания</button>
<button mat-raised-button (click)="run('None')">Вернуться к результатам фото</button>
<button mat-raised-button (click)="run('None')">Вернуться к результатам видео</button>

  `,
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
