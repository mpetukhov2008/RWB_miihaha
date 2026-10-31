import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface LoginRequest { email: string; password: string; }
export interface LoginResponse { token: string; user: { id: string; email: string; role: 'driver' | 'admin'; }; }

@Injectable({ providedIn: 'root' })
export class AuthService {
  private http = inject(HttpClient);

  login(req: LoginRequest): Observable<LoginResponse> {
    return this.http.post<LoginResponse>('/auth/login', req);
  }
}