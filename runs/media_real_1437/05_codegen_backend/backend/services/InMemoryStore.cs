using MediaProcessingApi.Entities;

namespace MediaProcessingApi.Services;

public class InMemoryStore
{
    private readonly object _lock = new();

    public Dictionary<string, Application> Applications { get; } = new();
    public Dictionary<string, ReferenceFile> ReferenceFiles { get; } = new();
    public Dictionary<string, MediaFile> MediaFiles { get; } = new();
    public Dictionary<string, PhotoAnalysisResult> PhotoAnalysisResults { get; } = new();
    public Dictionary<string, VideoAnalysisResult> VideoAnalysisResults { get; } = new();

    public Application? GetApplication(string id)
    {
        lock (_lock)
        {
            return Applications.TryGetValue(id, out var app) ? app : null;
        }
    }

    public void AddApplication(Application application)
    {
        lock (_lock)
        {
            Applications[application.Id] = application;
        }
    }

    public void UpdateApplication(Application application)
    {
        lock (_lock)
        {
            application.UpdatedAt = DateTime.UtcNow;
            Applications[application.Id] = application;
        }
    }

    public ReferenceFile? GetReferenceFile(string id)
    {
        lock (_lock)
        {
            return ReferenceFiles.TryGetValue(id, out var file) ? file : null;
        }
    }

    public void AddReferenceFile(ReferenceFile file)
    {
        lock (_lock)
        {
            ReferenceFiles[file.Id] = file;
        }
    }

    public MediaFile? GetMediaFile(string id)
    {
        lock (_lock)
        {
            return MediaFiles.TryGetValue(id, out var file) ? file : null;
        }
    }

    public void AddMediaFile(MediaFile file)
    {
        lock (_lock)
        {
            MediaFiles[file.Id] = file;
        }
    }

    public void UpdateMediaFile(MediaFile file)
    {
        lock (_lock)
        {
            MediaFiles[file.Id] = file;
        }
    }

    public PhotoAnalysisResult? GetPhotoAnalysisResult(string applicationId)
    {
        lock (_lock)
        {
            return PhotoAnalysisResults.Values.FirstOrDefault(r => r.ApplicationId == applicationId);
        }
    }

    public void AddPhotoAnalysisResult(PhotoAnalysisResult result)
    {
        lock (_lock)
        {
            PhotoAnalysisResults[result.Id] = result;
        }
    }

    public VideoAnalysisResult? GetVideoAnalysisResult(string applicationId)
    {
        lock (_lock)
        {
            return VideoAnalysisResults.Values.FirstOrDefault(r => r.ApplicationId == applicationId);
        }
    }

    public void AddVideoAnalysisResult(VideoAnalysisResult result)
    {
        lock (_lock)
        {
            VideoAnalysisResults[result.Id] = result;
        }
    }
}
