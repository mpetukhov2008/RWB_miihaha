import { Injectable } from '@angular/core';
import { of } from 'rxjs';
import { delay } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class ApiService {
  call(operationId: string) {
    return of({ status: 'ok', data: 'Сгенерировано ИИ' }).pipe(delay(500));
  }
}
