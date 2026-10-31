import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterLink } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

import { CalculationResponse, ProblemDetails } from '../../models/calculation.model';
import { CalculationService } from '../../services/calculation.service';
import { ResultDisplayComponent } from '../../components/result-display/result-display.component';
import { ErrorMessageComponent } from '../../components/error-message/error-message.component';
import { LoadingIndicatorComponent } from '../../components/loading-indicator/loading-indicator.component';

type ScreenState = 'empty' | 'loading' | 'error' | 'success';

@Component({
  selector: 'app-calculation-result',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    ResultDisplayComponent,
    ErrorMessageComponent,
    LoadingIndicatorComponent,
  ],
  template: `
    <div class="calculation-result">
      <mat-card class="calculation-result__card">
        <mat-card-header>
          <mat-icon mat-card-avatar>sum</mat-icon>
          <mat-card-title>Результат суммирования</mat-card-title>
        </mat-card-header>

        <mat-card-content>
          <!-- Состояние: empty -->
          <div *ngIf="state === 'empty'" class="calculation-result__empty">
            <mat-icon class="calculation-result__empty-icon">hourglass_empty</mat-icon>
            <p>Результат ещё не вычислен.</p>
            <p>Вернитесь к форме и выполните вычисление.</p>
          </div>

          <!-- Состояние: loading -->
          <app-loading-indicator
            *ngIf="state === 'loading'"
            label="Ожидание ответа сервера…"
          />

          <!-- Состояние: error -->
          <app-error-message
            *ngIf="state === 'error'"
            [message]="errorMessage"
            title="Ошибка вычисления"
          />

          <!-- Состояние: success -->
          <app-result-display
            *ngIf="state === 'success' && calculation"
            [result]="calculation.result"
            [firstNumber]="calculation.first_number"
            [secondNumber]="calculation.second_number"
            [createdAt]="calculation.created_at"
          />
        </mat-card-content>

        <mat-card-actions class="calculation-result__actions">
          <button mat-flat-button color="primary" (click)="onNewCalculation()">
            <mat-icon>refresh</mat-icon>
            Новое вычисление
          </button>
        </mat-card-actions>
      </mat-card>
    </div>
  `,
})
export class CalculationResultComponent implements OnInit {
  private readonly router = inject(Router);
  private readonly calculationService = inject(CalculationService);

  state: ScreenState = 'empty';
  errorMessage = '';
  calculation: CalculationResponse | null = null;

  ngOnInit(): void {
    const navigationState = this.router.getCurrentNavigation()?.extras.state as
      | { calculation?: CalculationResponse }
      | undefined;

    if (navigationState?.calculation) {
      this.calculation = navigationState.calculation;
      this.state = 'success';
      return;
    }

    // Если пользователь открыл страницу напрямую — показываем empty
    this.state = 'empty';
  }

  onNewCalculation(): void {
    this.router.navigate(['/form']);
  }
}
