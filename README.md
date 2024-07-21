# Games <img src="http://i.imgur.com/Cj4rMrS.gif" height="40" alt="Swimming Octocat" title="Games on GitHub">

# Runner #

## Introduction 

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
| Badge                                                                                                                | URL                                                                                                      |
2. Install Pygame:
```
pip install pygame-ce
```
3. Clone this repository or download the source code.

## Usage
```
python main.py
```
## Game Structure

### Player Class
- Manages player character animations and movement
- Handles gravity and jumping mechanics

### Obstacle Class
- Creates various obstacles (fly, spikes, snail, tooth, bee, worm)
- Manages obstacle animations and movement

### Coin Class
- Spawns gold and diamond coins
- Handles coin movement and collection

### Game States
1. Name Input: Players enter their name
2. Initial Menu: Start or exit the game
3. Character Selection: Choose a character to play
4. Game Playing: Main gameplay loop
5. Rankings Display: Show high scores after game over

### Game Mechanics

- **Scoring**: Based on survival time and coin collection
- **Difficulty Progression**: Obstacles spawn more frequently as score increases
- **Collision Detection**: Between player, obstacles, and coins
- **High Score System**: Tracks and displays top scores

### Graphics and Animation

- Multiple character sprites with walking and jumping animations
- Various obstacle types with unique animations
- Dynamic background that changes based on score

### Audio
(Note: Audio implementation is mentioned as a placeholder in the original code)

## Customization

- New characters can be added by creating appropriate sprite sheets and updating the `Player` class
- Additional obstacles can be introduced by adding new entries to the `Obstacle` class

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


A selection of major edit studios, publishers, etc. using GitHub:

[<img src="https://github.com/aseprite.png" title="aseprite" height="50">](https://github.com/aseprite)&nbsp;
[<img src="https://github.com/adobe-photoshop.png" title="adobe-photoshop" height="50">](https://github.com/adobe-photoshop)&nbsp;
[<img src="https://github.com/lospec.png" title="lospec" height="50">](https://github.com/lospec)&nbsp;
[<img src="https://github.com/unity-technologies.png" title="Unity Technologies" height="50">](https://github.com/unity-technologies)&nbsp;
[<img src="https://github.com/godotengine.png" title="godotengine" height="50">](https://github.com/godotengine)&nbsp;
[<img src="https://github.com/pygame.png" title="pygame" height="50">](https://github.com/pygame)&nbsp;
[<img src="https://github.com/microsoft.png" title="microsoft" height="50">](https://github.com/microsoft)&nbsp;



