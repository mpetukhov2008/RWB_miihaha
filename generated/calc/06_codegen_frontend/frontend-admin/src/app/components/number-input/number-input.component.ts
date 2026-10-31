import { Component, Input, forwardRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  ControlValueAccessor,
  NG_VALUE_ACCESSOR,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';

@Component({
  selector: 'app-number-input',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, MatFormFieldModule, MatInputModule],
  providers: [
    {
      provide: NG_VALUE_ACCESSOR,
      useExisting: forwardRef(() => NumberInputComponent),
      multi: true,
    },
  ],
  template: `
    <mat-form-field appearance="outline" class="number-input-field">
      <mat-label>{{ label }}</mat-label>
      <input
        matInput
        type="number"
        step="any"
        [formControl]="control"
        [placeholder]="placeholder"
        [disabled]="disabled"
      />
      <mat-error *ngIf="control?.hasError('required')">Обязательное поле</mat-error>
      <mat-error *ngIf="control?.hasError('min')">Значение слишком маленькое</mat-error>
      <mat-error *ngIf="control?.hasError('max')">Значение слишком большое</mat-error>
    </mat-form-field>
  `,
})
export class NumberInputComponent implements ControlValueAccessor {
  @Input() label = 'Число';
  @Input() placeholder = 'Введите число';
  @Input() disabled = false;

  private onChange: (value: number | null) => void = () => {};
  private onTouched: () => void = () => {};

  control = new (import('@angular/forms').FormControl)(null, {
    validators: [Validators.required, Validators.min(-1e15), Validators.max(1e15)],
    updateOn: 'change',
  });

  writeValue(value: number | null): void {
    this.control.setValue(value ?? null, { emitEvent: false });
  }

  registerOnChange(fn: (value: number | null) => void): void {
    this.onChange = fn;
    this.control.valueChanges.subscribe((value) => this.onChange(value));
  }

  registerOnTouched(fn: () => void): void {
    this.onTouched = fn;
  }

  setDisabledState(isDisabled: boolean): void {
    this.disabled = isDisabled;
    if (isDisabled) {
      this.control.disable({ emitEvent: false });
    } else {
      this.control.enable({ emitEvent: false });
    }
  }
}
