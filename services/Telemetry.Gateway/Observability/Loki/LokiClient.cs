using System.Globalization;
using System.Text;
using System.Text.Json;
using Microsoft.Extensions.Options;
using Reval.Telemetry.Gateway.Configuration;

namespace Reval.Telemetry.Gateway.Observability.Loki;

public sealed class LokiClient : ILokiClient
{
    private readonly ILogger<LokiClient> logger;
    private readonly HttpClient httpClient;
    private readonly LokiSettings settings;

    public LokiClient(ILogger<LokiClient> logger, HttpClient httpClient, IOptions<LokiSettings> options)
    {
        this.logger = logger;
        this.httpClient = httpClient;
        settings = options.Value;
        logger.LogInformation("LokiClient initialized with endpoint: {Endpoint}", settings.Endpoint);
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
                    stream = entries.First().Labels,
                    values = entries.Select(e => new[]
                    { 
                        ConvertToNanoseconds(e.Timestamp),
                        e.Line
                    }).ToArray()
                }
            }
        };

        var content = new StringContent(
            JsonSerializer.Serialize(payload),
            Encoding.UTF8,
            "application/json"
        );
        
        var requestUri = new Uri(
            httpClient.BaseAddress!,
            settings.Route);

        var request = new HttpRequestMessage(
            HttpMethod.Post,
            requestUri)
        {
            Content = content
        };

        logger.LogInformation("POST {Url}", request.RequestUri);
        logger.LogInformation("Sending this content to Loki: {Content}", await content.ReadAsStringAsync(cancellationToken));
        try
        {
            logger.LogInformation("Loki Push Payload: {Payload}", JsonSerializer.Serialize(payload));
            var response = await httpClient.SendAsync(request, cancellationToken);
            logger.LogInformation("Loki response content: {Content}", await response.Content.ReadAsStringAsync(cancellationToken));
            response.EnsureSuccessStatusCode();
        }
        catch (Exception ex)
        {
            logger.LogError(ex.Message, "Failed to serialize Loki payload for logging.");
            
        }
    }

    static string ConvertToNanoseconds(string secondsString)
    {
        var seconds = double.Parse(secondsString, CultureInfo.InvariantCulture);
        return ((long)(seconds * 1_000_000_000)).ToString();
    }
}