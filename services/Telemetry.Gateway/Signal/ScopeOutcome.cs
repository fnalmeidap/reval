namespace Reval.Telemetry.Gateway.Signal;

// TODO: define domain-specific outcomes (should be non contractual? maybe string?)
public enum ScopeOutcome
{
}

public class ExecutionOutcome : ISignal
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
    /// Outcome of the monitored execution
    /// </summary>
    public ScopeOutcome Outcome { get; set; }
}
