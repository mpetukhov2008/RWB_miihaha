import { Component, OnInit, inject, signal } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-payment',
  standalone: true,
  imports: [MatCardModule, MatButtonModule, MatSnackBarModule],
  template: `
    <div class="container">
      <h2>Оплата</h2>
      <mat-card>
        <mat-card-content>
          @if (url() !== null) {
            <p>Оплата обрабатывается внешним провайдером.</p>
            <a mat-raised-button color="primary" [href]="url()"> Перейти к оплате </a>
          } @else {
            <p>Ссылка оплаты недоступна.</p>
          }
        </mat-card-content>
      </mat-card>
    </div>
  `,
  styles: [
    `.container { max-width: 480px; margin: 0 auto; padding: 16px; display: grid; gap: 16px; }`,
  ],
})
export class PaymentComponent implements OnInit {
  private api = inject(ApiService);
  private snackBar = inject(MatSnackBar);
  url = signal<string | null>(null);

  ngOnInit(): void {
    this.api.activeSession().subscribe({
      next: (s) => {
        const id = (s as { id?: string })?.id;
        if (!id) return;
        this.api.paymentUrl(id).subscribe({
          next: (r) => this.url.set(r.url),
          error: () => this.snackBar.open('Ошибка получения ссылки', 'OK'),
        });
      },
    });
  }
}
