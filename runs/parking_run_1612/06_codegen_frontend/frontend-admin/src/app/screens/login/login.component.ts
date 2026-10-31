import { Component, inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({ selector: 'app-login', template: `<div *ngIf="loading">Загрузка...</div><div *ngIf="error">{{ error }}</div><form [formGroup]="form" (ngSubmit)="submit()"><input formControlName="email" placeholder="Email" /><input formControlName="password" type="password" placeholder="Пароль" /><button type="submit" [disabled]="loading || !form.valid">Войти</button></form>` })
export class LoginComponent {
  private fb = inject(FormBuilder);
  private auth = inject(AuthService);
  private router = inject(Router);
  form: FormGroup = this.fb.group({ email: ['', [Validators.required, Validators.email]], password: ['', Validators.required] });
  loading = false;
  error = '';

  submit() {
    if (!this.form.valid) return;
    this.loading = true;
    this.error = '';
    this.auth.login(this.form.value).subscribe({
      next: (res) => { localStorage.setItem('token', res.token); this.router.navigate(['/']); },
      error: (err) => { this.error = 'Неверные данные'; this.loading = false; }
    });
  }
}