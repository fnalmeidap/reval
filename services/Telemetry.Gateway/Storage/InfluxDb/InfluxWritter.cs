using System.Globalization;
using InfluxDB.Client;
using InfluxDB.Client.Api.Domain;
using InfluxDB.Client.Writes;
using Reval.Telemetry.Gateway.Configuration;
using Reval.Telemetry.Gateway.Observability.Loki;

namespace Reval.Telemetry.Gateway.Storage.InfluxDB;

public sealed class InfluxWriter : IInfluxWriter
{
    private readonly WriteApiAsync writeApi;
    private readonly InfluxSettings settings;

    public InfluxWriter(InfluxDBClient client, InfluxSettings settings)
    {
        this.settings = settings;
        writeApi = client.GetWriteApiAsync();
    }

    public Task WriteAsync(LokiLogEntry entry, CancellationToken ct)
    {
        var timestampNs = long.Parse(ConvertToNanoseconds(entry.Timestamp));

        var point = PointData
            .Measurement("monitor_signal")
            .Tag("scope", entry.Labels["scope"])
            .Field("line", entry.Line)
            .Timestamp(timestampNs, WritePrecision.Ns);

        return writeApi.WritePointAsync(
            point,
            settings.Bucket,
            settings.Org,
            ct
        );
    }
    
    static string ConvertToNanoseconds(string secondsString)
    {
        var seconds = double.Parse(secondsString, CultureInfo.InvariantCulture);
        return ((long)(seconds * 1_000_000_000)).ToString();
    }
}
