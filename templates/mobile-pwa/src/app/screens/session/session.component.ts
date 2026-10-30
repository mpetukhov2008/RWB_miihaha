import { Component, OnDestroy, OnInit, inject, signal } from '@angular/core';
import { RouterLink } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-session',
  standalone: true,
  imports: [MatCardModule, MatButtonModule, MatSnackBarModule, RouterLink],
  template: `
    <div class="container">
      <h2>Активная сессия</h2>
      <mat-card>
        <mat-card-content>
          @if (sessionId() !== null) {
            <p>Статус: активна</p>
            <p>Осталось: {{ remaining() }}</p>
            <button mat-raised-button color="primary" routerLink="/payment">
              Перейти к оплате
            </button>
          } @else {
            <p>Нет активной сессии</p>
          }
        </mat-card-content>
      </mat-card>
    </div>
  `,
  styles: [
    `.container { max-width: 480px; margin: 0 auto; padding: 16px; display: grid; gap: 16px; }`,
  ],
})
export class SessionComponent implements OnInit, OnDestroy {
  private api = inject(ApiService);
  private snackBar = inject(MatSnackBar);
  private timer: ReturnType<typeof setInterval> | null = null;

  sessionId = signal<string | null>(null);
  endsAt = signal<number | null>(null);
  remaining = signal('--:--');
  warned = false;

  ngOnInit(): void {
    this.api.activeSession().subscribe({
      next: (res) => {
        const s = res as { id?: string; endsAt?: number };
        this.sessionId.set(s?.id ?? null);
        this.endsAt.set(s?.endsAt ?? null);
        this.startCountdown();
      },
    });
  }

  ngOnDestroy(): void {
    if (this.timer) clearInterval(this.timer);
  }

  private startCountdown(): void {
    this.timer = setInterval(() => this.tick(), 1000);
  }

  private tick(): void {
    const endsAt = this.endsAt();
    if (!endsAt) return;
    const left = Math.max(0, endsAt - Date.now());
    const min = Math.floor(left / 60000);
    const sec = Math.floor((left % 60000) / 1000);
    this.remaining.set(`${String(min).padStart(2, '0')}:${String(sec).padStart(2, '0')}`);
    if (!this.warned && left <= 10 * 60 * 1000 && left > 0) {
      this.warned = true;
      this.snackBar.open('Сессия скоро закончится', 'OK', { duration: 5000 });
    }
  }
}
