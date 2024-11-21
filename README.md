# Kalah - Artificial Intelligence

This project was a collaborative effort with a colleague for our ```Artificial Intelligence``` course.
That was implemented in ```Python```, and all functionalities were successfully completed.
Our player achieved ```Rank 1 out of 74```, earning us a ```perfect score``` in the assignment.


## Project Overview
The goal of this project was to develop an AI player for the game ```Mancala``` (also known as ```Kalah```) using the ```alpha-beta pruning algorithm```. The AI evaluates game states at various depths to make decisions, with the objective of creating increasingly efficient versions.

The final version of the player participated in a ```tournament against other students’ AI players```, where the best player was determined by performance.

The project provided an opportunity to explore AI-based decision-making and develop a strategy capable of ```playing optimally or near-optimally``` against other AI opponents.


## What is Mancala (Kalah)?
```Mancala``` is one of the oldest family of board games with roots in Africa and the Middle East. ```Kalah``` is a modern variation of the game developed in the 1940s by William Champion. 

The game is played by two players, each with a set of 6 small pits and a larger pit (called Kalah) for storing collected seeds. 

The ```goal``` is to capture more seeds in your Kalah than your opponent.


## Game Rules:
- **Objective:** Capture more seeds in your Kalah than your opponent.
- **Setup:** Each player starts with 6 pits (4 seeds each) and one larger Kalah (store).
- **Turns:** Players distribute seeds counterclockwise. Landing the last seed in your Kalah grants another turn; landing in an empty pit captures seeds opposite it.
- **Endgame:** The game ends when one side's pits are empty, and remaining seeds go to the opponent.
- **Victory:** The player with the most seeds in their Kalah wins.


## Heuristics Implemented in our player (called Segfault):
- **_Clear the rightmost pit:_** A heuristic that always tries to empty the rightmost pit on the player's side.
- **_Prioritize captures:_** A heuristic that prioritizes moves that lead to the capture of the most seeds by the player.
- **_Avoid steals:_** A heuristic that prioritizes moves that minimize the chances of the opponent stealing seeds.
- **_Difference in Kalahs:_** A heuristic that maximizes the difference in the number of seeds in the Kalahs.
- **_Play again:_** A heuristic that prioritizes states where it is the player's turn to play again.
- **_Move that allows playing again:_** A heuristic that prioritizes moves that lead to a state where the player has a move that allows them to play again.
- **_Avoid moves that allow the opponent to play again:_** A heuristic that prioritizes moves that avoid states where the opponent has a move that allows them to play again.
- **_Save to the left:_** A heuristic that tries to keep seeds in the leftmost pit on the player's side.

**Note:** For optimization of the heuritics values we used a ```genetic algorithm``` (```genetics.py```).

## Bots/players for test:
- **_El Caos Inteligente:_** Focuses on terminal states with a simple scoring system (+100 for win, -100 for loss, 0 for draw).
- **_Chapiteu:_** Aims to maximize the seed difference between players while also scoring terminal states (+100/-100/0).


## How to Run
1. Move the file ```iia2324-proj2-jog-19.py```, which contains the final version of the player segfault with the heuristics, to the ```networked_kalah``` directory.

2. Read the ```README``` file inside the ```networked_kalah``` directory for detailed setup and execution instructions.

3. The main function containing all the logic to be used is called ```func_19```
(there's some files with examples of use like ```network_segfault_2h.py```, etc).