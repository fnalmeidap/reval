using System.Globalization;
using System.Text;
using System.Text.Json;
using System.Threading.Channels;
using Reval.Telemetry.Gateway.Observability.Loki;
using Reval.Telemetry.Gateway.Storage.InfluxDB;

namespace Reval.Telemetry.Gateway.Ingestion.MonitorDispatcher;


public sealed class MonitorDispatcherService : BackgroundService
{
    private readonly ILogger<MonitorDispatcherService> logger;
    private readonly ChannelReader<byte[]> reader;
    private readonly ILokiClient lokiClient;
    private readonly IConfiguration config;
    private readonly IInfluxWriter influxWriter;

    public MonitorDispatcherService(
        ILogger<MonitorDispatcherService> logger,
        Channel<byte[]> channel,
        ILokiClient lokiClient,
        IInfluxWriter influxWriter,
        IConfiguration config)
    {
        this.logger = logger;
        reader = channel.Reader;
        this.lokiClient = lokiClient;
        this.influxWriter = influxWriter;
        this.config = config;
    }

    protected override async Task ExecuteAsync(CancellationToken cancellationToken)
    {
        var batch = new List<LokiLogEntry>(500);

        while (await reader.WaitToReadAsync(cancellationToken))
        {
            while (reader.TryRead(out var bytes))
            {
                batch.Add(ToLogEntry(bytes));
                if (batch.Count >= 500 || batch.Count > 0)
                {
                    logger.LogInformation($"Dispatching {batch.Count} log entries to Loki");
                    await lokiClient.PushAsync(batch, cancellationToken);
                    foreach (var entry in batch)
                    {
                        await influxWriter.WriteAsync(entry, cancellationToken);
                    }
                    batch.Clear();
                }
            }
        }
    }

    private static LokiLogEntry ToLogEntry(byte[] bytes)
    {
        var monitorSignal = JsonDocument
            .Parse(Encoding.UTF8.GetString(bytes))
            .RootElement;

        Console.WriteLine($"Monitor Signal: {monitorSignal}");

        try
        {
            var timestamp = monitorSignal.GetProperty("timestamp").GetDecimal().ToString();
            var labels = new Dictionary<string, string>
            {
                { "scope", monitorSignal.GetProperty("scope").GetString() ?? "unknown" }
            };

            var line = JsonSerializer.Serialize(new Dictionary<string, string>
            {

                { "duration_ms", monitorSignal.GetProperty("duration_ms").GetDecimal().ToString() ?? string.Empty },
                { "meta", monitorSignal.GetProperty("meta").GetRawText() ?? string.Empty }
            });

            return new LokiLogEntry
            {
                Timestamp = timestamp ?? string.Empty,
                Labels = labels,
                Line = line
            };
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error parsing monitor signal: {ex.Message}");
            throw;
        }

    }
}
