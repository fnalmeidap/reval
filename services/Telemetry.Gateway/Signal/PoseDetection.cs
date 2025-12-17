namespace Reval.Telemetry.Gateway.Signal;

public class PoseDetection : ISignal
{
    /// <summary>
    /// Timestamp of when the pose was detected
    /// </summary>
    public DateTime Timestamp { get; set; }

    // TODO: Define properties relevant to pose detection
}
