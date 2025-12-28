using System.Net.Sockets;
using Reval.Telemetry.Gateway.Ingestion.MonitorListener;
using Reval.Telemetry.Gateway.Configuration;
using Reval.Telemetry.Gateway.Hubs;
using System.Net;
using Microsoft.Extensions.Options;

// Setup configuration from .yaml file
var builder = WebApplication.CreateBuilder(args);

builder.Configuration.AddJsonFile("appsettings.json", optional: false, reloadOnChange: true);
builder.Services.Configure<AppSettings>(builder.Configuration.GetSection("AppSettings"));

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

// Setup client ip/port binding from .yaml config file
builder.Services.AddSingleton(serviceProvider =>
{
    var config = serviceProvider
        .GetRequiredService<IOptions<AppSettings>>().Value;

    var endpoint = new IPEndPoint(IPAddress.Any, config.Networking.AppMonitorationPort);
    return new UdpClient(endpoint);
});
    
builder.Services.AddHostedService<MonitorListener>();

var app = builder.Build();

app.UseCors();

app.MapHub<Frame>("/framehub");

app.Run();
