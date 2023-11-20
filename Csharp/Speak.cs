using System;

public class CPHInline
{
    public bool Execute()
    {
        string selchatter = CPH.GetGlobalVar<string>("FinalChatter", false);
        string userName = args["userName"].ToString();
        if (userName == selchatter)
        {
            string message = args["rawInput"].ToString();

            if(!message.StartsWith("!") || !message.Contains("Has Been Selected"))
            {
                CPH.WebsocketSend(message,0);
                return true;
            }
        }
        return false;
    }
}