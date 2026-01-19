using System.Net.Sockets;
using System.Threading.Channels;
using Reval.Telemetry.Gateway.Ingestion.MonitorListener;
using Reval.Telemetry.Gateway.Configuration;
using Reval.Telemetry.Gateway.Hubs;
using System.Net;
using Microsoft.Extensions.Options;
using Reval.Telemetry.Gateway.Ingestion.MonitorDispatcher;
using Reval.Telemetry.Gateway.Observability.Loki;

// Setup configuration from .yaml file
var builder = WebApplication.CreateBuilder(args);

builder.Configuration.AddJsonFile("appsettings.json", optional: false, reloadOnChange: true);
builder.Services.Configure<AppSettings>(builder.Configuration.GetSection("AppSettings"));
builder.Services.Configure<LokiSettings>(
    builder.Configuration.GetSection("AppSettings:LokiSettings"));

builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>  
        policy
            .AllowAnyHeader()
            .AllowAnyMethod()
            .AllowCredentials()
            .SetIsOriginAllowed(_ => true)
    );
});

builder.Services.AddSignalR()
    .AddMessagePackProtocol();

builder.Services.AddSingleton(serviceProvider =>
{
    var config = serviceProvider
        .GetRequiredService<IOptions<AppSettings>>().Value;

    return Channel.CreateBounded<byte[]>(new BoundedChannelOptions(config.ChannelSettings.Capacity)
    {
        SingleReader = config.ChannelSettings.SingleReader,
        SingleWriter = config.ChannelSettings.SingleWriter,
        FullMode = BoundedChannelFullMode.DropOldest
    });
});

builder.Services.AddSingleton(serviceProvider =>
{
    var config = serviceProvider
        .GetRequiredService<IOptions<AppSettings>>().Value;

    var endpoint = new IPEndPoint(IPAddress.Any, 1234);
    return new UdpClient(endpoint);
});

builder.Services.AddHttpClient<ILokiClient, LokiClient>((serviceProvider, client) =>
{
    var config = serviceProvider
        .GetRequiredService<IOptions<LokiSettings>>().Value;
    
    client.BaseAddress = new Uri(config.Endpoint);
});
    
builder.Services.AddHostedService<MonitorListener>();
builder.Services.AddHostedService<MonitorDispatcherService>();

var app = builder.Build();

app.UseCors();

app.MapHub<Frame>("/framehub");

app.Run();
