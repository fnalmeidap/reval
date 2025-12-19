using System.Net.Sockets;
using Reval.Telemetry.Gateway.Ingestion.MonitorListener;
using Reval.Telemetry.Gateway.Configuration;
using Reval.Telemetry.Gateway.Hubs;
using System.Net;

// Setup configuration from .yaml file
var builder = WebApplication.CreateBuilder(args);

builder.Configuration.AddJsonFile("appsettings.json", optional: false, reloadOnChange: true);
builder.Services.AddSingleton<IConfiguration>(builder.Configuration);
builder.Services.Configure<>

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
    var endpoint = new IPEndPoint(IPAddress.Any, 5005);
    return new UdpClient(endpoint);
});
    
builder.Services.AddHostedService<MonitorListener>();

var app = builder.Build();

app.UseCors();

app.MapHub<Frame>("/framehub");

app.Run();
