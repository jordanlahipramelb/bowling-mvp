# Schema & API Feedback

### Users/Bowlers
The main considerations you want here are functional and also ensuring that when you build the UI it can be more graphical/visual to enhance the _shininess_ of your app.

 - Consider adding an email address for registration; this will allow you to do a lot more in the long term - email notifications, password resets, etc.
 - Consider adding a profile pic image URL and/or an avatar selection/URL.
 - Consider adding a league string, team string to add other stuff about the bowler. If you were building league support, you would need full tables for these kinds of things, but for your MVP a simple string field will be fine.

 ### Bowlers_Scores and scorecards

 I think this is a good idea, but I'm having trouble understanding the relationship between bowlers_scores and scorecards. It looks to me like it is essentially a 1:1.
 So you could take two approaches to this, you could either have a bowler scorecard that combines the fields of both tables, or you could make frames its own table to get away from the frame_1_1 etc. approach you had to take.
 **Definitely** what you want to do is ensure that null can be entered in the frame pin fields - we want to be able to differentiate whether a user had a gutter ball vs. they haven't entered the data in yet. What is frame_0 about? Are you planning on storing which frame the user is currently on or has entered last?

### A potential approach:
Table: Bowler 

Table: BowlerGame (Scorecard + Date + location)
Frame 1_1, Frame 2_2 or below GameFrame solution
Total Score field * a must if using GameFrame solution

Table: BowlerGameFrame (a potential approach)
   BowlerGame_id : foreign key to bowler game
   Frame Number : 1
   Ball Number : 1 or 2
   PinsDown : 3 ? 3 pins knocked down 0 ? gutterball null ? => not entered yet
   IsStrike bool
   IsSpare bool

**Later, if you want to work on above as MVP first**
Table: BowlerGameFramePinDown
   BowlerGameFrame_id : foreign key to bowler game frame
   Pin Number : 1-10

Insert N number of records for the corresponding pins knocked down


When calculating total score and displaying on UX:
foreach through the game frames and display UX based on Frame Number + Ball Number


### MapQuest API usage

I think this is a really good choice. I was able to use it pretty easily with the swagger. I think you'll want to think about what happens when you can't use the browser's location etc (set a default location etc.)