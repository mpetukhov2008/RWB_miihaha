import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-submit-button',
  standalone: true,
  imports: [CommonModule, MatButtonModule],
  template: `
    <button
      mat-flat-button
      color="primary"
      type="submit"
      [disabled]="disabled || loading"
      (click)="onClick.emit()"
    >
      <span *ngIf="!loading">{{ label }}</span>
      <span *ngIf="loading" class="submit-button__loading">Отправка…</span>
    </button>
  `,
})
export class SubmitButtonComponent {
  @Input() label = 'Отправить';
  @Input() disabled = false;
  @Input() loading = false;
  @Output() onClick = new EventEmitter<void>();
}
