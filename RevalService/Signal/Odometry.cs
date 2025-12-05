namespace Reval.Signal;

public class Odometry : ISignal
{
    /// <summary>
    /// Timestamp of the odometry data
    /// </summary>
    public DateTime Timestamp { get; set; }

    /// <summary>
    /// X position
    /// </summary>
    public float X { get; set; }

    /// <summary>
    /// Y position
    /// </summary>
    public float Y { get; set; }

    /// <summary>
    /// W position
    /// </summary>
    public float W { get; set; }
}