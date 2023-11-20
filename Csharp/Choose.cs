using System;
using System.Collections.Generic;

public class CPHInline
{
    public bool Execute()
    {
        // your main code goes here
        Random rnd = new Random();
        CPH.LogInfo("random number generated");
        string varName = "Player";
        UserVariableValue<string> TwitchPlayerValue = null;
        UserVariableValue<string> YTPlayerValue = null;
        try
        {
            List<UserVariableValue<string>> TTVUserVARL = CPH.GetTwitchUsersVar<string>(varName, false);
            CPH.LogInfo("var Twitchlistlist generated");
            int numberofttvplayers = TTVUserVARL.Count;
            CPH.LogInfo("Twitchlist count generated");
            int SelectedttvPlayer = rnd.Next(numberofttvplayers);
            CPH.LogInfo("selected Twitch player generated");
            TwitchPlayerValue = TTVUserVARL[SelectedttvPlayer];
            CPH.LogInfo("Twitch player value generated");
        }
        catch (System.ArgumentOutOfRangeException ex)
        {
            CPH.LogInfo("An error occurred at twitch list gen: " + ex.Message);
        }
        
        try
        {
            List<UserVariableValue<string>> YTUserVARL = CPH.GetYouTubeUsersVar<string>(varName, false);
            CPH.LogInfo("var YTlistlist generated");
            int numberofyt = YTUserVARL.Count;
            CPH.LogInfo("YTlist count generated");
            int SelectedYTPlayer = rnd.Next(numberofyt);
            CPH.LogInfo("selected YT player generated");
            YTPlayerValue = YTUserVARL[SelectedYTPlayer];
            CPH.LogInfo("YT player value generated");

        }
        catch (System.ArgumentOutOfRangeException ex)
        {
            CPH.LogInfo("An error occurred at YT list gen: " + ex.Message);
        }
        UserVariableValue<string> FinalPlayer;
        CPH.LogInfo("Final player value Initialized");
        int Flip = rnd.Next(10);
        if (Flip < 5 && YTPlayerValue != null)
            {
                FinalPlayer = YTPlayerValue;
                CPH.LogInfo("YT Player Selected");
            }
        else if (TwitchPlayerValue != null)
            {
                FinalPlayer = TwitchPlayerValue;
                CPH.LogInfo("TTV Player Selected");
            }
        else
        {
            CPH.LogInfo("Both YTPlayerValue and TwitchPlayerValue are null");
            // Handle the case when both YTPlayerValue and TwitchPlayerValue are null
            // For example, you might want to return from the function:
            return false;
        }
        string finaluser = FinalPlayer.UserName;
        CPH.SetGlobalVar("FinalChatter",finaluser, false);
        string FinalChatter = CPH.GetGlobalVar<string>("FinalChatter", false);
        CPH.LogInfo($"Final Send Final Chatter = {FinalChatter} + {finaluser}");
        CPH.SendMessage($"{finaluser} Has Been Selected");
        return true;
    }
}