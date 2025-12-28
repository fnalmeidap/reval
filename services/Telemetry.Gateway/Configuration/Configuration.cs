namespace Reval.Telemetry.Gateway.Configuration;

public sealed class NetworkSettings
{
    public required int AppMonitorationPort { get; set; }
}

public sealed class ChannelSettings
{
    public required int Capacity { get; set; }
    public required bool SingleReader { get; set; }
    public required bool SingleWriter { get; set; }
}

public sealed class LokiSettings
{
    public required string Route { get; set; }
    public required string Endpoint { get; set; }
}

public sealed class AppSettings
{
    public required string AppName { get; set; }
    public required string Version { get; set; }
    public required NetworkSettings NetworkSettings { get; set; }
    public required ChannelSettings ChannelSettings { get; set; }
    public required LokiSettings LokiSettings { get; set; }
}