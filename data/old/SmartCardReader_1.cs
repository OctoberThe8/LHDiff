// Source - https://codereview.stackexchange.com/q
// Posted by Robert Snyder
// Retrieved 2025-11-29, License - CC BY-SA 3.0

public override bool Open()
{
    readerThread = new Thread(CardStatusChange);
  
    return true;
}

public override bool Enable()
{
    run = true;
    //thread start checking for card events
    switch (readerThread.ThreadState)
    {
        case ThreadState.AbortRequested:
            break;
        case ThreadState.Aborted:
            break;
        case ThreadState.Background:
            break;
        case ThreadState.Running:
            break;
        case ThreadState.StopRequested:
            break;
        case ThreadState.Stopped:
            break;
        case ThreadState.SuspendRequested:
            break;
        case ThreadState.Suspended:
            readerThread.Resume();//TODO remove

            break;
        case ThreadState.Unstarted:
            readerThread.Start();

            break;
        case ThreadState.WaitSleepJoin:
            break;
        default:
            break;
    }

    return true;
}
public override void Disable()
{
    run = false;
    readerThread.Suspend(); //TODO remove
}
