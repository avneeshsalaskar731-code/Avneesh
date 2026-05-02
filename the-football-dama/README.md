# ⚽ The Football DAMA

A realistic French football management simulation game featuring Ligue 1 and Ligue 2.

## 🎮 Features

### Game Modes
- **Player Career Mode**: Create your own player and lead them to France national team selection
- **Manager Career Mode**: Manage a club and win Ligue 1 to complete your career

### Real Teams & Players
- All 18 Ligue 1 teams with real names
- All 20 Ligue 2 teams with real names
- Real players with accurate ratings, positions, and ages
- Dynamic player values based on performance and age

### Realistic Simulation
- Advanced match simulation with home advantage, form, and morale factors
- Player form system (0-10 scale) that fluctuates based on performances
- Team morale system affecting match outcomes
- Transfer market with budget management
- Promotion and relegation between leagues

### Advanced Features
- Save/Load game functionality
- Detailed league tables with form guides
- Player statistics tracking (goals, assists, matches)
- Team management (training, transfers)
- Season progression with end-of-season summaries
- Dynamic player development (young players improve with good performances)

## 🚀 How to Play

### Requirements
- Python 3.7 or higher
- No external dependencies required (uses standard library only)

### Installation
1. Navigate to the game directory:
```bash
cd the-football-dama
```

2. Run the game:
```bash
python src/game.py
```

### Gameplay

#### Main Menu
- **New Player Career**: Create a custom player and start their journey
- **New Manager Career**: Choose a team to manage
- **Load Game**: Continue a saved career
- **View Teams**: Browse all Ligue 1 and Ligue 2 squads
- **Exit**: Close the game

#### Player Career
1. Enter your player's name, position, age, and nationality
2. Choose a Ligue 1 team to join
3. Play through matchdays, improving your performance
4. Score goals and maintain high form to get noticed
5. **Goal**: Get selected for France national team to win!

#### Manager Career
1. Enter your manager name
2. Choose a Ligue 1 team to manage
3. Manage your squad, make transfers, and boost morale
4. Win matches to climb the table
5. **Goal**: Win Ligue 1 to complete your career!

### Controls
- Use number keys to select menu options
- Press Enter to continue after match results
- Save your progress regularly using option [5]

## 📊 Game Mechanics

### Match Simulation
Matches are simulated using:
- Team average ratings
- Home field advantage (+3 rating points)
- Recent form (last 5 matches)
- Team morale
- Poisson distribution for realistic goal scoring

### Player Development
- Young players (< 25) can improve their rating with good performances
- Form affects match performance and transfer value
- Goals and assists increase call-up chances for national team

### Transfer System
- Each team has a transfer budget
- Player values calculated from rating and age
- Teams can buy/sell players during the season
- Budget management is crucial for success

### Season Structure
- 34 matchdays per season (home and away vs each team)
- Top team wins Ligue 1
- Bottom 3 teams relegated to Ligue 2
- Top 3 Ligue 2 teams promoted

## 🏆 Winning Conditions

### Player Career
The game ends when you receive a France national team call-up. This happens based on:
- Player rating (higher = better chance)
- Current form (perform well consistently)
- Goals scored (for attacking positions)
- Patience and continuous improvement

### Manager Career
The game ends when you win Ligue 1 at the end of a season. You must:
- Finish top of the table after 34 matchdays
- Manage your team effectively throughout the season
- Make smart transfer decisions
- Keep team morale high

## 💾 Save System
- Games auto-save when you achieve the objective
- Manual save available in the menu (option 5)
- Save files stored as JSON for easy editing
- Load previous saves from the main menu

## 🛠️ Customization

### Adding Teams/Players
Edit `data/teams.json` to add or modify:
- Team names and short names
- Player rosters with custom stats
- League structure

### Modifying Game Balance
Adjust these values in `src/game.py`:
- `home_advantage`: Default is 3.0
- Player development rates
- Transfer market probabilities
- National team call-up thresholds

## 📝 File Structure
```
the-football-dama/
├── src/
│   └── game.py          # Main game code
├── data/
│   └── teams.json       # Team and player data
├── assets/              # Future graphics/sounds
├── savegame.json        # Current save file
└── README.md            # This file
```

## 🎯 Tips for Success

### Player Career
- Choose a younger age (16-20) for more development time
- Maintain form above 7.0 for best call-up chances
- Score goals consistently if playing as attacker
- Be patient - national team call-ups take time

### Manager Career
- Start with a top team (PSG, Marseille, Monaco) for easier difficulty
- Use training sessions to boost morale before important matches
- Monitor your budget and make smart transfers
- Focus on consistency throughout the season

## 🔧 Troubleshooting

### Game won't start
- Ensure Python 3.7+ is installed
- Check that you're in the correct directory
- Verify `teams.json` exists in the `data/` folder

### Save game not loading
- Check file permissions
- Ensure save file is valid JSON
- Try starting a new game

## 📄 License
This is a fan-made game for educational and entertainment purposes.
All team and player names are property of their respective owners.

## 👨‍💻 Credits
Developed as a demonstration of text-based sports simulation games.

---

**Enjoy managing your way to glory in The Football DAMA! ⚽🇫🇷**
