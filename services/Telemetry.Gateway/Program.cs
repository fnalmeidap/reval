using System.Net.Sockets;
using Reval.Telemetry.Gateway.Ingestion.MonitorListener;
using Reval.Telemetry.Gateway.Hubs;
using System.Net;

var builder = WebApplication.CreateBuilder(args);

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
    var endpoint = new IPEndPoint(IPAddress.Any, 5005);
    return new UdpClient(endpoint);
});
    
builder.Services.AddHostedService<MonitorListener>();

var app = builder.Build();

app.UseCors();

app.MapHub<Frame>("/framehub");

app.Run();
