using Reval.Telemetry.Gateway.Observability.Loki;

namespace Reval.Telemetry.Gateway.Storage.InfluxDB;

public interface IInfluxWriter
{
    Task WriteAsync(LokiLogEntry entry, CancellationToken ct);
}