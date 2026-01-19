namespace Reval.Telemetry.Gateway.Observability.Loki;

public sealed class LokiLogEntry
{
    public long Timestamp { get; init; }
    public Dictionary<string, string> Labels { get; init; } = new Dictionary<string, string>();
    public string Line { get; init; } = string.Empty;
}