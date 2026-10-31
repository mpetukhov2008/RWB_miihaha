import { Component, inject } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { MatCardModule } from '@angular/material/card';
import { ApiService } from '../../services/api.service';

@Component({
  selector: 'app-scr-002',
  standalone: true,
  imports: [CommonModule, FormsModule, MatButtonModule, MatProgressBarModule, MatCardModule],
  template: `
    <div class="scr-002">
      <div *ngIf="state === 'forbidden'" class="center">
        <p>Требуется авторизация</p>
        <button mat-button (click)="login()">Войти</button>
      </div>
      <div *ngIf="state !== 'forbidden'">
        <mat-card class="slot">
          <mat-card-title>Исходный файл</mat-card-title>
          <input type="file" (change)="onSourceFile($event)" />
          <mat-progress-bar *ngIf="sourceProgress > 0" [value]="sourceProgress"></mat-progress-bar>
          <p *ngIf="sourceError" class="error">{{ sourceError }}</p>
          <button mat-button *ngIf="sourceError" (click)="retrySource()">Повторить</button>
        </mat-card>
        <mat-card class="slot">
          <mat-card-title>Эталонный макет</mat-card-title>
          <input type="file" (change)="onRefFile($event)" />
          <mat-progress-bar *ngIf="refProgress > 0" [value]="refProgress"></mat-progress-bar>
          <p *ngIf="refError" class="error">{{ refError }}</p>
          <button mat-button *ngIf="refError" (click)="retryRef()">Повторить</button>
        </mat-card>
        <button mat-raised-button [disabled]="!canCreate" (click)="create()">Создать заявку</button>
      </div>
    </div>
  `
})
export class Scr002Component {
  private api = inject(ApiService);
  private router = inject(Router);
  state: 'empty' | 'loading' | 'error' | 'forbidden' | 'success' = 'empty';
  sourceProgress = 0; refProgress = 0;
  sourceError = ''; refError = '';
  sourceFile: File | null = null; refFile: File | null = null;
  sourceFileId = ''; refFileId = '';
  type = 'photo';

  get canCreate() { return !!this.sourceFileId && !!this.refFileId; }

  onSourceFile(e: Event) { this.uploadFile(e, 'source'); }
  onRefFile(e: Event) { this.uploadFile(e, 'reference'); }

  private uploadFile(e: Event, role: string) {
    const input = e.target as HTMLInputElement;
    const file = input.files?.[0];
    if (!file) return;
    const fileType = file.type.includes('png') ? 'png' : file.type.includes('jpeg') ? 'jpeg' : 'mp4';
    this.api.getUploadUrl(fileType, role, file.size).subscribe({
      next: (res) => {
        if (role === 'source') { this.sourceFile = file; this.sourceFileId = res.file_id; this.sourceProgress = 100; }
        else { this.refFile = file; this.refFileId = res.file_id; this.refProgress = 100; }
        this.api.confirmFileUpload(res.file_id).subscribe();
      },
      error: (err) => {
        if (role === 'source') this.sourceError = 'Ошибка загрузки';
        else this.refError = 'Ошибка загрузки';
      }
    });
  }

  retrySource() { this.sourceError = ''; }
  retryRef() { this.refError = ''; }
  login() { /* TODO */ }
  create() {
    this.api.createApplication({ type: this.type as any, reference_file_id: this.refFileId, source_file_id: this.sourceFileId }).subscribe({
      next: (app) => this.router.navigate(['/status', app.id]),
      error: () => this.state = 'error'
    });
  }
}