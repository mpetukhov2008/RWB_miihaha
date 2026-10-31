import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, catchError, map, throwError } from 'rxjs';

import { CalculationRequest, CalculationResponse, ProblemDetails } from '../models/calculation.model';

@Injectable({
  providedIn: 'root',
})
export class CalculationService {
  private readonly http = inject(HttpClient);
  private readonly baseUrl = '/calculations';

  /**
   * POST /calculations — createCalculation
   * Выполняет суммирование двух чисел.
   */
  createCalculation(request: CalculationRequest): Observable<CalculationResponse> {
    return this.http
      .post<CalculationResponse>(this.baseUrl, request)
      .pipe(
        map((response) => response),
        catchError((error: HttpErrorResponse) => {
          const problem: ProblemDetails = error.error ?? {
            title: 'Неизвестная ошибка',
            status: error.status,
          };
          return throwError(() => problem);
        }),
      );
  }
}
