import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiService {
  constructor(private http: HttpClient) {}

  call(operationId: string): Observable<unknown> {
    const map: Record<string, { method: string; path: string }> = {
      'login': { method: 'POST', path: '/auth/login' },
      'getNearbyZone': { method: 'GET', path: '/zones/nearby' },
      'startSession': { method: 'POST', path: '/sessions' },
      'getActiveSession': { method: 'GET', path: '/sessions/active' },
      'endSession': { method: 'POST', path: '/sessions/{session_id}/end' },
      'listMySessions': { method: 'GET', path: '/sessions' },
      'listNotifications': { method: 'GET', path: '/notifications' },
      'markNotificationRead': { method: 'POST', path: '/notifications/{notification_id}/read' },
      'adminListZones': { method: 'GET', path: '/admin/zones' },
      'adminCreateZone': { method: 'POST', path: '/admin/zones' },
      'adminUpdateZone': { method: 'PUT', path: '/admin/zones/{zone_id}' },
      'adminListSessions': { method: 'GET', path: '/admin/sessions' },
    };
    const op = map[operationId];
    if (!op) return new Observable((s) => s.error(new Error('unknown op')));
    return this.http.request(op.method, op.path);
  }
}
