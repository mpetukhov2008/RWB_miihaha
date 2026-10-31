import { Component, inject, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { ApiService, Application } from '../../services/api.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-scr-003',
  standalone: true,
  imports: [CommonModule, MatButtonModule, MatProgressSpinnerModule],
  template: `
    <div class="scr-003">
      <div *ngIf="state === 'forbidden'" class="center">
        <p>Требуется авторизация</p>
        <button mat-button (click)="login()">Войти</button>
      </div>
      <div *ngIf="state === 'loading'" class="center">
        <mat-spinner></mat-spinner>
        <p>Анализ медиафайла…</p>
        <p>Поиск рекламного блока…</p>
        <p>Нарезка видео…</p>
      </div>
      <div *ngIf="state === 'error'" class="center">
        <p>Не удалось обработать файл</p>
        <button mat-button (click)="retry()">Повторить обработку</button>
        <button mat-button (click)="back()">Вернуться к загрузке</button>
      </div>
      <div *ngIf="state === 'success'" class="center">
        <p>Выполнено</p>
        <button mat-raised-button (click)="toResults()">Посмотреть результаты</button>
      </div>
    </div>
  `
})
export class Scr003Component implements OnInit, OnDestroy {
  private api = inject(ApiService);
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private sub?: Subscription;
  private timer?: any;
  state: 'empty' | 'loading' | 'error' | 'forbidden' | 'success' = 'loading';
  app?: Application;
  id = '';

  ngOnInit() {
    this.id = this.route.snapshot.paramMap.get('id') || '';
    if (!this.id) { this.router.navigate(['/']); return; }
    this.poll();
  }

  ngOnDestroy() { this.sub?.unsubscribe(); clearInterval(this.timer); }

  private poll() {
    this.sub = this.api.getApplication(this.id).subscribe({
      next: (app) => {
        this.app = app;
        if (app.status === 'completed') this.state = 'success';
        else if (app.status === 'failed') this.state = 'error';
      },
      error: (err) => {
        if (err.status === 401) this.state = 'forbidden';
        else if (err.status === 404) this.router.navigate(['/']);
        else this.state = 'error';
      }
    });
    this.timer = setInterval(() => this.poll(), 5000);
  }

  retry() { this.state = 'loading'; this.api.triggerProcessing(this.id).subscribe(); }
  back() { this.router.navigate(['/upload']); }
  toResults() { this.router.navigate(['/results', this.id]); }
  login() { /* TODO */ }
}