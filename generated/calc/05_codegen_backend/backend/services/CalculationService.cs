using Api.Entities;
using Api.Dtos;

namespace Api.Services;

public class CalculationService
{
    private readonly InMemoryCalculationStore _store;

    public CalculationService(InMemoryCalculationStore store)
    {
        _store = store;
    }

    public Task<CalculationResponse> CreateCalculationAsync(decimal firstNumber, decimal secondNumber)
    {
        var calculation = new Calculation
        {
            Id = Guid.NewGuid().ToString(),
            FirstNumber = firstNumber,
            SecondNumber = secondNumber,
            Result = firstNumber + secondNumber,
            CreatedAt = DateTime.UtcNow
        };

        _store.Add(calculation);

        return Task.FromResult(new CalculationResponse
        {
            Id = calculation.Id,
            FirstNumber = calculation.FirstNumber,
            SecondNumber = calculation.SecondNumber,
            Result = calculation.Result,
            CreatedAt = calculation.CreatedAt
        });
    }
}
