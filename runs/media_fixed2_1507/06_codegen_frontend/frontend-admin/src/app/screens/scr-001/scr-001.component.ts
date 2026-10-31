import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-scr-001',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatCardModule, MatProgressSpinnerModule],
  template: `
    <div class="scr-001">
      <div *ngIf="state === 'loading'" class="center">
        <mat-spinner></mat-spinner>
      </div>
      <div *ngIf="state === 'error'" class="center">
        <p>Ошибка инициализации</p>
        <button mat-button (click)="retry()">Повторить</button>
      </div>
      <div *ngIf="state === 'forbidden'" class="center">
        <p>Требуется авторизация</p>
        <button mat-button (click)="login()">Войти</button>
      </div>
      <div *ngIf="state === 'success' || state === 'empty'" class="cards">
        <mat-card class="card" (click)="select('photo')">
          <mat-card-title>Фотоотчет</mat-card-title>
          <mat-card-content>JPEG/PNG</mat-card-content>
        </mat-card>
        <mat-card class="card" (click)="select('video')">
          <mat-card-title>Видеопоток</mat-card-title>
          <mat-card-content>MP4 150–300 с</mat-card-content>
        </mat-card>
      </div>
    </div>
  `
})
export class Scr001Component {
  private router = inject(Router);
  state: 'empty' | 'loading' | 'error' | 'forbidden' | 'success' = 'loading';

  constructor() {
    setTimeout(() => this.state = 'success', 500);
  }

  retry() { this.state = 'loading'; setTimeout(() => this.state = 'success', 500); }
  login() { /* TODO: auth */ }
  select(type: string) { this.router.navigate(['/upload'], { queryParams: { type } }); }
}