import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class ApiService {
  constructor(private http: HttpClient) {}

  call(operationId: string): Observable<unknown> {
    const map: Record<string, { method: string; path: string }> = {
      'createApplication': { method: 'POST', path: '/applications' },
      'getApplication': { method: 'GET', path: '/applications/{id}' },
      'getUploadUrl': { method: 'POST', path: '/files/upload-url' },
      'confirmFileUpload': { method: 'POST', path: '/files/{id}/confirm' },
      'triggerProcessing': { method: 'POST', path: '/applications/{id}/process' },
      'getVideoSegments': { method: 'GET', path: '/applications/{id}/segments' },
      'getDownloadUrl': { method: 'GET', path: '/files/{id}/download-url' },
    };
    const op = map[operationId];
    if (!op) return new Observable((s) => s.error(new Error('unknown op')));
    return this.http.request(op.method, op.path);
  }
}
