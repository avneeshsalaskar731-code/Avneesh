#!/usr/bin/env python3
"""
The Football DAMA - A realistic French football management simulation
Features:
- Ligue 1 and Ligue 2 with real teams and players
- Player Career mode (ends when selected for France)
- Manager Career mode (ends when winning Ligue 1)
- Realistic match simulation
- Transfer system
- League table, promotion/relegation
- Advanced statistics
"""

import json
import random
import math
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import os

# ==================== DATA CLASSES ====================

class Mode(Enum):
    PLAYER_CAREER = "player"
    MANAGER_CAREER = "manager"

class Position(Enum):
    GK = "GK"
    RB = "RB"
    CB = "CB"
    LB = "LB"
    CDM = "CDM"
    CM = "CM"
    CAM = "CAM"
    RW = "RW"
    LW = "LW"
    ST = "ST"

@dataclass
class Player:
    name: str
    position: str
    age: int
    rating: int
    nationality: str
    goals: int = 0
    assists: int = 0
    matches_played: int = 0
    yellow_cards: int = 0
    red_cards: int = 0
    form: float = 5.0  # 0-10 scale
    fitness: int = 100
    value: int = 0
    
    def __post_init__(self):
        # Calculate player value based on rating and age
        base_value = self.rating * 100000
        age_factor = max(0.5, 1.0 - (abs(self.age - 27) * 0.03))
        self.value = int(base_value * age_factor * 1000)
    
    def to_dict(self):
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data)

@dataclass
class Team:
    name: str
    short_name: str
    players: List[Player]
    points: int = 0
    played: int = 0
    won: int = 0
    drawn: int = 0
    lost: int = 0
    goals_for: int = 0
    goals_against: int = 0
    goal_difference: int = 0
    form: List[str] = field(default_factory=list)  # Last 5 matches: W, D, L
    budget: int = 50000000  # Transfer budget
    morale: float = 5.0  # 0-10 scale
    
    def to_dict(self):
        data = asdict(self)
        data['players'] = [p.to_dict() if isinstance(p, Player) else p for p in self.players]
        return data
    
    @classmethod
    def from_dict(cls, data):
        data['players'] = [Player(**p) if isinstance(p, dict) else p for p in data['players']]
        return cls(**data)
    
    def get_average_rating(self):
        if not self.players:
            return 0
        return sum(p.rating for p in self.players) / len(self.players)
    
    def get_best_xi(self):
        """Select best 11 players based on rating and form"""
        sorted_players = sorted(self.players, key=lambda p: p.rating * 0.7 + p.form * 3, reverse=True)
        
        # Simple formation: 4-3-3
        xi = []
        positions_needed = {'GK': 1, 'RB': 1, 'CB': 2, 'LB': 1, 'CDM': 1, 'CM': 2, 'RW': 1, 'LW': 1, 'ST': 1}
        positions_filled = {pos: 0 for pos in positions_needed}
        
        for player in sorted_players:
            pos = player.position
            if pos in positions_needed and positions_filled[pos] < positions_needed[pos]:
                xi.append(player)
                positions_filled[pos] += 1
            if len(xi) >= 11:
                break
        
        # Fill remaining spots with best available
        while len(xi) < 11:
            for player in sorted_players:
                if player not in xi:
                    xi.append(player)
                    break
        
        return xi[:11]

@dataclass
class Match:
    home_team: str
    away_team: str
    home_score: int = 0
    away_score: int = 0
    played: bool = False
    matchday: int = 0
    home_scorers: List[str] = field(default_factory=list)
    away_scorers: List[str] = field(default_factory=list)
    
    def to_dict(self):
        return asdict(self)

@dataclass
class Season:
    year: int
    ligue1_standings: List[Dict] = field(default_factory=list)
    ligue2_standings: List[Dict] = field(default_factory=list)
    promoted_teams: List[str] = field(default_factory=list)
    relegated_teams: List[str] = field(default_factory=list)

@dataclass
class GameSave:
    mode: str
    player_name: str
    player_age: int
    player_position: str
    player_nationality: str
    player_rating: int
    current_team: str
    current_league: str
    season: int
    matchday: int
    ligue1_teams: List[Dict]
    ligue2_teams: List[Dict]
    fixtures: List[Dict]
    seasons: List[Dict]
    player_stats: Dict = field(default_factory=dict)
    france_caps: int = 0
    game_ended: bool = False
    end_reason: str = ""

# ==================== GAME ENGINE ====================

class FootballDAMA:
    def __init__(self):
        self.ligue1_teams: Dict[str, Team] = {}
        self.ligue2_teams: Dict[str, Team] = {}
        self.fixtures: List[Match] = []
        self.current_matchday: int = 1
        self.total_matchdays: int = 34
        self.season_year: int = 2024
        self.mode: Optional[Mode] = None
        self.player_career_data: Dict = {}
        self.manager_career_data: Dict = {}
        self.seasons_history: List[Season] = []
        self.game_ended: bool = False
        self.end_reason: str = ""
        
        self.load_teams()
    
    def load_teams(self):
        """Load team data from JSON file"""
        try:
            with open('data/teams.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            for team_data in data['ligue1']:
                players = [Player(**p) for p in team_data['players']]
                team = Team(
                    name=team_data['name'],
                    short_name=team_data['short_name'],
                    players=players,
                    budget=random.randint(30000000, 200000000)
                )
                self.ligue1_teams[team_data['name']] = team
            
            for team_data in data['ligue2']:
                players = [Player(**p) for p in team_data['players']]
                team = Team(
                    name=team_data['name'],
                    short_name=team_data['short_name'],
                    players=players,
                    budget=random.randint(5000000, 30000000)
                )
                self.ligue2_teams[team_data['name']] = team
                
        except FileNotFoundError:
            print("Error: teams.json not found!")
            self.create_default_teams()
    
    def create_default_teams(self):
        """Create default teams if JSON file is missing"""
        # Fallback to basic teams
        pass
    
    def generate_fixtures(self):
        """Generate round-robin fixtures for the season"""
        self.fixtures = []
        teams_list = list(self.ligue1_teams.keys())
        
        # Simple round-robin algorithm
        if len(teams_list) % 2 == 1:
            teams_list.append("BYE")
        
        num_teams = len(teams_list)
        rounds = num_teams - 1
        matches_per_round = num_teams // 2
        
        for round_num in range(rounds):
            for match_num in range(matches_per_round):
                home_idx = (round_num + match_num) % (num_teams - 1)
                away_idx = (num_teams - 1 - match_num + round_num) % (num_teams - 1)
                
                if round_num % 2 == 0:
                    home, away = teams_list[home_idx], teams_list[away_idx]
                else:
                    home, away = teams_list[away_idx], teams_list[home_idx]
                
                if home != "BYE" and away != "BYE":
                    match = Match(
                        home_team=home,
                        away_team=away,
                        matchday=round_num + 1
                    )
                    self.fixtures.append(match)
        
        # Sort by matchday
        self.fixtures.sort(key=lambda m: m.matchday)
    
    def simulate_match(self, match: Match) -> Match:
        """Simulate a single match with realistic outcomes"""
        home_team = self.ligue1_teams.get(match.home_team)
        away_team = self.ligue1_teams.get(match.away_team)
        
        if not home_team or not away_team:
            return match
        
        # Calculate team strengths
        home_strength = home_team.get_average_rating()
        away_strength = away_team.get_average_rating()
        
        # Home advantage
        home_advantage = 3.0
        
        # Form factor
        home_form = sum(1 for r in home_team.form[-5:] if r == 'W') - sum(1 for r in home_team.form[-5:] if r == 'L')
        away_form = sum(1 for r in away_team.form[-5:] if r == 'W') - sum(1 for r in away_team.form[-5:] if r == 'L')
        
        # Morale factor
        home_morale = home_team.morale / 10.0
        away_morale = away_team.morale / 10.0
        
        # Calculate expected goals
        strength_diff = (home_strength - away_strength) / 10.0
        home_expected = 1.5 + strength_diff + home_advantage/10 + home_form * 0.1 + home_morale * 0.2
        away_expected = 1.2 - strength_diff + away_form * 0.1 + away_morale * 0.2
        
        # Poisson-like distribution for goals
        home_goals = max(0, int(random.gauss(home_expected, 1.2)))
        away_goals = max(0, int(random.gauss(away_expected, 1.2)))
        
        match.home_score = home_goals
        match.away_score = away_goals
        match.played = True
        
        # Determine scorers (simplified)
        home_xi = home_team.get_best_xi()
        away_xi = away_team.get_best_xi()
        
        attackers = [p for p in home_xi if p.position in ['ST', 'LW', 'RW', 'CAM']]
        for _ in range(home_goals):
            if attackers:
                scorer = random.choice(attackers)
                match.home_scorers.append(scorer.name)
                scorer.goals += 1
        
        attackers = [p for p in away_xi if p.position in ['ST', 'LW', 'RW', 'CAM']]
        for _ in range(away_goals):
            if attackers:
                scorer = random.choice(attackers)
                match.away_scorers.append(scorer.name)
                scorer.goals += 1
        
        return match
    
    def update_table(self, match: Match):
        """Update league table after a match"""
        home_team = self.ligue1_teams.get(match.home_team)
        away_team = self.ligue1_teams.get(match.away_team)
        
        if not home_team or not away_team:
            return
        
        # Update stats
        home_team.played += 1
        away_team.played += 1
        home_team.goals_for += match.home_score
        home_team.goals_against += match.away_score
        away_team.goals_for += match.away_score
        away_team.goals_against += match.home_score
        home_team.goal_difference = home_team.goals_for - home_team.goals_against
        away_team.goal_difference = away_team.goals_for - away_team.goals_against
        
        # Determine result
        if match.home_score > match.away_score:
            home_team.won += 1
            home_team.points += 3
            home_team.form.append('W')
            away_team.lost += 1
            away_team.form.append('L')
            home_team.morale = min(10, home_team.morale + 0.3)
            away_team.morale = max(0, away_team.morale - 0.3)
        elif match.home_score < match.away_score:
            away_team.won += 1
            away_team.points += 3
            away_team.form.append('W')
            home_team.lost += 1
            home_team.form.append('L')
            away_team.morale = min(10, away_team.morale + 0.3)
            home_team.morale = max(0, home_team.morale - 0.3)
        else:
            home_team.drawn += 1
            away_team.drawn += 1
            home_team.points += 1
            away_team.points += 1
            home_team.form.append('D')
            away_team.form.append('D')
        
        # Keep only last 5 form
        home_team.form = home_team.form[-5:]
        away_team.form = away_team.form[-5:]
    
    def get_ligue1_table(self) -> List[Team]:
        """Get sorted Ligue 1 table"""
        teams = list(self.ligue1_teams.values())
        teams.sort(key=lambda t: (t.points, t.goal_difference, t.goals_for), reverse=True)
        return teams
    
    def play_matchday(self, matchday: int):
        """Play all matches for a given matchday"""
        matches = [m for m in self.fixtures if m.matchday == matchday and not m.played]
        
        for match in matches:
            match = self.simulate_match(match)
            self.update_table(match)
        
        self.current_matchday = matchday + 1
    
    def check_player_career_end(self):
        """Check if player career should end (selected for France)"""
        if self.mode != Mode.PLAYER_CAREER:
            return
        
        player_data = self.player_career_data
        caps = player_data.get('france_caps', 0)
        
        # Chance of being called up based on performance
        if caps == 0:
            player_rating = player_data.get('rating', 70)
            form = player_data.get('form', 5.0)
            goals = player_data.get('goals', 0)
            
            # Better chance with higher rating and form
            callup_chance = (player_rating - 75) * 0.02 + (form - 5) * 0.05 + goals * 0.01
            
            if random.random() < callup_chance:
                player_data['france_caps'] = 1
                self.game_ended = True
                self.end_reason = f"🇫🇷 Congratulations! {player_data['name']} has been selected for France national team!"
    
    def check_manager_career_end(self):
        """Check if manager career should end (won Ligue 1)"""
        if self.mode != Mode.MANAGER_CAREER:
            return
        
        manager_team = self.manager_career_data.get('team', '')
        table = self.get_ligue1_table()
        
        if table and table[0].name == manager_team:
            # Check if season is over
            if self.current_matchday > self.total_matchdays:
                self.game_ended = True
                self.end_reason = f"🏆 Congratulations! You won Ligue 1 with {manager_team}!"
    
    def process_transfers(self):
        """Simple transfer system"""
        # Random transfers between teams
        for team_name, team in list(self.ligue1_teams.items()):
            if random.random() < 0.1:  # 10% chance per matchday
                # Try to sign a player
                other_teams = [t for t in self.ligue1_teams.values() if t.name != team_name]
                if other_teams and team.budget > 10000000:
                    target_team = random.choice(other_teams)
                    if target_team.players:
                        target_player = random.choice(target_team.players)
                        if target_player.value <= team.budget and target_player.rating < 85:
                            # Transfer happens
                            team.players.append(target_player)
                            team.budget -= target_player.value
                            target_team.players.remove(target_player)
                            target_team.budget += target_player.value
    
    def update_player_form(self):
        """Update player form based on recent performances"""
        for team in self.ligue1_teams.values():
            for player in team.players:
                # Form fluctuates slightly
                change = random.uniform(-0.3, 0.3)
                player.form = max(0, min(10, player.form + change))
                
                # Fitness recovery
                player.fitness = min(100, player.fitness + 5)
    
    def start_player_career(self, name: str, position: str, age: int, nationality: str, starting_team: str):
        """Initialize player career mode"""
        self.mode = Mode.PLAYER_CAREER
        
        # Create player
        base_rating = random.randint(65, 75)
        self.player_career_data = {
            'name': name,
            'position': position,
            'age': age,
            'nationality': nationality,
            'rating': base_rating,
            'team': starting_team,
            'goals': 0,
            'assists': 0,
            'matches': 0,
            'form': 5.0,
            'france_caps': 0,
            'seasons': 0
        }
        
        # Add player to team if not exists
        if starting_team in self.ligue1_teams:
            team = self.ligue1_teams[starting_team]
            new_player = Player(
                name=name,
                position=position,
                age=age,
                nationality=nationality,
                rating=base_rating
            )
            team.players.append(new_player)
    
    def start_manager_career(self, name: str, team_name: str):
        """Initialize manager career mode"""
        self.mode = Mode.MANAGER_CAREER
        
        self.manager_career_data = {
            'name': name,
            'team': team_name,
            'wins': 0,
            'draws': 0,
            'losses': 0,
            'trophies': [],
            'seasons': 0
        }
    
    def save_game(self, filename: str = 'savegame.json'):
        """Save current game state"""
        save_data = GameSave(
            mode=self.mode.value if self.mode else "",
            player_name=self.player_career_data.get('name', ''),
            player_age=self.player_career_data.get('age', 0),
            player_position=self.player_career_data.get('position', ''),
            player_nationality=self.player_career_data.get('nationality', ''),
            player_rating=self.player_career_data.get('rating', 0),
            current_team=self.player_career_data.get('team', '') or self.manager_career_data.get('team', ''),
            current_league="Ligue 1",
            season=self.season_year,
            matchday=self.current_matchday,
            ligue1_teams=[t.to_dict() for t in self.ligue1_teams.values()],
            ligue2_teams=[t.to_dict() for t in self.ligue2_teams.values()],
            fixtures=[f.to_dict() for f in self.fixtures],
            seasons=[asdict(s) for s in self.seasons_history],
            player_stats=self.player_career_data,
            france_caps=self.player_career_data.get('france_caps', 0),
            game_ended=self.game_ended,
            end_reason=self.end_reason
        )
        
        with open(filename, 'w') as f:
            json.dump(asdict(save_data), f, indent=2)
    
    def load_game(self, filename: str = 'savegame.json') -> bool:
        """Load saved game"""
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            
            self.mode = Mode(data['mode']) if data['mode'] else None
            self.player_career_data = data.get('player_stats', {})
            self.current_matchday = data['matchday']
            self.season_year = data['season']
            self.game_ended = data.get('game_ended', False)
            self.end_reason = data.get('end_reason', '')
            
            # Load teams
            for team_data in data['ligue1_teams']:
                self.ligue1_teams[team_data['name']] = Team.from_dict(team_data)
            
            for team_data in data['ligue2_teams']:
                self.ligue2_teams[team_data['name']] = Team.from_dict(team_data)
            
            # Load fixtures
            self.fixtures = [Match(**f) for f in data['fixtures']]
            
            return True
        except Exception as e:
            print(f"Error loading save: {e}")
            return False

# ==================== UI FUNCTIONS ====================

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_header(title: str):
    print("\n" + "=" * 60)
    print(f"  ⚽ THE FOOTBALL DAMA ⚽")
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60 + "\n")

def display_table(teams: List[Team]):
    """Display league table"""
    print(f"\n{'Pos':<4} {'Team':<25} {'P':<3} {'W':<3} {'D':<3} {'L':<3} {'GF':<3} {'GA':<3} {'GD':<4} {'Pts':<4} {'Form'}")
    print("-" * 90)
    
    for i, team in enumerate(teams, 1):
        form_str = ' '.join(team.form[-5:]) if team.form else '-'
        print(f"{i:<4} {team.name:<25} {team.played:<3} {team.won:<3} {team.drawn:<3} {team.lost:<3} "
              f"{team.goals_for:<3} {team.goals_against:<3} {team.goal_difference:<4} {team.points:<4} {form_str}")

def display_menu(options: List[Tuple[str, str]]):
    """Display menu options"""
    for key, description in options:
        print(f"  [{key}] {description}")
    print()

def main_menu():
    """Main menu"""
    game = FootballDAMA()
    
    while True:
        clear_screen()
        print_header("MAIN MENU")
        
        options = [
            ("1", "New Player Career"),
            ("2", "New Manager Career"),
            ("3", "Load Game"),
            ("4", "View Ligue 1 Teams"),
            ("5", "View Ligue 2 Teams"),
            ("6", "Exit")
        ]
        
        display_menu(options)
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            setup_player_career(game)
        elif choice == "2":
            setup_manager_career(game)
        elif choice == "3":
            if game.load_game():
                print("Game loaded successfully!")
                continue_game(game)
            else:
                input("Failed to load game. Press Enter to continue...")
        elif choice == "4":
            view_teams(game.ligue1_teams)
        elif choice == "5":
            view_teams(game.ligue2_teams)
        elif choice == "6":
            print("Thank you for playing The Football DAMA!")
            break

def setup_player_career(game: FootballDAMA):
    """Setup player career mode"""
    clear_screen()
    print_header("PLAYER CAREER SETUP")
    
    name = input("Enter player name: ").strip()
    if not name:
        name = "Unknown Player"
    
    print("\nPositions: GK, RB, CB, LB, CDM, CM, CAM, RW, LW, ST")
    position = input("Enter position: ").strip().upper()
    if position not in ['GK', 'RB', 'CB', 'LB', 'CDM', 'CM', 'CAM', 'RW', 'LW', 'ST']:
        position = 'ST'
    
    try:
        age = int(input("Enter age (16-35): ").strip())
        age = max(16, min(35, age))
    except:
        age = 18
    
    nationality = input("Enter nationality: ").strip()
    if not nationality:
        nationality = "France"
    
    print("\nAvailable Ligue 1 teams:")
    for i, team_name in enumerate(game.ligue1_teams.keys(), 1):
        print(f"  {i}. {team_name}")
    
    try:
        team_choice = int(input(f"Choose team (1-{len(game.ligue1_teams)}): ").strip())
        team_name = list(game.ligue1_teams.keys())[max(0, min(team_choice - 1, len(game.ligue1_teams) - 1))]
    except:
        team_name = list(game.ligue1_teams.keys())[0]
    
    game.start_player_career(name, position, age, nationality, team_name)
    game.generate_fixtures()
    
    print(f"\n✅ Career started! You are {name}, a {position} playing for {team_name}")
    input("Press Enter to continue...")
    
    continue_game(game)

def setup_manager_career(game: FootballDAMA):
    """Setup manager career mode"""
    clear_screen()
    print_header("MANAGER CAREER SETUP")
    
    name = input("Enter manager name: ").strip()
    if not name:
        name = "Unknown Manager"
    
    print("\nAvailable Ligue 1 teams:")
    for i, team_name in enumerate(game.ligue1_teams.keys(), 1):
        team = game.ligue1_teams[team_name]
        print(f"  {i}. {team_name} (Avg Rating: {team.get_average_rating():.1f})")
    
    try:
        team_choice = int(input(f"Choose team (1-{len(game.ligue1_teams)}): ").strip())
        team_name = list(game.ligue1_teams.keys())[max(0, min(team_choice - 1, len(game.ligue1_teams) - 1))]
    except:
        team_name = list(game.ligue1_teams.keys())[0]
    
    game.start_manager_career(name, team_name)
    game.generate_fixtures()
    
    print(f"\n✅ Career started! You are managing {team_name}")
    print("🏆 Objective: Win Ligue 1 to complete your career!")
    input("Press Enter to continue...")
    
    continue_game(game)

def view_teams(teams: Dict[str, Team]):
    """View teams and their squads"""
    clear_screen()
    print_header("TEAM SQUADS")
    
    for i, (name, team) in enumerate(teams.items(), 1):
        print(f"\n{name} (Avg Rating: {team.get_average_rating():.1f})")
        print(f"Budget: €{team.budget:,}")
        print("-" * 60)
        print(f"{'Name':<25} {'Pos':<5} {'Age':<4} {'Rating':<7} {'Nationality'}")
        
        for player in sorted(team.players, key=lambda p: p.rating, reverse=True)[:15]:
            print(f"{player.name:<25} {player.position:<5} {player.age:<4} {player.rating:<7} {player.nationality}")
    
    input("\nPress Enter to return...")

def continue_game(game: FootballDAMA):
    """Main game loop"""
    while not game.game_ended:
        clear_screen()
        
        if game.mode == Mode.PLAYER_CAREER:
            print_header(f"PLAYER CAREER - Matchday {game.current_matchday}/{game.total_matchdays}")
            player = game.player_career_data
            print(f"Player: {player['name']} | {player['position']} | Age: {player['age']}")
            print(f"Team: {player['team']} | Rating: {player['rating']} | Form: {player['form']:.1f}/10")
            print(f"Goals: {player['goals']} | Assists: {player['assists']} | Matches: {player['matches']}")
            print(f"France Caps: {player['france_caps']}")
        else:
            print_header(f"MANAGER CAREER - Matchday {game.current_matchday}/{game.total_matchdays}")
            manager = game.manager_career_data
            team = game.ligue1_teams.get(manager['team'])
            print(f"Manager: {manager['name']}")
            print(f"Team: {manager['team']} | Points: {team.points if team else 0}")
            print(f"Record: {manager['wins']}W - {manager['draws']}D - {manager['losses']}L")
        
        # Show league table
        table = game.get_ligue1_table()
        print("\n📊 LIGUE 1 TABLE (Top 10)")
        display_table(table[:10])
        
        # Menu
        print("\n" + "=" * 60)
        print("  OPTIONS")
        print("=" * 60)
        print("  [1] Play Next Matchday")
        print("  [2] View Full Table")
        print("  [3] View My Team")
        if game.mode == Mode.PLAYER_CAREER:
            print("  [4] View Player Stats")
        else:
            print("  [4] Team Management")
        print("  [5] Save Game")
        print("  [6] Exit to Main Menu")
        print()
        
        choice = input("Select option: ").strip()
        
        if choice == "1":
            play_matchday_flow(game)
        elif choice == "2":
            clear_screen()
            display_table(table)
            input("\nPress Enter to continue...")
        elif choice == "3":
            view_my_team(game)
        elif choice == "4":
            if game.mode == Mode.PLAYER_CAREER:
                view_player_stats(game)
            else:
                team_management(game)
        elif choice == "5":
            game.save_game()
            print("✅ Game saved!")
            input("Press Enter to continue...")
        elif choice == "6":
            break
    
    # Game ended
    game_over_screen(game)

def play_matchday_flow(game: FootballDAMA):
    """Play a matchday"""
    if game.current_matchday > game.total_matchdays:
        # End of season
        process_season_end(game)
        return
    
    clear_screen()
    print_header(f"MATCHDAY {game.current_matchday}")
    
    # Get matches for this matchday
    matches = [m for m in game.fixtures if m.matchday == game.current_matchday]
    
    # Highlight player/manager's team match
    if game.mode == Mode.PLAYER_CAREER:
        my_team = game.player_career_data['team']
    else:
        my_team = game.manager_career_data['team']
    
    for match in matches:
        is_my_match = match.home_team == my_team or match.away_team == my_team
        
        if is_my_match:
            print(f"\n⭐ YOUR MATCH: {match.home_team} vs {match.away_team}")
            print("Simulating your match...")
            
            # Simulate with more detail
            match = game.simulate_match(match)
            game.update_table(match)
            
            print(f"\n📍 FULL TIME: {match.home_team} {match.home_score} - {match.away_score} {match.away_team}")
            
            if match.home_scorers:
                print(f"   Scorers ({match.home_team}): {', '.join(match.home_scorers)}")
            if match.away_scorers:
                print(f"   Scorers ({match.away_team}): {', '.join(match.away_scorers)}")
            
            # Update player stats
            if game.mode == Mode.PLAYER_CAREER:
                update_player_performance(game, match)
            else:
                update_manager_record(game, match)
        else:
            # Simulate other matches quickly
            match = game.simulate_match(match)
            game.update_table(match)
    
    # Post-matchday updates
    game.update_player_form()
    game.process_transfers()
    
    # Check for career end conditions
    if game.mode == Mode.PLAYER_CAREER:
        game.check_player_career_end()
    else:
        game.check_manager_career_end()
    
    input("\nPress Enter to continue...")

def update_player_performance(game: FootballDAMA, match: Match):
    """Update player stats after a match"""
    player = game.player_career_data
    player['matches'] += 1
    
    # Random performance
    performance = random.uniform(5, 10)
    
    # Goals/assists chance
    if random.random() < 0.3:  # 30% chance to score
        player['goals'] += 1
        performance = min(10, performance + 1)
    
    if random.random() < 0.2:  # 20% chance for assist
        player['assists'] += 1
    
    # Update form
    player['form'] = (player['form'] * 0.7 + performance * 0.3)
    
    # Rating improvement
    if performance > 7.5 and player['age'] < 25:
        player['rating'] = min(95, player['rating'] + random.randint(0, 1))
    
    # Age progression
    if game.current_matchday % 34 == 1 and game.current_matchday > 1:
        player['age'] += 1
        player['seasons'] += 1

def update_manager_record(game: FootballDAMA, match: Match):
    """Update manager record after a match"""
    manager = game.manager_career_data
    
    if match.home_score > match.away_score:
        manager['wins'] += 1
    elif match.home_score < match.away_score:
        manager['losses'] += 1
    else:
        manager['draws'] += 1

def view_my_team(game: FootballDAMA):
    """View user's team"""
    if game.mode == Mode.PLAYER_CAREER:
        team_name = game.player_career_data['team']
    else:
        team_name = game.manager_career_data['team']
    
    team = game.ligue1_teams.get(team_name)
    if not team:
        print("Team not found!")
        input("Press Enter to continue...")
        return
    
    clear_screen()
    print_header(f"{team_name} Squad")
    
    print(f"Average Rating: {team.get_average_rating():.1f}")
    print(f"Budget: €{team.budget:,}")
    print(f"Morale: {team.morale:.1f}/10")
    print(f"League Position: {game.get_ligue1_table().index(team) + 1}")
    
    print(f"\n{'Name':<30} {'Pos':<5} {'Age':<4} {'Rating':<7} {'Form':<5} {'Goals'}")
    print("-" * 70)
    
    for player in sorted(team.players, key=lambda p: p.rating, reverse=True):
        print(f"{player.name:<30} {player.position:<5} {player.age:<4} {player.rating:<7} {player.form:<5.1f} {player.goals}")
    
    input("\nPress Enter to continue...")

def view_player_stats(game: FootballDAMA):
    """View detailed player stats"""
    player = game.player_career_data
    
    clear_screen()
    print_header(f"{player['name']} - Career Stats")
    
    print(f"Age: {player['age']}")
    print(f"Position: {player['position']}")
    print(f"Nationality: {player['nationality']}")
    print(f"Current Rating: {player['rating']}")
    print(f"Current Form: {player['form']:.1f}/10")
    print(f"Current Team: {player['team']}")
    
    print("\n📊 CAREER STATISTICS")
    print(f"Matches Played: {player['matches']}")
    print(f"Goals: {player['goals']}")
    print(f"Assists: {player['assists']}")
    print(f"France Caps: {player['france_caps']}")
    print(f"Seasons Played: {player['seasons']}")
    
    if player['france_caps'] > 0:
        print("\n🎉 INTERNATIONAL CAREER: ACTIVE")
    else:
        print("\n💪 Keep performing well to get called up to France!")
    
    input("\nPress Enter to continue...")

def team_management(game: FootballDAMA):
    """Manager team management options"""
    while True:
        clear_screen()
        print_header("TEAM MANAGEMENT")
        
        manager = game.manager_career_data
        team = game.ligue1_teams.get(manager['team'])
        
        if not team:
            break
        
        print(f"Team: {team.name}")
        print(f"Budget: €{team.budget:,}")
        print(f"Morale: {team.morale:.1f}/10")
        
        print("\nOptions:")
        print("  [1] View Squad")
        print("  [2] Training (Boost Morale)")
        print("  [3] Transfer Market")
        print("  [4] Back")
        
        choice = input("Select: ").strip()
        
        if choice == "1":
            view_my_team(game)
        elif choice == "2":
            team.morale = min(10, team.morale + 0.5)
            print("✅ Training session completed! Morale boosted.")
            input("Press Enter to continue...")
        elif choice == "3":
            transfer_market(game, team)
        elif choice == "4":
            break

def transfer_market(game: FootballDAMA, team: Team):
    """Simple transfer market"""
    clear_screen()
    print_header("TRANSFER MARKET")
    
    # Show available players from other teams
    available = []
    for other_team in game.ligue1_teams.values():
        if other_team.name != team.name:
            for player in other_team.players:
                if player.value <= team.budget and player.rating < 85:
                    available.append((player, other_team.name))
    
    if not available:
        print("No players available within your budget!")
        input("Press Enter to continue...")
        return
    
    print(f"Your Budget: €{team.budget:,}")
    print(f"\nAvailable Players (showing first 20):")
    print(f"{'Name':<25} {'Pos':<5} {'Age':<4} {'Rating':<7} {'Value':<12} {'Current Team'}")
    print("-" * 90)
    
    for i, (player, team_name) in enumerate(available[:20], 1):
        print(f"{i:<2} {player.name:<25} {player.position:<5} {player.age:<4} {player.rating:<7} €{player.value:>10,} {team_name}")
    
    try:
        choice = int(input(f"\nSign player (1-{min(20, len(available))}): ").strip())
        if 1 <= choice <= len(available):
            player, old_team_name = available[choice - 1]
            player_obj = Player(**player) if isinstance(player, dict) else player
            
            # Find actual player object
            for t in game.ligue1_teams.values():
                for p in t.players:
                    if p.name == player_obj.name:
                        if team.budget >= p.value:
                            team.players.append(p)
                            team.budget -= p.value
                            t.players.remove(p)
                            t.budget += p.value
                            print(f"✅ Signed {p.name} for €{p.value:,}!")
                        else:
                            print("❌ Not enough budget!")
                        input("Press Enter to continue...")
                        return
    except:
        pass

def process_season_end(game: FootballDAMA):
    """Process end of season"""
    clear_screen()
    print_header("END OF SEASON")
    
    table = game.get_ligue1_table()
    
    print("📊 FINAL LIGUE 1 STANDINGS")
    display_table(table)
    
    # Champion
    champion = table[0]
    print(f"\n🏆 CHAMPIONS: {champion.name}!")
    
    # Relegation
    relegated = table[-3:]
    print(f"\n⬇️  RELEGATED: {', '.join(t.name for t in relegated)}")
    
    # Promotion from Ligue 2 (simplified)
    print(f"\n⬆️  PROMOTED: Top 3 from Ligue 2")
    
    # Check manager career end
    if game.mode == Mode.MANAGER_CAREER:
        manager_team = game.manager_career_data['team']
        if champion.name == manager_team:
            game.game_ended = True
            game.end_reason = f"🏆 CONGRATULATIONS! You won Ligue 1 with {manager_team}!"
        else:
            print(f"\nYour team finished {table.index(next(t for t in table if t.name == manager_team)) + 1}th")
            response = input("Continue to next season? (y/n): ").strip().lower()
            if response == 'y':
                # Reset for new season
                for team in game.ligue1_teams.values():
                    team.points = 0
                    team.played = 0
                    team.won = 0
                    team.drawn = 0
                    team.lost = 0
                    team.goals_for = 0
                    team.goals_against = 0
                    team.goal_difference = 0
                    team.form = []
                game.current_matchday = 1
                game.manager_career_data['seasons'] += 1
                return
    
    # Save season history
    season = Season(year=game.season_year)
    game.seasons_history.append(season)
    
    # New season
    game.season_year += 1
    game.current_matchday = 1
    
    input("\nPress Enter to start new season...")

def game_over_screen(game: FootballDAMA):
    """Display game over screen"""
    clear_screen()
    print_header("CAREER COMPLETE!")
    
    print(game.end_reason)
    
    if game.mode == Mode.PLAYER_CAREER:
        player = game.player_career_data
        print(f"\n📊 FINAL STATS:")
        print(f"  Matches: {player['matches']}")
        print(f"  Goals: {player['goals']}")
        print(f"  Assists: {player['assists']}")
        print(f"  Final Rating: {player['rating']}")
        print(f"  France Caps: {player['france_caps']}")
    else:
        manager = game.manager_career_data
        print(f"\n📊 MANAGERIAL RECORD:")
        print(f"  Wins: {manager['wins']}")
        print(f"  Draws: {manager['draws']}")
        print(f"  Losses: {manager['losses']}")
        print(f"  Seasons: {manager['seasons']}")
    
    print("\n🎮 Thank you for playing The Football DAMA!")
    
    # Save final stats
    game.save_game('final_save.json')
    print("💾 Final stats saved to final_save.json")
    
    input("\nPress Enter to return to main menu...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
