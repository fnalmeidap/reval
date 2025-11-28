using System.Collections.Concurrent;

namespace Reval.Message;

public class MessageStore
{
    private readonly ConcurrentQueue<string> _messages = new();
    private const int MaxMessages = 100;

    public void AddMessage(string message)
    {
        _messages.Enqueue(message);
        // Keep only the last 100 messages
        while (_messages.Count > MaxMessages)
        {
            _messages.TryDequeue(out _);
        }
    }

    public List<string> GetMessages()
    {
        return _messages.Reverse().ToList();
    }
}