import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-s-c-r-001',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatProgressSpinnerModule],
    template: `
    <h2>Выбор типа обработки</h2>
    @if (state === 'empty') { <div class="state">Экран выбора типа: две карточки — «Фотоотчет» и «Видеопоток». Подсказки о поддерживаемых форматах (JPEG/PNG для фото, MP4 150–300 с для видео).</div> }
@if (state === 'loading') { <div class="state">Скелетон карточек при инициализации приложения.</div> }
@if (state === 'error') { <div class="state">Сообщение об ошибке инициализации с кнопкой «Повторить».</div> }
@if (state === 'forbidden') { <div class="state">Экран 401: «Требуется авторизация». Кнопка «Войти».</div> }
@if (state === 'success') { <div class="state">Карточки активны, пользователь может выбрать тип.</div> }

    <button mat-raised-button (click)="run('None')">Выбрать фотоотчет</button>
<button mat-raised-button (click)="run('None')">Выбрать видеопоток</button>

  `,
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
