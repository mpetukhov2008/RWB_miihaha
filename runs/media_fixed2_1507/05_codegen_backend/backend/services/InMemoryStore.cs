using MediaProcessingApi.Entities;

namespace MediaProcessingApi.Services;

public class InMemoryStore
{
    private readonly Dictionary<string, Application> _applications = new();
    private readonly Dictionary<string, MediaFile> _files = new();
    private readonly Dictionary<string, VideoSegment> _segments = new();
    private readonly Dictionary<string, ProcessingJob> _jobs = new();
    private readonly object _lock = new();

    public Application? GetApplication(string id)
    {
        lock (_lock)
        {
            return _applications.TryGetValue(id, out var app) ? app : null;
        }
    }

    public void AddApplication(Application application)
    {
        lock (_lock)
        {
            _applications[application.Id] = application;
        }
    }

    public void UpdateApplication(Application application)
    {
        lock (_lock)
        {
            _applications[application.Id] = application;
        }
    }

    public MediaFile? GetFile(string id)
    {
        lock (_lock)
        {
            return _files.TryGetValue(id, out var file) ? file : null;
        }
    }

    public void AddFile(MediaFile file)
    {
        lock (_lock)
        {
            _files[file.Id] = file;
        }
    }

    public void UpdateFile(MediaFile file)
    {
        lock (_lock)
        {
            _files[file.Id] = file;
        }
    }

    public List<VideoSegment> GetSegmentsByApplicationId(string applicationId)
    {
        lock (_lock)
        {
            return _segments.Values.Where(s => s.ApplicationId == applicationId).ToList();
        }
    }

    public void AddSegment(VideoSegment segment)
    {
        lock (_lock)
        {
            _segments[segment.Id] = segment;
        }
    }

    public void UpdateSegment(VideoSegment segment)
    {
        lock (_lock)
        {
            _segments[segment.Id] = segment;
        }
    }

    public ProcessingJob? GetJob(string id)
    {
        lock (_lock)
        {
            return _jobs.TryGetValue(id, out var job) ? job : null;
        }
    }

    public void AddJob(ProcessingJob job)
    {
        lock (_lock)
        {
            _jobs[job.Id] = job;
        }
    }

    public void UpdateJob(ProcessingJob job)
    {
        lock (_lock)
        {
            _jobs[job.Id] = job;
        }
    }

    public bool HasActiveJobForApplication(string applicationId)
    {
        lock (_lock)
        {
            return _jobs.Values.Any(j => j.ApplicationId == applicationId && (j.Status == "queued" || j.Status == "running"));
        }
    }
}
