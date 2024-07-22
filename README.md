# Runner <img src="http://i.imgur.com/Cj4rMrS.gif" height="40" alt="Swimming Octocat" title="Games on GitHub">
[![GitHub stars](https://img.shields.io/github/stars/Bachtran301/dinosaur-game.svg)](https://github.com/Bachtran301/dinosaur-game/stargazers) [![GitHub forks](https://img.shields.io/github/forks/Bachtran301/dinosaur-game.svg)](https://github.com/Bachtran301/dinosaur-game/network)

## Introduction 

![chrome offline game cast](images/screenshot.gif)

Runner is an exciting 2D platformer game built with Pygame. Players control a character who must jump over obstacles and collect coins while running through an ever-changing landscape.

## Features

- Multiple playable characters with unique animations
- Dynamic obstacle and coin spawning
- Increasing difficulty as the game progresses
- High score tracking and rankings system
- Character selection menu
- Multiple background environments

## Installation

1. Ensure you have Python installed on your system.

| Badge                                                                                                                 | URL                                                                                                       |
| --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue" /> | `https://www.python.org/downloads/` |
2. Install Pygame:
```
pip install pygame-ce
```
3. Clone this repository or download the source code.
```
git clone https://github.com/Bachtran301/dinosaur-game.git
```
## How to run game
1. To view the high score table, follow these steps:
```
python app.py
```
2. Run game:
```
python main.py
```
## How to play game
<kbd>Space</kbd>: Jump
## Game Structure

### Player Class
- Manages player character animations and movement
- Handles gravity and jumping mechanics

### Obstacle Class

<p align="center">
<img src="./images/obstacle.png">
</p>

- Creates various obstacles (fly, spikes, snail, tooth, bee, worm)
- Manages obstacle animations and movement

### Coin Class

<p align="center">
<img src="./images/coin.png">
</p>

- Spawns gold and diamond coins
- Handles coin movement and collection

### Game States
<p align="center">

1. Initial Menu: Start or exit the game

<img src="./images/menu.png">

2. Name Input: Players enter their name

<img src="./images/name_input.png">

3. Character Selection: Choose a character to play

<img src="./images/character_selection.png">

4. Game Playing: Main gameplay loop

<img src="./images/game_playing.png">

5. Rankings Display: Show high scores after game over

<img src="./images/rank.png">

6. Achieve high scores to unlock new characters

<img src="./images/unclock_character.png">

</p>

### Website High Scores

- Show history rank

<p align="center">
<img src="./images/high_scores.png">
</p>

### Game Mechanics

- **Scoring**: Based on survival time and coin collection
- **Difficulty Progression**: Obstacles spawn more frequently as score increases
- **Collision Detection**: Between player, obstacles, and coins
- **High Score System**: Initial Menu, Name Input, Character Selection, Game Playing, Rankings Display, Unclock new characters

### Graphics and Animation

- Multiple character sprites with walking and jumping animations
- Various obstacle types with unique animations
- Dynamic background that changes based on score

### Audio



## Customization

- New characters can be added by creating appropriate sprite sheets and updating the `Player` class
- Additional obstacles can be introduced by adding new entries to the `Obstacle` class
- Adjust required scores for unlocking characters in `player_stand_images`

## Troubleshooting

- Ensure all image files are in the correct directories
- Check Pygame installation if you encounter import errors

## Future Enhancements

- Implement background music and sound effects
- Add power-ups and special abilities for characters
- Create more diverse environments and obstacles

## Credits

This game was created using Pygame. Character and obstacle sprites are custom-made for this project.

## License

This project is licensed under the [MIT License](LICENSE).

# Major Companies

A selection of major edit studios, publishers, etc. using GitHub:

[<img src="https://github.com/aseprite.png" title="aseprite" height="50">](https://github.com/aseprite)&nbsp;
[<img src="https://github.com/adobe-photoshop.png" title="adobe-photoshop" height="50">](https://github.com/adobe-photoshop)&nbsp;
[<img src="https://github.com/lospec.png" title="lospec" height="50">](https://github.com/lospec)&nbsp;
[<img src="https://github.com/unity-technologies.png" title="Unity Technologies" height="50">](https://github.com/unity-technologies)&nbsp;
[<img src="https://github.com/godotengine.png" title="godotengine" height="50">](https://github.com/godotengine)&nbsp;
[<img src="https://github.com/pygame.png" title="pygame" height="50">](https://github.com/pygame)&nbsp;
[<img src="https://github.com/microsoft.png" title="microsoft" height="50">](https://github.com/microsoft)&nbsp;



