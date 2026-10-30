import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  private readonly baseUrl = '/api';

  findLocation(lat: number, lon: number, radiusM: number): Observable<unknown> {
    return this.http.get(`${this.baseUrl}/locations/nearest`, {
      params: { lat: String(lat), lon: String(lon), radius: String(radiusM) },
    });
  }

  activeSession(): Observable<unknown> {
    return this.http.get(`${this.baseUrl}/sessions/active`);
  }

  paymentUrl(sessionId: string): Observable<{ url: string }> {
    return this.http.get<{ url: string }>(
      `${this.baseUrl}/sessions/${sessionId}/payment-url`,
    );
  }
}
