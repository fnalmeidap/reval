namespace Reval.Signal;

public enum ProfileStatus
{
    Unknown = 0,
    Executing = 1,
    Crashed = 2,
}

public class MonitorProfile : ISignal
{
    /// <summary>
    /// Timestamp of when the monitored execution completed
    /// </summary>
    public DateTime Timestamp { get; set; }

    /// <summary>
    /// Name of the monitored execution
    /// </summary>
    public string Name { get; set; } = string.Empty;

    /// <summary>
    /// Duration of the monitored execution in milliseconds
    /// </summary>
    public long Duration { get; set; }

    /// <summary>
    /// Status of the monitored execution
    /// </summary>
    public ProfileStatus Status { get; set; }
}

