import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';

import { CalculationService } from '../../services/calculation.service';
import { CalculationResponse, ProblemDetails } from '../../models/calculation.model';
import { NumberInputComponent } from '../../components/number-input/number-input.component';
import { SubmitButtonComponent } from '../../components/submit-button/submit-button.component';
import { ErrorMessageComponent } from '../../components/error-message/error-message.component';
import { LoadingIndicatorComponent } from '../../components/loading-indicator/loading-indicator.component';

type ScreenState = 'empty' | 'loading' | 'error' | 'success';

@Component({
  selector: 'app-calculation-form',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatButtonModule,
    MatIconModule,
    NumberInputComponent,
    SubmitButtonComponent,
    ErrorMessageComponent,
    LoadingIndicatorComponent,
  ],
  template: `
    <div class="calculation-form">
      <mat-card class="calculation-form__card">
        <mat-card-header>
          <mat-icon mat-card-avatar>add</mat-icon>
          <mat-card-title>Форма ввода чисел</mat-card-title>
          <mat-card-subtitle>Введите два числа для вычисления суммы</mat-card-subtitle>
        </mat-card-header>

        <mat-card-content>
          <!-- Состояние: loading -->
          <app-loading-indicator
            *ngIf="state === 'loading'"
            label="Выполняется вычисление…"
          />

          <!-- Состояние: error -->
          <app-error-message
            *ngIf="state === 'error'"
            [message]="errorMessage"
            title="Ошибка вычисления"
          />

          <!-- Состояния: empty / success -->
          <form
            *ngIf="state === 'empty' || state === 'success'"
            [formGroup]="form"
            (ngSubmit)="onSubmit()"
            class="calculation-form__form"
          >
            <app-number-input
              formControlName="firstNumber"
              label="Первое число"
              placeholder="Например: 42"
            />
            <app-number-input
              formControlName="secondNumber"
              label="Второе число"
              placeholder="Например: 17"
            />

            <div class="calculation-form__actions">
              <app-submit-button
                label="Вычислить сумму"
                [loading]="state === 'loading'"
                [disabled]="form.invalid"
              />
              <button
                mat-stroked-button
                color="basic"
                type="button"
                (click)="onClear()"
              >
                Очистить форму
              </button>
            </div>
          </form>
        </mat-card-content>
      </mat-card>
    </div>
  `,
})
export class CalculationFormComponent implements OnInit {
  private readonly fb = inject(FormBuilder);
  private readonly router = inject(Router);
  private readonly calculationService = inject(CalculationService);

  state: ScreenState = 'empty';
  errorMessage = '';

  form = this.fb.nonNullable.group({
    firstNumber: [0, [Validators.required, Validators.min(-1e15), Validators.max(1e15)]],
    secondNumber: [0, [Validators.required, Validators.min(-1e15), Validators.max(1e15)]],
  });

  ngOnInit(): void {
    this.form.valueChanges.subscribe(() => {
      if (this.state === 'error' && this.form.valid) {
        this.state = 'success';
        this.errorMessage = '';
      }
    });
  }

  onSubmit(): void {
    if (this.form.invalid) {
      this.state = 'error';
      this.errorMessage = 'Пожалуйста, заполните все поля корректными числами.';
      return;
    }

    this.state = 'loading';
    this.errorMessage = '';

    const payload = {
      first_number: this.form.value.firstNumber,
      second_number: this.form.value.secondNumber,
    };

    this.calculationService.createCalculation(payload).subscribe({
      next: (response: CalculationResponse) => {
        this.state = 'success';
        this.router.navigate(['/result'], {
          state: { calculation: response },
        });
      },
      error: (problem: ProblemDetails) => {
        this.state = 'error';
        this.errorMessage =
          problem.detail || problem.title || 'Не удалось выполнить вычисление. Попробуйте ещё раз.';
      },
    });
  }

  onClear(): void {
    this.form.reset({ firstNumber: 0, secondNumber: 0 });
    this.state = 'empty';
    this.errorMessage = '';
  }
}
