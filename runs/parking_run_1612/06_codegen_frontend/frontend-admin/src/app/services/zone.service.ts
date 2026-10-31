import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Zone { id: string; name: string; rate_per_hour: number; currency: string; }
export interface NearbyZoneResponse { in_zone: boolean; zone: Zone | null; }

@Injectable({ providedIn: 'root' })
export class ZoneService {
  private http = inject(HttpClient);

  getNearbyZone(latitude: number, longitude: number): Observable<NearbyZoneResponse> {
    return this.http.get<NearbyZoneResponse>('/zones/nearby', { params: { latitude: String(latitude), longitude: String(longitude) } });
  }
}