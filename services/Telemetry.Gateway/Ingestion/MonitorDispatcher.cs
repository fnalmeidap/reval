using System.Text;
using System.Text.Json;
using System.Threading.Channels;
using Reval.Telemetry.Gateway.Observability.Loki;

namespace Reval.Telemetry.Gateway.Ingestion.MonitorDispatcher;


public sealed class MonitorDispatcherService : BackgroundService
{
    private readonly ILogger<MonitorDispatcherService> logger;
    private readonly ChannelReader<byte[]> reader;
    private readonly ILokiClient lokiClient;
    private readonly IConfiguration config;

    public MonitorDispatcherService(ILogger<MonitorDispatcherService> logger, Channel<byte[]> channel, ILokiClient lokiClient, IConfiguration config)
    {
        this.logger = logger;
        reader = channel.Reader;
        this.lokiClient = lokiClient;
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

        return new LokiLogEntry
        {
            Timestamp = monitorSignal.GetProperty("timestamp").GetInt64(),
            Labels = new Dictionary<string, string>
            {
                { "scope", monitorSignal.GetProperty("scope").GetString() ?? "unknown" }
            },
            Line = JsonSerializer.Serialize(new Dictionary<string, string>
            {
                { "duration_ms", monitorSignal.GetProperty("duration_ms").GetString() ?? string.Empty },
                { "meta", monitorSignal.GetProperty("meta").GetString() ?? string.Empty }
            })
        };
    }
}
