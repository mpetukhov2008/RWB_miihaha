import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiService {
  constructor(private http: HttpClient) {}

  call(operationId: string): Observable<unknown> {
    const map: Record<string, { method: string; path: string }> = {
      'getZone': { method: 'GET', path: '/zones/{zoneId}' },
      'startSession': { method: 'POST', path: '/sessions' },
      'completeSession': { method: 'POST', path: '/sessions/{sessionId}/complete' },
      'listSessions': { method: 'GET', path: '/sessions' },
      'createZone': { method: 'POST', path: '/admin/zones' },
    };
    const op = map[operationId];
    if (!op) return new Observable((s) => s.error(new Error('unknown op')));
    return this.http.request(op.method, op.path);
  }
}
