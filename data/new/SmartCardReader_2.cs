// Source - https://codereview.stackexchange.com/a
// Posted by Robert Snyder
// Retrieved 2025-11-29, License - CC BY-SA 3.0

public override bool Open()
{
    

    readerThread = new Thread(CardStatusChange);
    readerThread.IsBackground = true;

    return true;
}
public override bool Enable()
{
    run = true;
    //thread start checking for card events
    Globals.tracer.TraceInformation("Checking Thread State:{0}", readerThread.ThreadState);
    var startable = (readerThread.ThreadState & ThreadState.Unstarted);
    if (startable > 0)
        readerThread.Start();

    return true;
}
public override void Disable()
{
    run = false;
    if(readerThread.ThreadState == ThreadState.Unstarted)
        readerThread.Join();
}
