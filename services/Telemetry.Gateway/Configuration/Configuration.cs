namespace Reval.Telemetry.Gateway.Configuration;

public sealed class Networking
{
    public required int AppMonitorationPort { get; set; }
}

public sealed class Configuration
{
    public required string AppName { get; set; }
    public required string Version { get; set; }
    public required Networking Networking { get; set; }
}