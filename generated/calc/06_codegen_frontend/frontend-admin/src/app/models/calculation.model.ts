export interface CalculationRequest {
  first_number: number;
  second_number: number;
}

export interface CalculationResponse {
  id: string;
  first_number: number;
  second_number: number;
  result: number;
  created_at: string;
}

export interface ProblemDetails {
  type?: string;
  title?: string;
  status?: number;
  detail?: string;
  instance?: string;
}
