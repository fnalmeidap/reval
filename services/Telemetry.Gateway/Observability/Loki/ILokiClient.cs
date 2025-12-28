namespace Reval.Telemetry.Gateway.Observability.Loki;

public interface ILokiClient
{
    Task PushAsync(
        IReadOnlyList<LokiLogEntry> entries,
        CancellationToken cancellationToken);
}
