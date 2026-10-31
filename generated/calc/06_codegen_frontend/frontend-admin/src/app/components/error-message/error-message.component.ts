import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-error-message',
  standalone: true,
  imports: [CommonModule, MatIconModule],
  template: `
    <div class="error-message" role="alert" *ngIf="message">
      <mat-icon class="error-message__icon">error_outline</mat-icon>
      <div class="error-message__body">
        <p class="error-message__title">{{ title }}</p>
        <p class="error-message__text">{{ message }}</p>
      </div>
    </div>
  `,
})
export class ErrorMessageComponent {
  @Input() message = '';
  @Input() title = 'Ошибка';
}
