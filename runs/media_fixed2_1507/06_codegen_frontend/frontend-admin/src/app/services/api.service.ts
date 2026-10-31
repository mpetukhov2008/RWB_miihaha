import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface CreateApplicationRequest {
  type: 'photo' | 'video';
  reference_file_id: string;
  source_file_id: string;
}

export interface Application {
  id: string;
  type?: string;
  status: string;
  similarity_score?: number;
  verification_status?: string;
  result_file_ids?: string[];
  segments?: { start_time: number; end_time: number; result_file_id: string }[];
  created_at: string;
  updated_at?: string;
}

export interface UploadUrlResponse {
  file_id: string;
  upload_url: string;
  s3_key: string;
  expires_at: string;
}

@Injectable({ providedIn: 'root' })
export class ApiService {
  private http = inject(HttpClient);
  private baseUrl = '/api';

  createApplication(req: CreateApplicationRequest): Observable<Application> {
    return this.http.post<Application>(`${this.baseUrl}/applications`, req);
  }

  getApplication(id: string): Observable<Application> {
    return this.http.get<Application>(`${this.baseUrl}/applications/${id}`);
  }

  getUploadUrl(fileType: string, fileRole: string, sizeBytes: number): Observable<UploadUrlResponse> {
    return this.http.post<UploadUrlResponse>(`${this.baseUrl}/files/upload-url`, {
      file_type: fileType,
      file_role: fileRole,
      size_bytes: sizeBytes
    });
  }

  confirmFileUpload(id: string): Observable<{ file_id: string; status: string }> {
    return this.http.post(`${this.baseUrl}/files/${id}/confirm`, {});
  }

  triggerProcessing(id: string): Observable<{ application_id: string; job_id: string; status: string }> {
    return this.http.post(`${this.baseUrl}/applications/${id}/process`, {});
  }
}