using System.Net.Sockets;
using Microsoft.AspNetCore.SignalR;
using Reval.Telemetry.Gateway.Hubs;

namespace Reval.Telemetry.Gateway.Ingestion.MonitorListener;

public class MonitorListener : BackgroundService
{
    private readonly ILogger<MonitorListener> logger;
    private readonly UdpClient client;
    private readonly IHubContext<Frame> hub;
    
    public MonitorListener(ILogger<MonitorListener> logger, UdpClient client, IHubContext<Frame> hub)
    {
        this.client = client;
        this.logger = logger;
        this.hub = hub;
    }

    // TODO: handle mutiple connections and message types
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            logger.LogInformation($"UDP client listening on {client.Client.LocalEndPoint}");

        try
        {
            while (!stoppingToken.IsCancellationRequested)
            {
                try
                {
                    var result = await client.ReceiveAsync(stoppingToken);
                    var bytes = result.Buffer;

                    await hub.Clients.All.SendAsync("ReceiveFrame", bytes);

                    logger.LogInformation(
                        $"Received UDP message from {result.RemoteEndPoint}, size: {bytes.Length} bytes");
                }
                catch (OperationCanceledException)
                {
                    break;
                }
                catch (Exception ex)
                {
                    logger.LogError(ex, "Error receiving UDP message");
                }
            }
        }
        finally
        {
            client.Close();
            logger.LogInformation("UDP Listener stopped");
        }
    }

    public override void Dispose()
    {
        client.Close();
        base.Dispose();
    }
}
