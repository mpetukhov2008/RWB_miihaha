import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-loading-indicator',
  standalone: true,
  imports: [CommonModule, MatProgressSpinnerModule],
  template: `
    <div class="loading-indicator" role="status" aria-live="polite">
      <mat-progress-spinner mode="indeterminate" diameter="48"></mat-progress-spinner>
      <p class="loading-indicator__label">{{ label }}</p>
    </div>
  `,
})
export class LoadingIndicatorComponent {
  @Input() label = 'Загрузка…';
}
