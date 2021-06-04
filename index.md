## LAMAS Project --- BoerenBridge

[This](https://github.com/JeroenVanB/LAMAS) is the link to our github repository.

### Game Rules

# Variations
There are many variants of the game: 'Oh hell!', 'Oh Pshaw' or 'Nomination Whist'. We decided to implement a version, which we ourselves usually play. There are 15 rounds and only the high cards of the normal deck of cards are used (7 up to Ace). The trump changes each round and is chosen randomly.

# Points
The aim of the game is to get the most points. Points can be obtained by winning tricks and (most importantly) correctly guessing how many tricks $c_{guess}$ the player himself will take in a round. 
If the player correctly guesses the total number of tricks he has taken ($c_{wins}$), he will receive two points for each trick taken, with a 10 points bonus ($2*c_{wins}+10$). A special reward is given to players if they correctly guess taking 0 tricks, in rounds with 6 or more cards. Here, the bonus points change from 10 to 20.
If the player guesses wrong, he will get two points subtracted for each trick he was off ($-2*|c_{wins}-c_{guess}|$). The player with the most points after 15 rounds wins the game.

# Gameplay
In each round, each player is given $n$ cards. From the remaining cards, one random card is picked to determine the trump of the round. Starting by the player to the left of the dealer ($P_1$) and continuing clockwise, every player $P \in \{1, 2, 3, 4\}$ guesses the number of tricks $c_{guess}^{P}$ he will win. (In the rare occasion that all the guesses sum up to $n$, the dealer has to change his guess. He has to increase or decrease his original guess with 1 such that the total is not a sum equal to $n$.)

Next, $t=n$ tricks are played. During the first trick $t_1$, the player left of the dealer starts. In the following rounds, the winner of the previous trick starts. The starting player is called 'the opener', denoted by $P_{opener}$. Every player after the opener, should play a card matching the suit of the card played by the opener. If this is not possible, the player may play any card of his choice.
# Winning tricks
The player who played the highest card during a trick, takes the trick. The cards follow the usual order, where 7 is the lowest and Ace is the highest (7, 8, 9, 10, Jack, Queen, King, Ace). When a player plays a card of a different suit than the opener, it is considered the lowest and can never win.  Trump cards, however, are always higher than the other cards.


# Number of cards
In every round $r$, the players is dealt $n_r$ cards. First, starting in the first round with $n_1=2$. In each following round, every player is given $n_r = n_{r-1}+1$ cards, up to 8 cards in total (in round 7). Then a special round without a trump is played with $n_8=8$ cards. Next, starting with $n_{9}=8$, 7 more rounds are played, where the amount of cards decreases by 1. The game ends after round 15, where $n_{15}=2$. See Table~\ref{cards} for clarification.

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/JeroenVanB/LAMAS/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
