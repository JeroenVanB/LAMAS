## LAMAS Project --- BoerenBridge

[This](https://github.com/JeroenVanB/LAMAS) is the link to our github repository.

### Game Rules

#### Variations
There are many variants of the game: 'Oh hell!', 'Wizard' or 'Nomination Whist'. We decided to implement a version, which we ourselves usually play. To prevent state explosion, we simplified some game rules, e.g. the amount of cards. We implemented a version with 7 rounds and only the highest cards of the normal deck of cards are used. The trump changes each round and is chosen randomly.

#### Points
The aim of the game is to get the most points. Points can be obtained by winning tricks and (most importantly) correctly guessing how many tricks the player himself will take in a round. 
If the player correctly guesses the total number of tricks he has taken, he will receive two points for each trick taken, with a 10 points bonus. A special reward is given to players if they correctly guess taking 0 tricks, in rounds with 6 or more cards. Here, the bonus points increase from 10 to 20.
If the player guesses wrong, he will get two points subtracted for each trick he was off. The player with the most points after 15 rounds wins the game.

#### Gameplay
In each round, each player is given _n_ cards. From a separate set of cards, one random card is picked to determine the trump of the round. Starting by the player to the left of the dealer _P<sub>1</sub>_ and continuing clockwise, every player _P_ ∈ \{_P<sub>1</sub>_, _P<sub>2</sub>_, _P<sub>3</sub>_, _P<sub>4</sub>_\} guesses the number of tricks he will win. (In the rare occasion that all the guesses sum up to _n_, the dealer has to change his guess. He has to increase or decrease his original guess with 1 such that the total is not a sum equal to _n_.)

Next, _t_ = _n_ tricks are played, in which each player plays one card. During the first trick _t_<sub>1</sub>, the player left of the dealer starts. In the following rounds, the winner of the previous trick starts. The starting player is called _the opener_. Every player after the opener, should play a card matching the suit of the card played by the opener. If this is not possible, the player may play any card of his choice.
#### Winning tricks
The player who played the highest card during a trick, takes the trick. The cards follow the usual order, where 2 is the lowest and Ace is the highest (2, 3, 4, 5, 6, 7, 8, 9, 10, Jack, Queen, King, Ace). When a player plays a card of a different suit than the opener, it is considered the lowest and can never win.  Trump cards, however, are always higher than the other cards.


#### Number of cards
The number of cards depend on the rumber of rounds. The number of rounds can usually freedly be determined by the players. We chose to play 5 rounds.
In every round _r_, the players is dealt _t<sub>r</sub>_ cards. First, starting in the first round with _t<sub>1</sub>_ = 3. In each following round, every player is given _t<sub>r</sub>_ = _t<sub>r-1</sub>_+1 cards, up to 5 cards in total (in round 3). Then, starting with 2 more rounds are played, where the amount of cards decreases by 1. The game ends after round 5, where _n<sub>5</sub>=3. See the table below for clarification.
To decrease the possible states, we minimized the amount of cards used in the game. This way it is known which cards are in the game and wich are not. E.g. in round 1, only the (Queen, King, Ace) of all the suits are used. This is also clarified in the table below

##### Table 1
| Round  | Number of cards  | Cards                      |
| ------ | ---------------- | -------------------------- |
| 1      | 3                | Queen, King, Ace           |
| 2      | 4                | Jack, Queen, King, Ace     |
| 3      | 5                | 10, Jack, Queen, King, Ace |
| 4      | 4                | Jack, Queen, King, Ace     |
| 5      | 3                | Queen, King, Ace           |
