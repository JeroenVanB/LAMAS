# Logical Aspects of Multi-Agent Systems - Logical Boeren Bridge

Authors:

- Daan Krol (d.j.krol.1@student.rug.nl)
- Julian Bruinsma (j.bruinsma.6@student.rug.nl)
- Jeroen van Brandenburg (j.c.van.brandenburg@student.rug.nl)

This repository contains the project code for the MSc course Logical Aspects of Multi-Agent Systems of the University of Groningen. In this project, we are going to analyze the Dutch game 'Boeren Bridge'. It is a card game played with four players, in which the objective is to obtain the most points, by correctly guessing the amount of tricks the player himself will take.
The program also visualizes all Kripke models for the cards in the game. Several agents are implemented that use tactics based on the Kripke Knowledge.

The full report can be found at https://jeroenvanb.github.io/LAMAS/

## Instructions

```bash
# First install all packages:
pip install -r requirements.txt
# Run the game with UI
python3 main.py

# To compare the agents performance do:
python3 main.py <number of experiments>
```
