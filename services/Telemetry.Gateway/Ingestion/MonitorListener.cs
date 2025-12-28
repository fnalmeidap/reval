using System.Net.Sockets;
using System.Threading.Channels;
using Microsoft.AspNetCore.SignalR;
using Reval.Telemetry.Gateway.Configuration;
using Reval.Telemetry.Gateway.Hubs;

namespace Reval.Telemetry.Gateway.Ingestion.MonitorListener;

public class MonitorListener : BackgroundService
{
    private readonly ILogger<MonitorListener> logger;
    private readonly UdpClient client;
    private readonly IHubContext<Frame> hub;
    private readonly IConfiguration config;
    private readonly ChannelWriter<byte[]> writer;
    
    public MonitorListener(
        ILogger<MonitorListener> logger,
        UdpClient client,
        IHubContext<Frame> hub,
        Channel<byte[]> channel,
        IConfiguration config)
    {
        this.client = client;
        this.logger = logger;
        this.hub = hub;
        this.writer = channel.Writer;
        this.config = config;
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

                    await writer.WriteAsync(bytes, stoppingToken);

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
