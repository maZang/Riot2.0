# Riot2.0

This data analysis attempts to analyze how the champs interact individually and together as a team in the game mode 
Black Market Brawlers in the game League of Legends by Riot Games. Using Riot's API to fetch many games of data,
then analyzing the data into 8 categories with K-Means clustering (a simple machine learning algorithm based upon
Euclidean distances), we serve to analyze how different champs perform in different roles.

The roles are based upon the total overall stat gain of the champion (items and runes), masteries used, as well as 
other game statistics such as creep score and gold earned and summoner spells. To make sure the order of the
summoner spells did not matter, we combined features (summonerspell1 + summonerspell2 and summonerspell1 * 
summonerspell2) to introduce symmetry to keep features consistent.After getting the K-means parameters, 
the data set wasanalyzed again focusing on each individual game. As we fetched data, we also got pretty important
data such as team synergies. To do this we focused on getting the winrate of the champions individually then 
compared the win rate of the two champions together. We used a weighted winrate system. For example, if Jinx's
individual winrate was 52% and Bard's was 40%, and together their winrate is 51%, this is treated as positive 
synergy because Bard's winrate shot up much higher than Jinx was lowered. Of course this new winrate took into
account number of games played, weighing in favor of more games.

We compiled the data into a website using mainly HTML, CSS, and JS (using AngularJS for the majority of the site,
and some additional packages such as D3 for the pie graph). We also borroed some open source autocomplete code.
Credits goes to JustGoscha at http://justgoscha.github.io/allmighty-autocomplete/.

Thanks for viewing our site and hope you enjoyed your stay. Thank you and come again.

Note: Gangplank was not in the game mode, but since the page was created using AngularJS, his page can still be 
found although it is meaningless.
