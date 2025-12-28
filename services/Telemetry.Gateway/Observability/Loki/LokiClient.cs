using System.Text;
using System.Text.Json;

namespace Reval.Telemetry.Gateway.Observability.Loki;

public sealed class LokiClient : ILokiClient
{
    private readonly ILogger<LokiClient> logger;
    private readonly HttpClient httpClient;
    private readonly string lokiEndpoint;
    private readonly IConfiguration config;

    public LokiClient(ILogger<LokiClient> logger, HttpClient httpClient, string lokiEndpoint, IConfiguration config)
    {
        this.logger = logger;
        this.httpClient = httpClient;
        this.lokiEndpoint = lokiEndpoint;
        this.config = config;
    }

    public async Task PushAsync(
        IReadOnlyList<LokiLogEntry> entries,
        CancellationToken cancellationToken)
    {
        if (entries.Count == 0)
        {
            return;
        }

        var payload = new
        {
            streams = new[]
            {
                new
                {
                    stream = entries.Select(e => e.Labels),
                    values = entries.Select(e => new[]
                    { 
                        e.Timestamp.ToString(),
                        e.Line
                    })
                }
            }
        };

        var content = new StringContent(
            JsonSerializer.Serialize(payload),
            Encoding.UTF8,
            "application/json"
        );
        
        logger.LogInformation("Sending this content to Loki: {}", await content.ReadAsStringAsync(cancellationToken));
        // var response = await httpClient.PostAsync(lokiEndpoint, content, cancellationToken);
        // response.EnsureSuccessStatusCode();
    }
}