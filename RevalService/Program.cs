using System.Net.Sockets;
using Reval.Services.MonitorListenerService;
using Reval.Message;
using Reval.Hubs;
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
    var endpoint = new IPEndPoint(IPAddress.Any, 5005); // 0.0.0.0
    return new UdpClient(endpoint);
});
    
builder.Services.AddHostedService<MonitorListenerService>();

var app = builder.Build();

app.UseCors();

app.MapHub<FrameHub>("/framehub");

app.Run();
