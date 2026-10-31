import { Component, inject, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { ZoneService, NearbyZoneResponse } from '../../services/zone.service';
import { SessionService } from '../../services/session.service';

@Component({ selector: 'app-home', template: `<div *ngIf="loading">Определение зоны...</div><div *ngIf="error">{{ error }}</div><div *ngIf="!loading && !error"><div *ngIf="!zone">Вне платной зоны</div><div *ngIf="zone"><h2>{{ zone.name }}</h2><p>Тариф: {{ zone.rate_per_hour }} {{ zone.currency }}/час</p><button (click)="startSession()">Начать сессию</button></div><button (click)="router.navigate(['/history'])">История</button><button (click)="router.navigate(['/notifications'])">Уведомления</button></div>` })
export class HomeComponent implements OnInit {
  private zoneService = inject(ZoneService);
  private sessionService = inject(SessionService);
  private router = inject(Router);
  loading = true;
  error = '';
  zone: NearbyZoneResponse['zone'] = null;

  ngOnInit() { this.detectZone(); }

  detectZone() {
    this.loading = true;
    this.error = '';
    navigator.geolocation.getCurrentPosition(
      (pos) => this.zoneService.getNearbyZone(pos.coords.latitude, pos.coords.longitude).subscribe({
        next: (res) => { this.zone = res.zone; this.loading = false; },
        error: () => { this.error = 'Ошибка определения зоны'; this.loading = false; }
      }),
      () => { this.error = 'Ошибка геолокации'; this.loading = false; }
    );
  }

  startSession() {
    if (!this.zone) return;
    this.sessionService.startSession(this.zone.id).subscribe({
      next: () => this.router.navigate(['/session']),
      error: () => this.error = 'Не удалось начать сессию'
    });
  }
}