namespace Reval.Telemetry.Gateway.Observability.Loki;

public sealed class LokiLogEntry
{
    public string Timestamp { get; init; } = string.Empty;
    public Dictionary<string, string> Labels { get; init; } = new Dictionary<string, string>();
    public string Line { get; init; } = string.Empty;
}