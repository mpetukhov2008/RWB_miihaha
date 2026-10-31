import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiService {
  constructor(private http: HttpClient) {}

  call(operationId: string): Observable<unknown> {
    const map: Record<string, { method: string; path: string }> = {
      'createCalculation': { method: 'POST', path: '/calculations' },
    };
    const op = map[operationId];
    if (!op) return new Observable((s) => s.error(new Error('unknown op')));
    return this.http.request(op.method, op.path);
  }
}
