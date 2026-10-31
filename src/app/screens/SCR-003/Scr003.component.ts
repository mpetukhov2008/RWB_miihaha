import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-s-c-r-003',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatProgressSpinnerModule],
    template: `
    <h2>Статус обработки заявки</h2>
    @if (state === 'empty') { <div class="state">Не должно возникать; если заявка не найдена — редирект на SCR-001.</div> }
@if (state === 'loading') { <div class="state">Анимация обработки: «Анализ медиафайла…», «Поиск рекламного блока…», «Нарезка видео…». Таймер ожидаемого времени (до 20 мин для видео).</div> }
@if (state === 'error') { <div class="state">Ошибка обработки: «Не удалось обработать файл». Кнопки «Повторить обработку» и «Вернуться к загрузке».</div> }
@if (state === 'forbidden') { <div class="state">Экран 401: «Требуется авторизация». Кнопка «Войти».</div> }
@if (state === 'success') { <div class="state">Обработка завершена. Статус «Выполнено». Кнопка «Посмотреть результаты».</div> }

    <button mat-raised-button (click)="run('getApplication')">Получить статус заявки</button>
<button mat-raised-button (click)="run('triggerProcessing')">Запустить принудительную обработку</button>
<button mat-raised-button (click)="run('None')">Перейти к результатам</button>

  `,
  })
export class Scr003Component {
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
