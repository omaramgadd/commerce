# Sporty

Sporty is a web application that shows the Spanish league (La Liga) soccer fixtures and scores, you can see the match details such as live events and scores, the stats of the games, and also the whole league standings.   
You can create an account to star your favorite games.  
You can star any game you like and save it into your starred games.  
You can open any specific club and see its matches only. 
the application uses [sport data api](https://app.sportdataapi.com/)

## Distinctiveness and Complexity

### Distinctiveness
This project is a sports application that is completely different from all the other projects in the course and also different from the old pizza project.
### Framework
The project uses Django on the backend and Javascript on the frontend and more than one model in the DataBase.
### Mobile responsive
I have made the application mobile responsive so that it fits any mobile or tablet screen.  
The navigation bar also is compressed to the 3 dashes on the top right when it is used on the mobile. 
  
  
## Static Files

### sporty.js
This file contains the javascript for the front end, we'll go through each function
* **weekcontrol** function : when you press next or previous on the main page to change the week by
* **open_match** functinon : opens the match page when you press on it by taking the match id and making a request to the API
* **change section** function : changes between the 3 sections on the match page which are stats, match events, and the league standings by changing the style and showing only the selected section
* **open_club** function : inside the match page, when you press on the logo of the team it takes you to a page where you can see only this club's scores and fixtures
* **starry function** : this function is used to add a match to your starred games page and it also changes the star icon when you star or unstar the match

### styles.css

This page contains all the styling for the web application

### matchevents.txt

A demo responsive of the [api](https://app.sportdataapi.com/) that I am using

### PNGs

2 png's for the yellow and the red card

## Templates files

### login.html and register.html

Takes user name, email, and password when registering.  
Takes only the user name and password when logging in. 

### layout.html

contains the navigation bar which is collapsable if the screen is smaller than a certain width to be mobile responsive.  

### matchweek.html

shows the main page which has matches of the current week and you can go to the previous or the next week by pressing the next or previous buttons beside the date.  
shows the matches of this week and their dates, and matches on the same day are grouped.  
shows the time of the match if it didn't start yet but if it did start it will show the live score of the match.

### match.html

at the top, it shows time, date, and score, it also shows the star icon which you can press to add this game to your favorite games.  
then you can see 3 selectable sections
* match events: shows the goals scored, substitutions ( green is the player going in and red is the player going out ), yellow cards, and red cards.
* match stats: shows general stats of the game like shots and possession percentage.         
* standings: shows the current standings of the league.  
  * MP means total matches played 
  * w:d:l is won, draws, and lost games 
  * F: A is goals for and goals against the whole season
  * +/- is the goals difference ( between goals for and goals against)
  * PTS is the total points that each team has. the win gives you 3 points, a draw gives you 1 and losing gives you nothing


### club.html

when you press on the logo of any club inside the match details page it opens a page with only fixtures and results belonging to this club only, it has the same interface as the home page (matchweek.html)

### starred.html

it has all the starred games for the current user and it has the same interface as the home page (matchweek.html)

## Python files

### views.py

* **home view**: home view which calls the home page it used, it is called by ajax if the previous (p) or next (n) week button was pressed and depending on the direction it changes the date and returns a page with matches in those dates using **request_games** function
* **match view**: renders match page and provides single match information
* **starred view**: renders the starred games page, and it can be called with ajax to add or remove games from the user's starred games which are stored in the database
* **club_matches view**: renders the page for single club matches

### models.py

* **club model**: stores club id, club logo, and club name
* **star model**: stores starred games for each user

## How to run

* Open the match by clicking on the matchbox.
* Star or unstar the game by clicking on the star icon.
* inside the match page, you can press on the logo to open the club's matches.
* Starred games, login, and logout are in the navigation bar.























