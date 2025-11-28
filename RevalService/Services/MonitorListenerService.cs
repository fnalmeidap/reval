using System.Net.Sockets;
using Microsoft.AspNetCore.SignalR;
using Reval.Hubs;

namespace Reval.Services.MonitorListenerService;

public class MonitorListenerService : BackgroundService
{
    private readonly ILogger<MonitorListenerService> logger;
    private readonly UdpClient monitorListener;
    private readonly IHubContext<FrameHub> hub;
    
    public MonitorListenerService(ILogger<MonitorListenerService> logger, UdpClient monitorListener, IHubContext<FrameHub> hub)
    {
        this.monitorListener = monitorListener;
        this.logger = logger;
        this.hub = hub;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            logger.LogInformation($"UDP Listener started on {monitorListener.Client.LocalEndPoint}");

        try
        {
            while (!stoppingToken.IsCancellationRequested)
            {
                try
                {
                    var result = await monitorListener.ReceiveAsync(stoppingToken);
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
            monitorListener.Close();
            logger.LogInformation("UDP Listener stopped");
        }
    }

    public override void Dispose()
    {
        monitorListener.Close();
        base.Dispose();
    }
}
