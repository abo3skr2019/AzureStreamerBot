using System;

public class CPHInline
{
    public bool Execute()
    {
        string varName = "Player";
        string username = args["userName"].ToString();
        string userId = args["targetUserId"].ToString();
        string usertype = args["userType"].ToString();
        if (usertype == "youtube")
        {
            CPH.SetYouTubeUserVarById(userId,varName, username, false);
        }

        if (usertype == "twitch")
        {
            CPH.SetTwitchUserVarById(userId, varName, username, false);
        }
        CPH.SendMessage($"{username} Wants to Play");
        return true;
    }
}