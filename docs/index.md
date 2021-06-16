





## LAMAS Project --- BoerenBridge

By Daan Krol (s3142221),
Jeroen van Brandenburg (s3193063), and
Julian Bruinsma (s3215601)

### Introduction
<!-- Ook een soort van abstract -->

In this project, we are going to analyze the application of Kripke knowledge in the Dutch game called _Boeren Bridge_. It is a card game played with four players, in which the objective is to obtain the most points, by correctly guessing the amount of tricks the player himself will take. We created agents which use playing strategies based on Kripke models, which are updated during the game with Public Announcement Logic. In this project we are testing the performance of agents that use Kripke knowlegde and compare it with agents that use simple tactics that are not based on Kripke knowledge.

[This](https://github.com/JeroenVanB/LAMAS) is the link to our github repository.


##### TODO Research question/Wat gaan we onderzoeken/testen (moet dit bij experiments als extra?)
### Game Rules

#### Variations

There are many variants of the game: 'Oh hell!', 'Wizard' or 'Nomination Whist'. We decided to implement a version, which we ourselves usually play. To prevent state explosion, we simplified some game rules, e.g. the amount of cards. We implemented a version with 5 rounds and only the highest cards of the normal deck of cards are used. The trump changes each round and is chosen randomly.

#### Points

The aim of the game is to get the most points. Points can be obtained by winning tricks and (most importantly) correctly guessing how many tricks the player himself will take in a round.
If the player correctly guesses the total number of tricks he has taken, he will receive two points for each trick taken, with a 10 points bonus. 
If the player guesses wrong, he will get two points subtracted for each trick he was off. The player with the most points after 15 rounds wins the game.

#### Gameplay

In each round, each player is given _n_ cards. From a separate set of cards, one random card is picked to determine the trump of the round. Starting by the player to the left of the dealer _P<sub>1</sub>_ and continuing clockwise, every player _P_ ∈ \{_P<sub>1</sub>_, _P<sub>2</sub>_, _P<sub>3</sub>_, _P<sub>4</sub>_\} guesses the number of tricks he will win. (In the rare occasion that all the guesses sum up to _n_, the dealer has to change his guess. He has to increase or decrease his original guess with 1 such that the total is not a sum equal to _n_.)

Next, _t_ = _n_ tricks are played, in which each player plays one card. During the first trick _t_<sub>1</sub>, the player left of the dealer starts. In the following rounds, the winner of the previous trick starts. The starting player is called _the opener_. Every player after the opener, should play a card matching the suit of the card played by the opener. If this is not possible, the player may play any card of his choice.

#### Winning tricks

The player who played the highest card during a trick, takes the trick. The cards follow the usual order, where 2 is the lowest and Ace is the highest (2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace). When a player plays a card of a different suit than the opener, it is considered the lowest and can never win. Trump cards, however, are always higher than the other cards.

#### Number of cards

The number of cards depend on the number of rounds. The number of rounds can is determined by the players beforehand. We chose to play 5 rounds.
In every round _r_, the players is dealt _t<sub>r</sub>_ cards. First, starting in the first round with _t<sub>1</sub>_ = 3. In each following round, every player is given _t<sub>r</sub>_ = _t<sub>r-1</sub>_+1 cards, up to 5 cards in total (in round 3). Then, starting with 2 more rounds are played, where the amount of cards decreases by 1. The game ends after round 5, where \_n<sub>5</sub>=3. See the table below for clarification.
To decrease the possible states, we minimized the amount of cards used in the game. This way it is known which cards are in the game and which are not. E.g. in round 1, only the (Queen, King, Ace) of all the suits are used. This is also clarified in the table below.

##### Table 1

<!-- | Round  | Number of cards  | Cards                      |
| ------ | ---------------- | -------------------------- |
| 1      | 3                | Queen, King, Ace           |
| 2      | 4                | Jack, Queen, King, Ace     |
| 3      | 5                | 10, Jack, Queen, King, Ace |
| 4      | 4                | Jack, Queen, King, Ace     |
| 5      | 3                | Queen, King, Ace           | -->

<table style="width:100%">
<caption>Table 1: Number of cards in each round.</caption>
  <tr>
    <th>Round</th>
    <th>Number of cards</th>
    <th>Cards</th>
  </tr>
  <tr>
    <td>1</td>
    <td>3</td>
    <td>Queen, King, Ace</td>
  </tr>
  <tr>
    <td>2</td>
    <td>4</td>
    <td>Jack, Queen, King, Ace</td>
  </tr>
  <tr>
    <td>3</td>
    <td>5</td>
    <td>10, Jack, Queen, King, Ace</td>
  </tr>
  <tr>
    <td>4</td>
    <td>4</td>
    <td>Jack, Queen, King, Ace</td>
  </tr>
  <tr>
    <td>5</td>
    <td>3</td>
    <td>Queen, King, Ace</td>
  </tr>
</table>

### Formalization

Every time a player plays a card, he makes an announcement. By using Public Announcement Logic (PAL), we can reduce the amount of possible states in the Kripke models. By using PAL, we can increase the common knowledge in the game. Since the announcements are always true, and contain information that all the players can use, it can be used to update the Kripke models of all players. The announced knowledge has thus become common knowledge. The announcements give more information about the real world and therefore result in a decreased number of relations between possible states. This can eliminate the possibilities of players having certain cards. Therefore, an announcement can result in common knowledge. For a more formal proof of the relation between PAL and common knowledge we refer to the book by _Dynamic Epistemic Logic_ by _Hans van Ditmarsch_. 

To formalize the model we use the following notation: _x_S_r_, where _x_ ∈ \{N, E, S, W\} which are the players, _S_ ∈ \{C, SP, H, D\} and _r_ ∈ \{A, K, Q, J, 10\}. This indicates that player _x_ has (and plays) a card with suit _S_ and rank _r_.

The full names and used abbreviations of the players, suits and ranks can be found in the tables 1, 2, and 3, respectively. 

<table style="width:100%">
<caption>Table 3: Player names.</caption>
  <tr>
    <th>Name</th>
    <th>Abbreviation</th>
  </tr>
  <tr>
    <td>North</td>
    <td>N</td>
  </tr>
  <tr>
    <td>East</td>
    <td>E</td>
  </tr>
  <tr>
    <td>South</td>
    <td>S</td>
  </tr>
</table>

<table style="width:100%">
<caption>Table 4: Suits.</caption>
  <tr>
    <th>Name</th>
    <th>Abbreviation</th>
  <tr>
    <td>West</td>
    <td>W</td>
  </tr>
  <tr>
    <td>Clubs</td>
    <td>C</td>
  </tr>
    <tr>
    <td>Spades</td>
    <td>SP</td>
  </tr>
    <tr>
    <td>Hearts</td>
    <td>H</td>
  </tr>
    <tr>
    <td>Diamonds</td>
    <td>D</td>
</table>
  
<table style="width:100%">
<caption>Table 5: Ranks. </caption>
  <tr>
    <th>Name</th>
    <th>Abbreviation</th>
  </tr>
    <tr>
    <td>Ace</td>
    <td>A</td>
  </tr>
    <tr>
    <td>King</td>
    <td>K</td>
  </tr>
    <tr>
    <td>Queen</td>
    <td>Q</td>
  </tr>
    <tr>
    <td>Jack</td>
    <td>J</td>
  </tr>
  </tr>
    <tr>
    <td>10</td>
    <td>10</td>
  </tr>
</table>

##### Example 1 - Announcement 'Played card'

If player North plays the Ace of Spades, no one else can hold that card. Therefore, the Kripke model of the Ace of Spades can be updated. All players only have a relation from the real world, to the real world (in which North is the owner of the Ace of Spades). After the update it is common knowledge that no one has that specific card anymore.
the public announcement changes the common knowledge as follows:

<img src="announcement_plays_card.png" alt="Formal definition of the announcement 'Played card'">

##### Example 2 - Announcement 'Does not have suit'

Consider the Kripke model of the Queen of Hearts. Player South does not hold the Queen of Hearts. Player North is the opener and starts the trick by playing the 10 of Hearts. Player East plays the Jack of Clubs. If Player East had a card of the Hearts suit (the trick suit), he was obligated to play it. Since he did not, player South now knows, that he does not have the Queen of Hearts and therefore has no Hearts suit at all. Therefore, every Player can update their knowledge on the cards that Player East holds. It is now common knowledge that Player East does not hold a card with suit Hearts.
In formal, the public announcement changes the common knowledge as follows:

<img src="announcement_has_no_suit.png" alt="Formal definition of the announcement 'Does not have suit'" width="400">


### Game implementation

The game is made in Python with [Pygame](https://www.pygame.org/), using a MVC pattern and an object oriented approach. In the GameModel class, all the logic of the game is handled. The classes _Player_, _Deck_ and _Card_ facilitate an easy implementation of the logic.

##### Card Class

An instance of the Card Class represents a card, by keeping track of the rank, suit, owner and the value. The base value is determined by the rank, as shown in Table 2. When a card is played, the value is influenced by the trump and trick suit. When a card has the same suit as the trick suit, its value is increased by 13. When a card has the same suit as the trump, its value is increased by 26.

<table style="width:100%">
<caption>Table 2: Value of each rach. </caption>
  <tr>
    <th>Rank</th>
    <th>Value</th>
  </tr>
  <tr>
    <td>Two</td>
    <td>0</td>
  </tr>
  <tr>
    <td>Three</td>
    <td>1</td>
  </tr>
  <tr>
    <td>Four</td>
    <td>2</td>
  </tr>
  <tr>
    <td>Five</td>
    <td>3</td>
  </tr>
  <tr>
    <td>Six</td>
    <td>4</td>
  </tr>
    <tr>
    <td>Seven</td>
    <td>5</td>
  </tr>
    <tr>
    <td>Eight</td>
    <td>6</td>
  </tr>
    <tr>
    <td>Nine</td>
    <td>7</td>
  </tr>
    <tr>
    <td>Ten</td>
    <td>8</td>
  </tr>
    <tr>
    <td>Jack</td>
    <td>9</td>
  </tr>
    <tr>
    <td>Queen</td>
    <td>10</td>
  </tr>
    <tr>
    <td>King</td>
    <td>11</td>
  </tr>
    <tr>
    <td>Ace</td>
    <td>12</td>
  </tr>
</table>

##### Deck Class

During the game only one instance of the Deck class is present. It keeps track of all the cards in the game. The amount of cards in the deck depends on the round, as explained in the section Game Rules.

##### Player Class

The player class is an abstract class in which some basic functions are defined, such as _calculate\_score()_ and _play\_card()_. Many other functions consider finding a specific card of the player e.g. _get_highest\_card()_ and _get\_lowest\_card\_of\_suit()_. These functions are defined here, since they can be used in different types of tactics.
The abstract class _Player_ is extended by different types of agents. The subclasses override the function _pick\_card()_ and _guess\_wins()_, in which the tactics are implemented. This way, we created two simple agents called the _RandomAgent_ (RA), which plays random cards, and the _GreedyAgent_ (GA), which plays the highest cards. The two subclasses that we mainly focussed on are the _GreedyKripkeAgent_ (GKA) and _FullKripkeAgent_ (FKA). These both make use of a Kripke model, to determine which cards to play. The GKA always tries to win a trick, using a set of rules based on a Kripke model. If a GKA has already won as much games, as he guessed, he will play a random card. The FKA also uses the same tactics as the GKA to win tricks, but also has a losing strategy. These exact rules of these strategies explained below in the section 'Strategy'.
##### GameModel Class

The GameModel contains all the variables and functions to run the game. The function _next\_move()_ keeps being executed in the main loop. It determines whose turn it is and checks if a trick, round or game should start or end. It also lets the current player make a move.
At the start of each round, the cards are dealt, a trump is chosen en the _opener_ is determined. In the next four steps, each player plays a card, which is added to the dictionary _table_. After the last player, _determine\_winner()_ checks who played the winning card. That player becomes the new _opener_. After all the tricks of a round are finished, the points are calculated for each player. After the final round, the game ends.

##### Knowledge_base class
The _KnowledgeBase_ class is constructed to represent the knowledge of every player during the game.  It initizales the knowledge base by considering it possible that every other player has a card _unless_ it has the card itself. This is done by the function _knowledge\_of\_remaining\_cards\_in\_deck()_. To set the knowledge of the player itself, the function _set\_knowledge\_of\_own\_hand()_ is used. The function _remove\_card_ is used to remove a card from the the knowledge base of the player if the card is played by another player. The belief about the cards in the game are also determined using the functions _get\_highest\_card\_of\_suit()_ and _get\_highest\_non\_trump\_cards()_ that return the highest card of a suit and the highest trump card that are currently in the game, respectively. 
The knowledge base also contains the belief about which cards are in the game and what player might have a certain card. Using the function _other\_players\_have\_suit()_ it is determined if another player might also have the suit that you want to play. The function _player\_might\_have\_suit()_ determines the belief of a player that other players might have a card of a certain suit. 


##### TODO: Announcement class (and how the announcements are used to update the kripke model)
To use PAL in the game model, a _PublicAnnouncement_ class is created. If a player plays a card or cannot follow suit, he sends an announcement to all the other players in the game, which then update the corresponding Kripke model. If a player receives the announcement 'card\_played', the player now does no longer consider that the other players have the card. The worlds and relations are updated accordingly to reflect this change. In the Kripke Model Viewer we show the Kripke models for a card for all players.
<!--  Hier even mooi plaatje in zetten -->

<p float="left">
  <img src="knowledge_before_announcement.png" width="100" />
  <img src="game_UI.png" width="100" />
</p>


he removes all the relations in the Kripke model of that card. Since the card has been played, the players should not consider it possible for another player to have the card. If a player receives the announcement 'does\_not\_have\_suit', the Kripke models are updated by removing the relations of the sender in the Kripke models of all possible cards of the trick suit.

#FIXME: kan denk ik wel duidelijker. ook even methods erbij denk ik #FIXME 2: Mss afbeeldingen erbij van hoe het geupdate wordt?

### Visualization

To visualize the game and the Kripke models a UI class is constructed. The UI is made using Pygame which enables you to draw basic shapes such as rectangles, lines and text to positions on the screen. Cards are visualized by showing their images on the screen. In the image below you can see the full visualization of the game and Kripke model.

![Visualization of the game and Kripke models](game_UI.png)

#### Game UI

The left hand side of the UI shows the game information such as the current round, scores, trump and trick suits. For each player we show his hand to the user. Do note that the cards are of course not visible to the players in the game. They have to rely on their knowledge about the game. At the center of the table you can see all players guesses and how many rounds they have actually won until now. The game will be paused after each move so that the user has the time to observe all game and model changes. When the user presses the spacebar the game will continue to the next move of the current player. The player, game and model states will be updated internally. The UI class is notified that there is a change and it will redraw all game elements on the left hand side of the screen.

#### Message box

To give the user a better overview of what is happening in the game and models we added a status box at the bottom. This box shows messages such as who's turn it is to play, what the trump is for this round or what the current trick suit is. All public announcements can be observed here so that the user has a better understanding of the changes to the Kripke models. In the image above you can find that player West had to change it's guess since it is not allowed for the sum of guess to be equal to the amount of tricks in the game.

#### Kripke Model Viewer

The right hand side of the screen shows an interactive Kripke Model viewer. The screen is continuously redrawn so that we can make use of buttons to redraw parts of the viewer but also to make it independent of the game loop. The user can use the suit and rank buttons to select a card in the current game. The Kripke Model of that card is then visualized above the buttons. The model shows the knowledge of the current card.
<img src="kripke_model_viewer.png" alt="Kripke Model Viewer">

In the image above the Kripke Model of the Queen of Hearts is visualized. The true world is shown by a golden box. Possible world relations are represented by colored lines where each color represents a player. Here, Player West has the card in its hand and thus only considers the true world possible so there is no line being drawn. All other players consider it possible that all other players have the card except for the player himself.

As this is a S5 model, it is known that there is a reflexive relation between the worlds and themselves. However, we chose to remove the reflexive relations to increase clarity in the kripke model. To indicate the reflexive relation of the true world, i.e. the world where the player who holds the card knows that he holds the card, we highlight the box of that world.

Observe the following example of a game:
![Example of only one possible world](one_world.png)
North has just opened the game and a public announcement is made that he played the Ace of Diamonds. It is now common knowledge that North has/had the Ace of Diamonds. On the right we find the Kripke model of this card. Since there is only one possible word, the true world, we remove all other worlds.

<!--
### Kripke implementation

We build an agent that determines which card to play, based on Kripke knowledge. For every card in the game, the agent has a Kripke model with four different states. Each of the states correspond to one of the four players holding the card. Each of the agents have a set of relations between the possible states. We visualize the Kripke models using a graphical representation next to the game UI. A screenshot can be seen in figure 1.

<img src="kripke_model.png" alt="Example of the Kripke models"> -->



### Strategy

##### Playing cards

The Greedy Kripke Agent and Full Kripke Agent use the Kripke models to determine which card to play. The GKA is greedy, since he only has a strategy to win a trick. Since a good strategy can become very complex (especially in a programming language), the rules are also presented in the win-graph below (made with draw.io).

[![](greedy_kripke.jpg)Rules for winning using a kripke model](greedy_kripke.jpg)

The FKA extends the GKA, by also using applying moves based on strategy to deliberatly lose tricks when the guessed wins are already reached. The strategy for losing is also presended in the lose-graph.
TODO mention that the lose-graph does not yet make use of kripke knowledge. This can be done in the future (ref to possible extensions)

[![](kripke_graph_lose.jpg)Rules for losing using a kripke model](kripke_graph_lose.jpg)

Examples of applied strategies:

- When a player is the opener, playing the highest trump card will always win the trick (GKA/FKA)

  This strategy is implemented in the win-graph in the following path: 
  - Is he the opener? -> Yes
  - Do the others still have trump cards? -> Yes
  - Does he have the highest trump card? -> Yes
  - Play the highest trump card

  The question 'Do the others till have trump cards?' can be answered by using the kripke models. If the player considers it possible that one of the players owns a trump card, the answer to the question is yes. In other rounds trump cards can be used to 'steal' tricks from the player that played the highest (non trump) trick suit card. Therefore, opening with the highest trump card is a good habit, which forces the other players to play their trump cards. This way, the opener will remain the opener in the next round, in which stealing tricks is less likely (since there are less trump cards in the game).

- When a player knows that he has the highest card of the trick suit, playing that card will often win the trick (GKA/FKA)

  This strategy is implemented in the win-graph in the following path: 
  - Is he the opener? -> No
  - Does he have trick suit? -> Yes
  - Did someone play a trump card? - No
  - Does he have the highest trick suit card? -> Yes
  - Play the highest trick suit card

  The agent has to make assumptions about the game in order to play a good strategy. In the win-graph one of the questions is "Does he have the highest trick suit card?". Using his knowledge about all possible trick cards in the game, the agent can make the right move. However, it is not always certain if the other players still have trick suit cards. If they don't, they might use a trump card to win the trick anyway. This shows that our graph is not certain of leading to a win, but we believe it definitely has a high chance of doing so.


- A player already has reached his guessed wins, so he wants to lose tricks. In a trick, another player played a trump card. He does have the highest trick suit card in the game, so he plays it. (FKA)
  This strategy is implemented in the lose-graph in the following path:
  - Is he the opener? -> No
  - Does he have trick suit? -> Yes
  - Did someone play a trump card? -> Yes
  - Play the highest trick suit card

  The player wants to lose all following tricks, since he has already reached his goal. High (non-trump) cards are likely to win tricks. It is difficult to lose tricks with them. Therefore, it is a good habit to play them when someone else has played a trump card.

Unfortunately, the lose-gaph does not use make use of Kripke knowledge. The graph was heuristically created to optimize the play of the agent. We did think of some exceptional rules that do take the Kripke knowledge into account, but these situations are very rare. An example is explained in the section 'Possible Extensions'

##### Guessing

The guessing is a very important part of the game. Since tactical guessing results in rather complex behavior we heuristically determined two simple approaches. The RandomAgent randomly guesses a number between 0 and the amount of tricks. All the other agents use a system in which uses a the average mean of the cards (_mean\_value\_hand_) in the hand is compared to the mean value of all the cards in the game (_mean\_value\_game_). These values are calculated using the function _pre\_evaluate()_ in the Card class, which take the trump into account (but ignores the trick suit, since there is none). If the _mean\_value\_hand_ is less than 90% of _mean\_value\_game_, the player guesses 0 tricks. If it is between 90% and 110% of _mean\_value\_game_, the player guesses he will win 1 trick. Between 110% and 130%, he guesses 2 tricks. For more than 130%, the player guesses to win all tricks, which is 4. This method uses all the available knowledge at the start of the game: which cards the player has and which other cards are in the game.


### Experiments
TODO
To test the performance of the four different agents (Random, Greedy, GreedyKripke, FullKripke), they all played against eachother. The performance is averaged over 100.000 games.



### TODO: Results

### Discussion


- GKA is very similar to Greedy (Almost always plays high cards)
The GreedyKripkeAgent performs very similar to the GreedyAgent. This can be explained by the fact that there play style is very similar. They guess their wins using the same strategy and if they do not want to win a trick, they both play a random card. They only differ in their playing style when trying to win tricks. The GKA uses Kripke knowledge, where the GA always plays the highest card. However, the strategy of GKA often leads to playing the highest card, which results in similar play.

- We only play with few cards
In our experiments we play 5 different rounds, with a maximum of 5 cards. We deliberately chose this setup, since with more cards the optimal strategy is more difficult to find. We therefore simplified the game to 
- The Strategy based on kripke models is heuristically determined
- The guessing is similar across 3 of the agents
- FKA loss-graph is not optimized (see Extensions)

### TODO: Conclusion

### Possible extensions

#### Q-learning

A possible extension for inferring tactics is implementing a (Deep) Q-Learning algorithm. Instead of implementing rules based on the knowledge base manually, we train a Q-Learning network to extract these rules and tactics itself. The network could have a Kripke model as an input as it is a perfect representation of the state.

The card game can be seen as a Markov Decision Process. We will define the state, action and reward as the following:

- State _S_: A list of 52 one hot encoded vectors (one for every card). Each card representation consist of 4 bits, one for every player. Here a 1 will represent a possible owner, and a 0 the opposite.
- Action _A_: A list of 52 possible cards to play. Since the player only has a subset of these cards, the possible actions can be reduced, based on the available cards.
- Reward _R(s,a)_: Results in a 1 for a win, and a 0 for a loss (we might consider adding a discount factor).

Using the representation of the MDP we can use Q-learning in combination with a multilayer perceptron as a function approximator. This function will approximate Policy P, which is choosing the action with the highest expected reward.

The implementation of such an algorithm is not the main goal of the course, but it could be interesting to combine Kripke models with a deep reinforcement learning algorithm. After training, the influence of different Kripke models on the tactics of the algorithm can be investigated. To see if the Kripke models can actually benefit the Q-learning agent, its performance could be compared to that of a greedy Kripke agent (without Q-learning).

#### Tactical guessing

Our implementation of the game is a simplified version because of time constraints. As previously discussed we focus only on 'greedy guessing' in which the agent guesses the amount of plays he will win. The player then uses a greedy tactic to get the most wins out of the game. While this results in a relatively good score this is only played by beginners. In Boeren Bridge players often use 'tactical guessing'. This means guessing and playing for 0 wins. This can get you bonus points if you succeed and can result in more points. However the player has to adopt a whole new tactic. The question is now "How can I lose my high cards without winning the trick?". It would be interesting to extend our implementation so that there are agents that use the Kripke models for both greedy and non-greedy dynamic behavior.

It would be interesting to extend the Q-learning approach mentioned above with tactical guessing. A second neural network could be used to make a correct guess and to chose which tactic to apply: greedy or non-greedy.


#### TODO: Explain how the lose graph can be updated so it used kripke knowledge:
 Is he opener -> Yes
Do you have the highest card of a non-trump suit -> Yes
Does anyone not have cards of that suit, but still have trump cards -> Yes
Play that highest non-trump suit card
#### Higher order Logic (K_1K_2)

TODO: Uitwerken punten
-We only use PAL and K1
-Make use of the fact that a player uses a certain strategy for guessing
-Make use of the fact that a player uses a certain strategy for playing cards
-Not that well applicable for games with few cards
