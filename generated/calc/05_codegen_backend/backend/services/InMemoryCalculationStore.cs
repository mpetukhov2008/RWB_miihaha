using Api.Entities;

namespace Api.Services;

public class InMemoryCalculationStore
{
    private readonly List<Calculation> _calculations = new();
    private readonly object _lock = new();

    public void Add(Calculation calculation)
    {
        lock (_lock)
        {
            _calculations.Add(calculation);
        }
    }

    public Calculation? GetById(string id)
    {
        lock (_lock)
        {
            return _calculations.FirstOrDefault(c => c.Id == id);
        }
    }

    public IReadOnlyList<Calculation> GetAll()
    {
        lock (_lock)
        {
            return _calculations.ToList();
        }
    }
}
