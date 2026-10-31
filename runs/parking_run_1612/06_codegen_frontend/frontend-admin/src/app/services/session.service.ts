import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Session { id: string; zone_id: string; zone_name: string; started_at: string; rate_per_hour: number; currency: string; status: 'active' | 'completed' | 'overdue'; current_amount?: number; ended_at?: string; duration_seconds?: number; amount?: number; }

@Injectable({ providedIn: 'root' })
export class SessionService {
  private http = inject(HttpClient);

  startSession(zoneId: string, latitude?: number, longitude?: number): Observable<{ session: Session; payment: { id: string; amount: number; status: 'pending'; } }> {
    return this.http.post<any>('/sessions', { zone_id: zoneId, latitude, longitude });
  }

  getActiveSession(): Observable<{ session: Session | null }> {
    return this.http.get<{ session: Session | null }>('/sessions/active');
  }

  endSession(sessionId: string): Observable<{ session: Session; payment: { id: string; amount: number; status: 'paid'; paid_at: string; } }> {
    return this.http.post<any>(`/sessions/${sessionId}/end`, {});
  }
}