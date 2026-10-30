import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-location',
  standalone: true,
  imports: [MatCardModule, MatButtonModule, RouterLink],
  template: `
    <div class="container">
      <h2>Текущая локация</h2>
      <mat-card>
        <mat-card-content>
          @if (position !== null) {
            <p>Координаты: {{ position.lat }}, {{ position.lon }}</p>
            <p>{{ nearest ?? 'В радиусе ничего не найдено' }}</p>
          } @else {
            <p>Получаем координаты...</p>
          }
        </mat-card-content>
      </mat-card>
      <button mat-raised-button color="primary" routerLink="/session">Сессия</button>
    </div>
  `,
  styles: [
    `.container { max-width: 480px; margin: 0 auto; padding: 16px; display: grid; gap: 16px; }`,
  ],
})
export class LocationComponent {
  private api = inject(ApiService);
  position: { lat: number; lon: number } | null = null;
  nearest: string | null = null;

  constructor() {
    navigator.geolocation?.getCurrentPosition((p) => {
      this.position = { lat: p.coords.latitude, lon: p.coords.longitude };
      this.api.findLocation(this.position.lat, this.position.lon, 150).subscribe({
        next: (res) => (this.nearest = (res as { name?: string })?.name ?? null),
        error: () => (this.nearest = null),
      });
    });
  }
}
