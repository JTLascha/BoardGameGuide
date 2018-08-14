Hello!

This is simple program that can help you pick which board game to play next out of your giant collection to introduce to your group.
The data for the board games is included in a file named "games.txt" This is hardcoded, so you need to have that exact file in your directory.

The format for data entry in games.txt is:
Game Name, BGG Rank, Complexity, BGGRating, Language - Comma delimted list of categories --0

As it is at the moment, BGG Rank and Rating are unused, as is the list for partial categories, which is why I left that part blank here.

The 0 at the end means that your group does not know this game yet. If they do know the game, put a 1 there instead.

Start the program by typing "python3 analysis.py" in the command line.

"Language" refers to how well you need to speak English to play. I made this program for a friend who is still learning English, so I made it so the plan function prioritizes games with lower language values. I used a scale of 0 -3, 
based on BGG's information.


The plan function is the main appeal to this for me. It will put your games in the order it thinks you should introduce them to your group, and it will tell you which mechanics in that game are new and which ones are familiar.

Compare is another useful one. It compares the selected game with all the other games to help show you which games you own are most like it. My girlfriend liked this, as it helped her to see what it was about her favorite games 
specifically that she likes.


Have fun teaching games to your friends!
