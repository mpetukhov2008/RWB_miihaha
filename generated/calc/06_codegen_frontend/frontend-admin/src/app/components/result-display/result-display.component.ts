import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';

@Component({
  selector: 'app-result-display',
  standalone: true,
  imports: [CommonModule, MatCardModule, MatIconModule],
  template: `
    <mat-card class="result-display" *ngIf="result !== null">
      <mat-card-header>
        <mat-icon mat-card-avatar class="result-display__icon">calculate</mat-icon>
        <mat-card-title>Результат вычисления</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <p class="result-display__formula">
          {{ firstNumber }} + {{ secondNumber }}
        </p>
        <p class="result-display__value">= {{ result }}</p>
        <p class="result-display__meta" *ngIf="createdAt">
          Вычислено: {{ createdAt | date: 'medium' }}
        </p>
      </mat-card-content>
    </mat-card>
  `,
})
export class ResultDisplayComponent {
  @Input() result: number | null = null;
  @Input() firstNumber: number | null = null;
  @Input() secondNumber: number | null = null;
  @Input() createdAt: string | null = null;
}
