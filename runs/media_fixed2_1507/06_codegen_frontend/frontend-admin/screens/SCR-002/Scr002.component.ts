import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-s-c-r-002',
  standalone: true,
  imports: [MatButtonModule, MatProgressSpinnerModule],
  template: `
    <h2>Загрузка исходного файла и эталонного макета</h2>
    @if (state === 'empty') { <div class="state">Два слота: «Исходный файл» (камера/галерея) и «Эталонный макет» (галерея). Прогресс-бары загрузки в S3.</div> }
@if (state === 'loading') { <div class="state">Прогресс-бары загрузки файлов, статус «Загрузка в S3…». Индикатор подтверждения загрузки.</div> }
@if (state === 'error') { <div class="state">Ошибка загрузки файла (таймаут, неверный формат, превышение размера). Кнопки «Повторить» и «Выбрать другой файл».</div> }
@if (state === 'forbidden') { <div class="state">Экран 401: «Требуется авторизация». Кнопка «Войти».</div> }
@if (state === 'success') { <div class="state">Оба файла загружены и подтверждены. Превью файлов. Кнопка «Создать заявку» активна.</div> }

    <button mat-raised-button (click)="run('getUploadUrl')">Загрузить исходный файл</button>
<button mat-raised-button (click)="run('confirmFileUpload')">Подтвердить загрузку исходного файла</button>
<button mat-raised-button (click)="run('getUploadUrl')">Загрузить эталонный макет</button>
<button mat-raised-button (click)="run('confirmFileUpload')">Подтвердить загрузку макета</button>
<button mat-raised-button (click)="run('createApplication')">Создать заявку</button>

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
