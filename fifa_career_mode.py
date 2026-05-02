#!/usr/bin/env python3
"""
FIFA CAREER MODE - ENGLAND DEMO
Features:
- Premier League (Division 1) - All 20 teams with real players
- Championship (Division 2) - All 24 teams with real players
- Realistic player attributes, ages, positions
- Transfer system, matches, leagues, cups
- Player career mode
"""

import random
from datetime import datetime
from typing import List, Dict, Optional
import json

# ============================================================================
# PLAYER DATA - REAL PLAYERS WITH ATTRIBUTES
# ============================================================================

class Player:
    def __init__(self, name: str, age: int, position: str, overall: int, 
                 potential: int, nationality: str, value: float, wage: float):
        self.name = name
        self.age = age
        self.position = position  # GK, CB, LB, RB, CDM, CM, CAM, LW, RW, ST
        self.overall = overall
        self.potential = potential
        self.nationality = nationality
        self.value = value  # in millions
        self.wage = wage  # weekly in thousands
        self.form = 5  # 1-10 scale
        self.matches_played = 0
        self.goals = 0
        self.assists = 0
        
    def __str__(self):
        return f"{self.name} ({self.age}) - {self.position} - OVR: {self.overall} - POT: {self.potential}"
    
    def to_dict(self):
        return {
            'name': self.name,
            'age': self.age,
            'position': self.position,
            'overall': self.overall,
            'potential': self.potential,
            'nationality': self.nationality,
            'value': self.value,
            'wage': self.wage,
            'form': self.form,
            'matches_played': self.matches_played,
            'goals': self.goals,
            'assists': self.assists
        }

# ============================================================================
# TEAM DATA - PREMIER LEAGUE & CHAMPIONSHIP
# ============================================================================

class Team:
    def __init__(self, name: str, division: int, stadium: str, manager: str):
        self.name = name
        self.division = division  # 1 = Premier League, 2 = Championship
        self.stadium = stadium
        self.manager = manager
        self.players: List[Player] = []
        self.points = 0
        self.played = 0
        self.won = 0
        self.drawn = 0
        self.lost = 0
        self.gf = 0
        self.ga = 0
        
    def add_player(self, player: Player):
        self.players.append(player)
        
    def get_squad_value(self):
        return sum(p.value for p in self.players)
    
    def get_average_rating(self):
        if not self.players:
            return 0
        return sum(p.overall for p in self.players) / len(self.players)
    
    def __str__(self):
        return f"{self.name} ({self.stadium}) - Manager: {self.manager}"

# ============================================================================
# REAL TEAM AND PLAYER DATABASE
# ============================================================================

def create_premier_league_teams() -> List[Team]:
    """Create all 20 Premier League teams with real players"""
    teams = []
    
    # Arsenal
    arsenal = Team("Arsenal", 1, "Emirates Stadium", "Mikel Arteta")
    arsenal.add_player(Player("David Raya", 28, "GK", 86, 87, "Spain", 35, 120))
    arsenal.add_player(Player("William Saliba", 23, "CB", 87, 92, "France", 75, 150))
    arsenal.add_player(Player("Gabriel Magalhães", 26, "CB", 86, 88, "Brazil", 60, 140))
    arsenal.add_player(Player("Ben White", 26, "RB", 84, 86, "England", 50, 110))
    arsenal.add_player(Player("Jurriën Timber", 23, "LB", 82, 87, "Netherlands", 45, 95))
    arsenal.add_player(Player("Declan Rice", 25, "CDM", 88, 91, "England", 110, 250))
    arsenal.add_player(Player("Martin Ødegaard", 25, "CAM", 89, 91, "Norway", 100, 240))
    arsenal.add_player(Player("Bukayo Saka", 22, "RW", 88, 93, "England", 130, 280))
    arsenal.add_player(Player("Gabriel Martinelli", 23, "LW", 85, 90, "Brazil", 80, 180))
    arsenal.add_player(Player("Kai Havertz", 25, "ST", 84, 87, "Germany", 65, 190))
    arsenal.add_player(Player("Gabriel Jesus", 27, "ST", 83, 84, "Brazil", 55, 170))
    teams.append(arsenal)
    
    # Aston Villa
    villa = Team("Aston Villa", 1, "Villa Park", "Unai Emery")
    villa.add_player(Player("Emiliano Martínez", 31, "GK", 88, 88, "Argentina", 40, 140))
    villa.add_player(Player("Ezri Konsa", 26, "CB", 82, 85, "England", 35, 90))
    villa.add_player(Player("Pau Torres", 27, "CB", 84, 86, "Spain", 45, 110))
    villa.add_player(Player("Lucas Digne", 30, "LB", 83, 83, "France", 25, 85))
    villa.add_player(Player("Matty Cash", 26, "RB", 81, 83, "Poland", 28, 75))
    villa.add_player(Player("Douglas Luiz", 26, "CM", 85, 87, "Brazil", 60, 130))
    villa.add_player(Player("John McGinn", 29, "CM", 83, 83, "Scotland", 35, 95))
    villa.add_player(Player("Leon Bailey", 26, "RW", 83, 85, "Jamaica", 40, 100))
    villa.add_player(Player("Moussa Diaby", 24, "LW", 84, 87, "France", 55, 120))
    villa.add_player(Player("Ollie Watkins", 28, "ST", 86, 87, "England", 70, 160))
    teams.append(villa)
    
    # Bournemouth
    bournemouth = Team("Bournemouth", 1, "Vitality Stadium", "Andoni Iraola")
    bournemouth.add_player(Player("Neto", 34, "GK", 82, 82, "Brazil", 8, 60))
    bournemouth.add_player(Player("Illia Zabarnyi", 21, "CB", 80, 86, "Ukraine", 25, 50))
    bournemouth.add_player(Player("Marcos Senesi", 27, "CB", 81, 83, "Argentina", 22, 55))
    bournemouth.add_player(Player("Milos Kerkez", 20, "LB", 78, 85, "Hungary", 20, 40))
    bournemouth.add_player(Player("Adam Smith", 33, "RB", 79, 79, "England", 5, 45))
    bournemouth.add_player(Player("Lewis Cook", 27, "CDM", 81, 83, "England", 25, 60))
    bournemouth.add_player(Player("Ryan Christie", 29, "CM", 80, 81, "Scotland", 18, 50))
    bournemouth.add_player(Player("Antoine Semenyo", 24, "RW", 80, 84, "Ghana", 25, 55))
    bournemouth.add_player(Player("Marcus Tavernier", 25, "LW", 79, 82, "England", 20, 50))
    bournemouth.add_player(Player("Dominic Solanke", 26, "ST", 83, 85, "England", 45, 90))
    teams.append(bournemouth)
    
    # Brentford
    brentford = Team("Brentford", 1, "Gtech Community Stadium", "Thomas Frank")
    brentford.add_player(Player("Mark Flekken", 30, "GK", 83, 84, "Netherlands", 18, 65))
    brentford.add_player(Player("Nathan Collins", 23, "CB", 81, 86, "Ireland", 28, 60))
    brentford.add_player(Player("Ethan Pinnock", 31, "CB", 80, 80, "Jamaica", 15, 50))
    brentford.add_player(Player("Rico Henry", 26, "LB", 81, 84, "England", 25, 65))
    brentford.add_player(Player("Kristoffer Ajer", 26, "RB", 80, 83, "Norway", 22, 55))
    brentford.add_player(Player("Christian Nørgaard", 30, "CDM", 82, 82, "Denmark", 20, 60))
    brentford.add_player(Player("Vitaly Janelt", 26, "CM", 80, 83, "Germany", 22, 55))
    brentford.add_player(Player("Bryan Mbeumo", 24, "RW", 82, 85, "Cameroon", 35, 75))
    brentford.add_player(Player("Yoane Wissa", 27, "LW", 81, 83, "DR Congo", 28, 65))
    brentford.add_player(Player("Ivan Toney", 28, "ST", 84, 85, "England", 55, 120))
    teams.append(brentford)
    
    # Brighton
    brighton = Team("Brighton & Hove Albion", 1, "Amex Stadium", "Roberto De Zerbi")
    brighton.add_player(Player("Jason Steele", 33, "GK", 81, 81, "England", 10, 50))
    brighton.add_player(Player("Lewis Dunk", 32, "CB", 83, 83, "England", 20, 70))
    brighton.add_player(Player("Jan Paul van Hecke", 24, "CB", 81, 85, "Netherlands", 25, 55))
    brighton.add_player(Player("Pervis Estupiñán", 26, "LB", 83, 86, "Ecuador", 35, 80))
    brighton.add_player(Player("Tariq Lamptey", 23, "RB", 79, 84, "England", 20, 45))
    brighton.add_player(Player("Pascal Groß", 32, "CM", 83, 83, "Germany", 18, 70))
    brighton.add_player(Player("Billy Gilmour", 23, "CDM", 80, 86, "Scotland", 28, 60))
    brighton.add_player(Player("Kaoru Mitoma", 27, "LW", 84, 86, "Japan", 50, 100))
    brighton.add_player(Player("Simon Adingra", 22, "RW", 80, 85, "Ivory Coast", 30, 65))
    brighton.add_player(Player("João Pedro", 22, "ST", 83, 88, "Brazil", 45, 90))
    teams.append(brighton)
    
    # Burnley
    burnley = Team("Burnley", 1, "Turf Moor", "Vincent Kompany")
    burnley.add_player(Player("James Trafford", 21, "GK", 76, 83, "England", 12, 45))
    burnley.add_player(Player("Dara O'Shea", 25, "CB", 78, 81, "Republic of Ireland", 10, 50))
    burnley.add_player(Player("Jordan Beyer", 23, "CB", 77, 81, "Germany", 10, 45))
    burnley.add_player(Player("Charlie Taylor", 30, "LB", 78, 79, "England", 8, 45))
    burnley.add_player(Player("Connor Roberts", 28, "RB", 78, 79, "Wales", 8, 45))
    burnley.add_player(Player("Josh Cullen", 27, "CDM", 79, 81, "Republic of Ireland", 12, 55))
    burnley.add_player(Player("Sander Berge", 25, "CM", 80, 82, "Norway", 15, 60))
    burnley.add_player(Player("Wilson Odobert", 19, "LW", 76, 83, "France", 12, 50))
    burnley.add_player(Player("Luca Koleosho", 19, "RW", 75, 82, "USA", 10, 45))
    burnley.add_player(Player("Zeki Amdouni", 23, "ST", 78, 82, "Switzerland", 14, 55))
    teams.append(burnley)
    
    # Chelsea
    chelsea = Team("Chelsea", 1, "Stamford Bridge", "Mauricio Pochettino")
    chelsea.add_player(Player("Robert Sánchez", 26, "GK", 82, 85, "Spain", 30, 90))
    chelsea.add_player(Player("Thiago Silva", 39, "CB", 84, 84, "Brazil", 8, 100))
    chelsea.add_player(Player("Levi Colwill", 21, "CB", 81, 88, "England", 45, 80))
    chelsea.add_player(Player("Reece James", 24, "RB", 86, 89, "England", 70, 180))
    chelsea.add_player(Player("Marc Cucurella", 25, "LB", 82, 85, "Spain", 35, 90))
    chelsea.add_player(Player("Moisés Caicedo", 22, "CDM", 84, 90, "Ecuador", 80, 150))
    chelsea.add_player(Player("Enzo Fernández", 23, "CM", 85, 90, "Argentina", 85, 160))
    chelsea.add_player(Player("Cole Palmer", 22, "CAM", 84, 89, "England", 65, 120))
    chelsea.add_player(Player("Raheem Sterling", 29, "LW", 84, 84, "England", 45, 180))
    chelsea.add_player(Player("Nicolas Jackson", 22, "ST", 81, 86, "Senegal", 40, 85))
    teams.append(chelsea)
    
    # Crystal Palace
    palace = Team("Crystal Palace", 1, "Selhurst Park", "Roy Hodgson")
    palace.add_player(Player("Sam Johnstone", 31, "GK", 81, 82, "England", 15, 55))
    palace.add_player(Player("Marc Guéhi", 24, "CB", 83, 87, "England", 45, 80))
    palace.add_player(Player("Joachim Andersen", 27, "CB", 82, 84, "Denmark", 30, 70))
    palace.add_player(Player("Tyrick Mitchell", 24, "LB", 81, 84, "England", 25, 60))
    palace.add_player(Player("Joel Ward", 34, "RB", 78, 78, "England", 5, 40))
    palace.add_player(Player("Cheick Doucouré", 24, "CDM", 81, 85, "Mali", 28, 65))
    palace.add_player(Player("Eberechi Eze", 25, "CAM", 83, 86, "England", 45, 90))
    palace.add_player(Player("Michael Olise", 22, "RW", 83, 88, "France", 50, 95))
    palace.add_player(Player("Jordan Ayew", 32, "LW", 79, 79, "Ghana", 12, 55))
    palace.add_player(Player("Jean-Philippe Mateta", 26, "ST", 81, 83, "France", 25, 70))
    teams.append(palace)
    
    # Everton
    everton = Team("Everton", 1, "Goodison Park", "Sean Dyche")
    everton.add_player(Player("Jordan Pickford", 30, "GK", 84, 85, "England", 30, 100))
    everton.add_player(Player("James Tarkowski", 32, "CB", 82, 82, "England", 18, 70))
    everton.add_player(Player("Jarrad Branthwaite", 21, "CB", 80, 87, "England", 35, 60))
    everton.add_player(Player("Vitaliy Mykolenko", 25, "LB", 80, 83, "Ukraine", 20, 55))
    everton.add_player(Player("Séamus Coleman", 35, "RB", 78, 78, "Ireland", 4, 45))
    everton.add_player(Player("Idrissa Gueye", 34, "CDM", 81, 81, "Senegal", 10, 65))
    everton.add_player(Player("James Garner", 23, "CM", 80, 84, "England", 25, 60))
    everton.add_player(Player("Dwight McNeil", 24, "LW", 81, 84, "England", 28, 70))
    everton.add_player(Player("Jack Harrison", 27, "RW", 81, 83, "England", 25, 75))
    everton.add_player(Player("Dominic Calvert-Lewin", 27, "ST", 81, 83, "England", 30, 80))
    teams.append(everton)
    
    # Fulham
    fulham = Team("Fulham", 1, "Craven Cottage", "Marco Silva")
    fulham.add_player(Player("Bernd Leno", 32, "GK", 83, 83, "Germany", 18, 70))
    fulham.add_player(Player("Tim Ream", 35, "CB", 80, 80, "USA", 8, 50))
    fulham.add_player(Player("Calvin Bassey", 24, "CB", 81, 85, "Nigeria", 30, 65))
    fulham.add_player(Player("Antonee Robinson", 26, "LB", 82, 85, "USA", 28, 70))
    fulham.add_player(Player("Kenny Tete", 28, "RB", 80, 81, "Netherlands", 15, 55))
    fulham.add_player(Player("João Palhinha", 28, "CDM", 85, 86, "Portugal", 50, 100))
    fulham.add_player(Player("Harrison Reed", 29, "CM", 79, 80, "England", 12, 50))
    fulham.add_player(Player("Alex Iwobi", 28, "CAM", 82, 83, "Nigeria", 30, 85))
    fulham.add_player(Player("Willian", 35, "RW", 80, 80, "Brazil", 6, 60))
    fulham.add_player(Player("Rodrigo Muniz", 23, "ST", 79, 84, "Brazil", 20, 55))
    teams.append(fulham)
    
    # Liverpool
    liverpool = Team("Liverpool", 1, "Anfield", "Jürgen Klopp")
    liverpool.add_player(Player("Alisson Becker", 31, "GK", 89, 89, "Brazil", 55, 180))
    liverpool.add_player(Player("Virgil van Dijk", 32, "CB", 89, 89, "Netherlands", 45, 200))
    liverpool.add_player(Player("Ibrahima Konaté", 25, "CB", 84, 88, "France", 50, 130))
    liverpool.add_player(Player("Andy Robertson", 30, "LB", 86, 86, "Scotland", 40, 150))
    liverpool.add_player(Player("Trent Alexander-Arnold", 25, "RB", 87, 90, "England", 80, 180))
    liverpool.add_player(Player("Alexis Mac Allister", 25, "CM", 85, 88, "Argentina", 65, 140))
    liverpool.add_player(Player("Dominik Szoboszlai", 23, "CM", 84, 89, "Hungary", 60, 130))
    liverpool.add_player(Player("Mohamed Salah", 31, "RW", 89, 89, "Egypt", 65, 350))
    liverpool.add_player(Player("Luis Díaz", 27, "LW", 85, 87, "Colombia", 60, 150))
    liverpool.add_player(Player("Darwin Núñez", 24, "ST", 84, 88, "Uruguay", 70, 160))
    teams.append(liverpool)
    
    # Luton Town
    luton = Team("Luton Town", 1, "Kenilworth Road", "Rob Edwards")
    luton.add_player(Player("Thomas Kaminski", 31, "GK", 80, 81, "Belgium", 10, 40))
    luton.add_player(Player("Teden Mengi", 22, "CB", 77, 83, "England", 12, 35))
    luton.add_player(Player("Tom Lockyer", 29, "CB", 79, 80, "Wales", 10, 40))
    luton.add_player(Player("Amari'i Bell", 29, "LB", 77, 78, "Jamaica", 8, 35))
    luton.add_player(Player("Alfie Doughty", 24, "RB", 76, 80, "England", 10, 30))
    luton.add_player(Player("Ross Barkley", 30, "CM", 80, 80, "England", 15, 60))
    luton.add_player(Player("Marvelous Nakamba", 30, "CDM", 78, 79, "Zimbabwe", 8, 40))
    luton.add_player(Player("Tahith Chong", 24, "RW", 77, 81, "Netherlands", 12, 40))
    luton.add_player(Player("Andros Townsend", 32, "LW", 78, 78, "England", 6, 45))
    luton.add_player(Player("Carlton Morris", 28, "ST", 78, 80, "England", 12, 45))
    teams.append(luton)
    
    # Manchester City
    city = Team("Manchester City", 1, "Etihad Stadium", "Pep Guardiola")
    city.add_player(Player("Ederson", 30, "GK", 88, 88, "Brazil", 50, 180))
    city.add_player(Player("Rúben Dias", 27, "CB", 88, 90, "Portugal", 75, 180))
    city.add_player(Player("John Stones", 29, "CB", 85, 86, "England", 50, 150))
    city.add_player(Player("Kyle Walker", 33, "RB", 84, 84, "England", 25, 140))
    city.add_player(Player("Josko Gvardiol", 22, "LB", 84, 90, "Croatia", 70, 140))
    city.add_player(Player("Rodri", 27, "CDM", 89, 91, "Spain", 100, 220))
    city.add_player(Player("Kevin De Bruyne", 32, "CAM", 91, 91, "Belgium", 70, 300))
    city.add_player(Player("Bernardo Silva", 29, "RW", 87, 88, "Portugal", 70, 200))
    city.add_player(Player("Phil Foden", 23, "LW", 87, 92, "England", 100, 220))
    city.add_player(Player("Erling Haaland", 23, "ST", 91, 95, "Norway", 180, 350))
    teams.append(city)
    
    # Manchester United
    united = Team("Manchester United", 1, "Old Trafford", "Erik ten Hag")
    united.add_player(Player("André Onana", 28, "GK", 85, 87, "Cameroon", 40, 140))
    united.add_player(Player("Raphaël Varane", 30, "CB", 85, 85, "France", 35, 160))
    united.add_player(Player("Lisandro Martínez", 26, "CB", 85, 88, "Argentina", 50, 140))
    united.add_player(Player("Luke Shaw", 28, "LB", 83, 84, "England", 35, 130))
    united.add_player(Player("Diogo Dalot", 25, "RB", 82, 86, "Portugal", 40, 100))
    united.add_player(Player("Casemiro", 32, "CDM", 87, 87, "Brazil", 40, 200))
    united.add_player(Player("Bruno Fernandes", 29, "CAM", 88, 89, "Portugal", 75, 240))
    united.add_player(Player("Marcus Rashford", 26, "LW", 86, 89, "England", 80, 250))
    united.add_player(Player("Antony", 24, "RW", 81, 85, "Brazil", 45, 150))
    united.add_player(Player("Rasmus Højlund", 21, "ST", 81, 88, "Denmark", 55, 120))
    teams.append(united)
    
    # Newcastle United
    newcastle = Team("Newcastle United", 1, "St James' Park", "Eddie Howe")
    newcastle.add_player(Player("Nick Pope", 31, "GK", 85, 85, "England", 30, 100))
    newcastle.add_player(Player("Fabian Schär", 32, "CB", 83, 83, "Switzerland", 20, 80))
    newcastle.add_player(Player("Sven Botman", 24, "CB", 84, 88, "Netherlands", 50, 110))
    newcastle.add_player(Player("Dan Burn", 31, "LB", 80, 80, "England", 15, 65))
    newcastle.add_player(Player("Kieran Trippier", 33, "RB", 84, 84, "England", 20, 110))
    newcastle.add_player(Player("Bruno Guimarães", 26, "CDM", 86, 89, "Brazil", 75, 150))
    newcastle.add_player(Player("Joelinton", 27, "CM", 82, 84, "Brazil", 40, 110))
    newcastle.add_player(Player("Anthony Gordon", 23, "LW", 82, 86, "England", 50, 100))
    newcastle.add_player(Player("Miguel Almirón", 30, "RW", 81, 82, "Paraguay", 30, 90))
    newcastle.add_player(Player("Alexander Isak", 24, "ST", 85, 88, "Sweden", 70, 140))
    teams.append(newcastle)
    
    # Nottingham Forest
    forest = Team("Nottingham Forest", 1, "City Ground", "Nuno Espírito Santo")
    forest.add_player(Player("Matt Turner", 29, "GK", 80, 82, "USA", 12, 50))
    forest.add_player(Player("Willy Boly", 33, "CB", 80, 80, "France", 10, 55))
    forest.add_player(Player("Murillo", 21, "CB", 80, 86, "Brazil", 30, 55))
    forest.add_player(Player("Ola Aina", 27, "LB", 79, 81, "Nigeria", 15, 50))
    forest.add_player(Player("Neco Williams", 23, "RB", 79, 83, "Wales", 18, 50))
    forest.add_player(Player("Danilo", 22, "CDM", 79, 85, "Brazil", 25, 55))
    forest.add_player(Player("Ryan Yates", 26, "CM", 78, 80, "England", 12, 45))
    forest.add_player(Player("Morgan Gibbs-White", 24, "CAM", 81, 85, "England", 35, 75))
    forest.add_player(Player("Callum Hudson-Odoi", 23, "LW", 80, 84, "England", 25, 65))
    forest.add_player(Player("Chris Wood", 32, "ST", 81, 81, "New Zealand", 12, 70))
    teams.append(forest)
    
    # Sheffield United
    sheffield = Team("Sheffield United", 1, "Bramall Lane", "Chris Wilder")
    sheffield.add_player(Player("Wes Foderingham", 33, "GK", 79, 79, "England", 6, 40))
    sheffield.add_player(Player("Jack Robinson", 30, "CB", 78, 79, "England", 8, 40))
    sheffield.add_player(Player("Auston Trusty", 25, "CB", 77, 81, "USA", 10, 35))
    sheffield.add_player(Player("Max Lowe", 27, "LB", 76, 78, "England", 8, 35))
    sheffield.add_player(Player("Jayden Bogle", 23, "RB", 77, 80, "England", 10, 40))
    sheffield.add_player(Player("Oliver Norwood", 32, "CDM", 78, 78, "Northern Ireland", 6, 45))
    sheffield.add_player(Player("Gustavo Hamer", 26, "CM", 79, 82, "Netherlands", 15, 50))
    sheffield.add_player(Player("James McAtee", 21, "CAM", 77, 83, "England", 15, 40))
    sheffield.add_player(Player("Ben Osborn", 29, "LW", 76, 77, "England", 6, 35))
    sheffield.add_player(Player("Cameron Archer", 22, "ST", 77, 82, "England", 15, 45))
    teams.append(sheffield)
    
    # Tottenham
    spurs = Team("Tottenham Hotspur", 1, "Tottenham Hotspur Stadium", "Ange Postecoglou")
    spurs.add_player(Player("Guglielmo Vicario", 27, "GK", 83, 85, "Italy", 28, 80))
    spurs.add_player(Player("Cristian Romero", 26, "CB", 85, 88, "Argentina", 55, 130))
    spurs.add_player(Player("Micky van de Ven", 23, "CB", 83, 88, "Netherlands", 45, 100))
    spurs.add_player(Player("Destiny Udogie", 21, "LB", 80, 86, "Italy", 30, 70))
    spurs.add_player(Player("Pedro Porro", 24, "RB", 83, 86, "Spain", 40, 95))
    spurs.add_player(Player("Yves Bissouma", 27, "CDM", 82, 84, "Mali", 35, 90))
    spurs.add_player(Player("Pape Matar Sarr", 21, "CM", 80, 86, "Senegal", 35, 75))
    spurs.add_player(Player("James Maddison", 27, "CAM", 85, 86, "England", 55, 140))
    spurs.add_player(Player("Dejan Kulusevski", 24, "RW", 84, 87, "Sweden", 55, 120))
    spurs.add_player(Player("Son Heung-min", 31, "LW", 87, 87, "South Korea", 50, 200))
    spurs.add_player(Player("Richarlison", 26, "ST", 83, 85, "Brazil", 50, 130))
    teams.append(spurs)
    
    # West Ham
    westham = Team("West Ham United", 1, "London Stadium", "David Moyes")
    westham.add_player(Player("Alphonse Areola", 31, "GK", 82, 82, "France", 15, 70))
    westham.add_player(Player("Kurt Zouma", 29, "CB", 81, 82, "France", 25, 90))
    westham.add_player(Player("Nayef Aguerd", 28, "CB", 81, 83, "Morocco", 28, 75))
    westham.add_player(Player("Emerson Palmieri", 29, "LB", 81, 82, "Italy", 20, 70))
    westham.add_player(Player("Vladimír Coufal", 31, "RB", 81, 81, "Czech Republic", 15, 65))
    westham.add_player(Player("Edson Álvarez", 26, "CDM", 83, 85, "Mexico", 40, 95))
    westham.add_player(Player("Tomáš Souček", 29, "CM", 82, 83, "Czech Republic", 30, 85))
    westham.add_player(Player("Lucas Paquetá", 26, "CAM", 84, 86, "Brazil", 55, 120))
    westham.add_player(Player("Jarrod Bowen", 27, "RW", 84, 86, "England", 55, 130))
    westham.add_player(Player("Mohammed Kudus", 23, "LW", 82, 87, "Ghana", 45, 95))
    westham.add_player(Player("Michail Antonio", 34, "ST", 80, 80, "Jamaica", 12, 80))
    teams.append(westham)
    
    # Wolves
    wolves = Team("Wolverhampton Wanderers", 1, "Molineux Stadium", "Gary O'Neil")
    wolves.add_player(Player("José Sá", 31, "GK", 83, 84, "Portugal", 20, 75))
    wolves.add_player(Player("Max Kilman", 26, "CB", 82, 85, "England", 35, 75))
    wolves.add_player(Player("Craig Dawson", 33, "CB", 80, 80, "England", 10, 55))
    wolves.add_player(Player("Rayan Aït-Nouri", 22, "LB", 81, 86, "France", 35, 70))
    wolves.add_player(Player("Nélson Semedo", 30, "RB", 82, 82, "Portugal", 20, 75))
    wolves.add_player(Player("João Gomes", 23, "CDM", 81, 86, "Brazil", 40, 80))
    wolves.add_player(Player("Mario Lemina", 30, "CM", 81, 82, "Gabon", 22, 70))
    wolves.add_player(Player("Pedro Neto", 24, "RW", 82, 86, "Portugal", 45, 90))
    wolves.add_player(Player("Matheus Cunha", 24, "CAM", 82, 85, "Brazil", 45, 95))
    wolves.add_player(Player("Hwang Hee-chan", 28, "ST", 81, 83, "South Korea", 30, 85))
    teams.append(wolves)
    
    return teams

def create_championship_teams() -> List[Team]:
    """Create all 24 Championship teams with real players"""
    teams = []
    
    # Birmingham City
    birmingham = Team("Birmingham City", 2, "St Andrew's", "Tony Mowbray")
    birmingham.add_player(Player("John Ruddy", 37, "GK", 78, 78, "England", 3, 35))
    birmingham.add_player(Player("Krystian Bielik", 26, "CB", 78, 81, "Poland", 10, 45))
    birmingham.add_player(Player("Dion Sanderson", 24, "CB", 76, 80, "England", 8, 35))
    birmingham.add_player(Player("Lee Buchanan", 23, "LB", 75, 80, "England", 8, 30))
    birmingham.add_player(Player("Ethan Laird", 22, "RB", 76, 81, "England", 10, 35))
    birmingham.add_player(Player("Tomoki Iwata", 26, "CDM", 77, 79, "Japan", 8, 40))
    birmingham.add_player(Player("Paik Seung-ho", 26, "CM", 77, 80, "South Korea", 10, 40))
    birmingham.add_player(Player("Juninho Bacuna", 27, "CM", 78, 80, "Curaçao", 10, 45))
    birmingham.add_player(Player("Siriki Dembélé", 27, "LW", 78, 80, "England", 12, 45))
    birmingham.add_player(Player("Jay Stansfield", 21, "ST", 76, 82, "England", 12, 40))
    teams.append(birmingham)
    
    # Blackburn Rovers
    blackburn = Team("Blackburn Rovers", 2, "Ewood Park", "Jon Dahl Tomasson")
    blackburn.add_player(Player("Aynsley Pears", 26, "GK", 77, 79, "England", 6, 35))
    blackburn.add_player(Player("Scott Wharton", 26, "CB", 77, 79, "England", 8, 40))
    blackburn.add_player(Player("Hayden Carter", 24, "CB", 76, 80, "England", 7, 35))
    blackburn.add_player(Player("Harry Pickering", 24, "LB", 77, 80, "England", 8, 40))
    blackburn.add_player(Player("Connor Bradley", 20, "RB", 74, 81, "Northern Ireland", 6, 25))
    blackburn.add_player(Player("Lewis Travis", 26, "CDM", 78, 80, "England", 10, 45))
    blackburn.add_player(Player("Sammie Szmodics", 28, "CM", 79, 81, "Republic of Ireland", 12, 55))
    blackburn.add_player(Player("Tyrhys Dolan", 22, "RW", 77, 82, "England", 12, 45))
    blackburn.add_player(Player("Sam Gallagher", 28, "ST", 78, 79, "England", 10, 50))
    teams.append(blackburn)
    
    # Bristol City
    bristol = Team("Bristol City", 2, "Ashton Gate", "Liam Manning")
    bristol.add_player(Player("Stefan Bajic", 22, "GK", 75, 81, "France", 6, 30))
    bristol.add_player(Player("Zak Vyner", 26, "CB", 76, 78, "England", 7, 35))
    bristol.add_player(Player("Rob Dickie", 28, "CB", 77, 78, "England", 8, 40))
    bristol.add_player(Player("George Tanner", 24, "RB", 76, 79, "England", 7, 35))
    bristol.add_player(Player("Naomichi Ueda", 29, "LB", 76, 77, "Japan", 6, 35))
    bristol.add_player(Player("Joe Williams", 27, "CDM", 77, 79, "England", 8, 40))
    bristol.add_player(Player("Jason Knight", 23, "CM", 77, 81, "Republic of Ireland", 10, 45))
    bristol.add_player(Player("Anis Mehmeti", 23, "RW", 76, 80, "England", 8, 40))
    bristol.add_player(Player("Tommy Conway", 22, "ST", 77, 82, "Scotland", 10, 45))
    teams.append(bristol)
    
    # Cardiff City
    cardiff = Team("Cardiff City", 2, "Cardiff City Stadium", "Erol Bulut")
    cardiff.add_player(Player("Jak Alnwick", 30, "GK", 76, 77, "England", 5, 35))
    cardiff.add_player(Player("Perry Ng", 27, "CB", 77, 79, "Wales", 8, 40))
    cardiff.add_player(Player("Mark McGuinness", 22, "CB", 76, 81, "Republic of Ireland", 8, 35))
    cardiff.add_player(Player("Jamilu Collins", 29, "LB", 76, 78, "Nigeria", 7, 40))
    cardiff.add_player(Player("Ryan Wintle", 27, "RB", 75, 77, "England", 6, 35))
    cardiff.add_player(Player("Aaron Ramsey", 33, "CM", 79, 79, "Wales", 10, 70))
    cardiff.add_player(Player("Joe Ralls", 30, "CM", 76, 77, "England", 6, 40))
    cardiff.add_player(Player("Rubin Colwill", 21, "CAM", 74, 80, "Wales", 6, 30))
    cardiff.add_player(Player("Kieffer Moore", 31, "ST", 78, 78, "Wales", 10, 50))
    teams.append(cardiff)
    
    # Coventry City
    coventry = Team("Coventry City", 2, "Coventry Building Society Arena", "Mark Robins")
    coventry.add_player(Player("Ben Wilson", 31, "GK", 78, 78, "England", 7, 40))
    coventry.add_player(Player("Bobby Thomas", 23, "CB", 77, 81, "England", 10, 40))
    coventry.add_player(Player("Luis Binks", 22, "CB", 76, 81, "England", 8, 35))
    coventry.add_player(Player("Jake Bidwell", 31, "LB", 78, 78, "England", 8, 45))
    coventry.add_player(Player("Milan van Ewijk", 23, "RB", 77, 81, "Netherlands", 10, 45))
    coventry.add_player(Player("Ben Sheaf", 26, "CDM", 78, 80, "England", 10, 50))
    coventry.add_player(Player("Josh Eccles", 23, "CM", 76, 80, "England", 8, 40))
    coventry.add_player(Player("Tatsuhiro Sakamoto", 27, "RW", 77, 79, "Japan", 8, 45))
    coventry.add_player(Player("Ellis Simms", 23, "ST", 77, 82, "England", 12, 50))
    teams.append(coventry)
    
    # Huddersfield Town
    huddersfield = Team("Huddersfield Town", 2, "John Smith's Stadium", "Darren Moore")
    huddersfield.add_player(Player("Lee Nicholls", 31, "GK", 77, 78, "England", 6, 40))
    huddersfield.add_player(Player("Michal Helik", 28, "CB", 78, 79, "Poland", 8, 45))
    huddersfield.add_player(Player("Tom Lees", 33, "CB", 77, 77, "England", 5, 40))
    huddersfield.add_player(Player("Ben Jackson", 23, "LB", 75, 79, "England", 6, 35))
    huddersfield.add_player(Player("Oliver Turton", 31, "RB", 76, 77, "England", 5, 35))
    huddersfield.add_player(Player("Jonathan Hogg", 35, "CDM", 76, 76, "England", 4, 35))
    huddersfield.add_player(Player("David Kasumu", 24, "CM", 75, 79, "England", 6, 35))
    huddersfield.add_player(Player("Jack Rudoni", 22, "CM", 76, 80, "England", 8, 40))
    huddersfield.add_player(Player("Sorba Thomas", 25, "RW", 77, 79, "Wales", 8, 45))
    huddersfield.add_player(Player("Delano Burgzorg", 25, "LW", 76, 78, "Netherlands", 7, 40))
    huddersfield.add_player(Player("Danny Ward", 30, "ST", 78, 78, "England", 8, 50))
    teams.append(huddersfield)
    
    # Hull City
    hull = Team("Hull City", 2, "MKM Stadium", "Liam Rosenior")
    hull.add_player(Player("Ivor Pandur", 24, "GK", 77, 81, "Croatia", 8, 40))
    hull.add_player(Player("Alfie Jones", 26, "CB", 77, 79, "England", 7, 40))
    hull.add_player(Player("Liam Delap", 21, "ST", 76, 83, "England", 12, 45))
    hull.add_player(Player("Reggie Slater", 23, "CB", 75, 79, "England", 6, 35))
    hull.add_player(Player("Jacob Greaves", 23, "CB", 78, 82, "England", 12, 50))
    hull.add_player(Player("Ryan Giles", 24, "LB", 78, 81, "England", 10, 50))
    hull.add_player(Player("Jean Michaël Seri", 32, "CM", 79, 79, "Ivory Coast", 8, 55))
    hull.add_player(Player("Ozan Tufan", 29, "CM", 78, 79, "Turkey", 8, 50))
    hull.add_player(Player("Abu Kamara", 24, "RW", 76, 80, "Sierra Leone", 8, 40))
    teams.append(hull)
    
    # Ipswich Town
    ipswich = Team("Ipswich Town", 2, "Portman Road", "Kieran McKenna")
    ipswich.add_player(Player("Christian Walton", 28, "GK", 78, 80, "England", 8, 45))
    ipswich.add_player(Player("Luke Woolfenden", 25, "CB", 77, 80, "England", 8, 40))
    ipswich.add_player(Player("Cameron Burgess", 28, "CB", 78, 79, "Australia", 8, 45))
    ipswich.add_player(Player("Leif Davis", 24, "LB", 78, 82, "England", 12, 50))
    ipswich.add_player(Player("Axel Tuanzebe", 26, "RB", 77, 79, "England", 8, 45))
    ipswich.add_player(Player("Sam Morsy", 32, "CDM", 79, 79, "Egypt", 8, 50))
    ipswich.add_player(Player("Massimo Luongo", 31, "CM", 78, 78, "Australia", 7, 45))
    ipswich.add_player(Player("Wes Burns", 29, "RW", 77, 78, "Wales", 7, 45))
    ipswich.add_player(Player("Nathan Broadhead", 26, "LW", 78, 80, "Wales", 10, 50))
    ipswich.add_player(Player("Freddie Ladapo", 31, "ST", 77, 78, "Republic of Ireland", 7, 45))
    teams.append(ipswich)
    
    # Leeds United
    leeds = Team("Leeds United", 2, "Elland Road", "Daniel Farke")
    leeds.add_player(Player("Illan Meslier", 24, "GK", 80, 85, "France", 18, 60))
    leeds.add_player(Player("Joe Rodon", 26, "CB", 79, 82, "Wales", 15, 55))
    leeds.add_player(Player("Pascal Struijk", 24, "CB", 79, 83, "Netherlands", 18, 60))
    leeds.add_player(Player("Junior Firpo", 27, "LB", 79, 81, "Dominican Republic", 12, 55))
    leeds.add_player(Player("Archie Gray", 18, "RB", 74, 84, "England", 12, 40))
    leeds.add_player(Player("Ethan Ampadu", 23, "CDM", 79, 83, "Wales", 15, 60))
    leeds.add_player(Player("Glen Kamara", 28, "CM", 80, 81, "Finland", 15, 65))
    leeds.add_player(Player("Crysencio Summerville", 22, "LW", 80, 84, "Netherlands", 20, 70))
    leeds.add_player(Player("Wilfried Gnonto", 20, "RW", 78, 85, "Italy", 20, 60))
    leeds.add_player(Player("Georginio Rutter", 22, "ST", 79, 84, "France", 22, 70))
    teams.append(leeds)
    
    # Leicester City
    leicester = Team("Leicester City", 2, "King Power Stadium", "Enzo Maresca")
    leicester.add_player(Player("Mads Hermansen", 24, "GK", 79, 84, "Denmark", 15, 55))
    leicester.add_player(Player("Wout Faes", 26, "CB", 80, 83, "Belgium", 20, 65))
    leicester.add_player(Player("Jannik Vestergaard", 31, "CB", 80, 80, "Denmark", 12, 60))
    leicester.add_player(Player("James Justin", 26, "RB", 80, 83, "England", 22, 70))
    leicester.add_player(Player("Victor Kristiansen", 21, "LB", 78, 84, "Denmark", 18, 55))
    leicester.add_player(Player("Harry Winks", 28, "CDM", 80, 81, "England", 18, 70))
    leicester.add_player(Player("Kiernan Dewsbury-Hall", 25, "CM", 80, 83, "England", 22, 70))
    leicester.add_player(Player("Abdul Fatawu", 20, "RW", 77, 84, "Ghana", 15, 50))
    leicester.add_player(Player("Stephy Mavididi", 26, "LW", 79, 82, "England", 18, 60))
    leicester.add_player(Player("Jamie Vardy", 37, "ST", 80, 80, "England", 8, 80))
    teams.append(leicester)
    
    # Middlesbrough
    middlesbrough = Team("Middlesbrough", 2, "Riverside Stadium", "Michael Carrick")
    middlesbrough.add_player(Player("Seny Dieng", 29, "GK", 78, 79, "Senegal", 8, 45))
    middlesbrough.add_player(Player("Dael Fry", 26, "CB", 78, 80, "England", 10, 50))
    middlesbrough.add_player(Player("Rav van den Berg", 20, "CB", 75, 82, "Netherlands", 10, 45))
    middlesbrough.add_player(Player("Lukas Engel", 25, "LB", 77, 80, "Denmark", 10, 50))
    middlesbrough.add_player(Player("Tommy Smith", 32, "RB", 77, 77, "England", 6, 45))
    middlesbrough.add_player(Player("Jonny Howson", 35, "CDM", 78, 78, "England", 6, 50))
    middlesbrough.add_player(Player("Hayden Hackney", 22, "CM", 76, 82, "England", 10, 45))
    middlesbrough.add_player(Player("Isaiah Jones", 24, "RW", 78, 81, "England", 12, 55))
    middlesbrough.add_player(Player("Emmanuel Latte Lath", 25, "ST", 78, 81, "Ivory Coast", 12, 55))
    teams.append(middlesbrough)
    
    # Millwall
    millwall = Team("Millwall", 2, "The Den", "Gary Rowett")
    millwall.add_player(Player("Bartosz Białkowski", 36, "GK", 76, 76, "Poland", 4, 35))
    millwall.add_player(Player("Japhet Tanganga", 25, "CB", 78, 82, "England", 12, 50))
    millwall.add_player(Player("Shaun Hutchinson", 33, "CB", 76, 76, "Republic of Ireland", 5, 40))
    millwall.add_player(Player("Murray Wallace", 31, "LB", 76, 77, "Scotland", 6, 40))
    millwall.add_player(Player("George Honeyman", 29, "RB", 76, 78, "England", 7, 45))
    millwall.add_player(Player("Joe Bryan", 30, "LM", 77, 78, "England", 7, 45))
    millwall.add_player(Player("Romain Esse", 19, "RM", 73, 81, "England", 6, 30))
    millwall.add_player(Player("Zian Flemming", 25, "CAM", 77, 80, "Netherlands", 10, 50))
    millwall.add_player(Player("Duncan Watmore", 30, "ST", 77, 78, "England", 8, 50))
    teams.append(millwall)
    
    # Norwich City
    norwich = Team("Norwich City", 2, "Carrow Road", "David Wagner")
    norwich.add_player(Player("Angus Gunn", 28, "GK", 79, 81, "England", 10, 55))
    norwich.add_player(Player("Shane Duffy", 32, "CB", 79, 79, "Republic of Ireland", 8, 50))
    norwich.add_player(Player("Grant Hanley", 32, "CB", 78, 78, "Scotland", 6, 45))
    norwich.add_player(Player("Jack Stacey", 28, "RB", 78, 79, "England", 8, 50))
    norwich.add_player(Player("Greg Leigh", 29, "LB", 76, 77, "England", 6, 40))
    norwich.add_player(Player("Kenny McLean", 32, "CM", 78, 78, "Scotland", 7, 50))
    norwich.add_player(Player("Gabriel Sara", 25, "CM", 79, 82, "Brazil", 15, 60))
    norwich.add_player(Player("Onel Hernández", 31, "LW", 78, 78, "Cuba", 8, 50))
    norwich.add_player(Player("Borja Sainz", 23, "RW", 78, 81, "Spain", 12, 55))
    norwich.add_player(Player("Josh Sargent", 24, "ST", 79, 82, "USA", 15, 65))
    teams.append(norwich)
    
    # Plymouth Argyle
    plymouth = Team("Plymouth Argyle", 2, "Home Park", "Steven Schumacher")
    plymouth.add_player(Player("Michael Cooper", 24, "GK", 76, 81, "England", 8, 40))
    plymouth.add_player(Player("Julio Pleguezuelo", 27, "CB", 77, 79, "Spain", 8, 45))
    plymouth.add_player(Player("Brendan Galloway", 28, "CB", 77, 78, "Zimbabwe", 7, 40))
    plymouth.add_player(Player("Bali Mumba", 22, "RB", 76, 80, "England", 8, 40))
    plymouth.add_player(Player("Jordan Houghton", 28, "LB", 75, 76, "Republic of Ireland", 5, 35))
    plymouth.add_player(Player("Joe Edwards", 33, "RM", 76, 76, "England", 5, 40))
    plymouth.add_player(Player("Adam Randell", 24, "CM", 75, 79, "England", 6, 35))
    plymouth.add_player(Player("Darko Gyabi", 20, "CM", 74, 80, "England", 6, 35))
    plymouth.add_player(Player("Freddie Issaka", 20, "LW", 73, 79, "England", 5, 30))
    plymouth.add_player(Player("Morgan Whittaker", 23, "ST", 78, 81, "England", 12, 50))
    teams.append(plymouth)
    
    # Preston North End
    preston = Team("Preston North End", 2, "Deepdale", "Ryan Lowe")
    preston.add_player(Player("Freddie Woodman", 27, "GK", 79, 81, "England", 10, 55))
    preston.add_player(Player("Liam Lindsay", 28, "CB", 77, 78, "Scotland", 7, 45))
    preston.add_player(Player("Patrick Bauer", 31, "CB", 77, 77, "Germany", 6, 40))
    preston.add_player(Player("Brad Potts", 29, "RB", 77, 78, "England", 7, 45))
    preston.add_player(Player("Jordan Storey", 26, "LB", 76, 78, "England", 7, 40))
    preston.add_player(Player("Alan Browne", 29, "CM", 78, 79, "Republic of Ireland", 8, 55))
    preston.add_player(Player("Duane Holmes", 29, "RM", 77, 78, "USA", 7, 50))
    preston.add_player(Player("Benjamin Whiteman", 27, "CDM", 76, 78, "England", 7, 45))
    preston.add_player(Player("Emil Riis", 25, "ST", 78, 80, "Denmark", 10, 55))
    teams.append(preston)
    
    # Queens Park Rangers
    qpr = Team("Queens Park Rangers", 2, "Loftus Road", "Gareth Ainsworth")
    qpr.add_player(Player("Joe Lumley", 29, "GK", 76, 77, "England", 6, 40))
    qpr.add_player(Player("Steve Cook", 33, "CB", 78, 78, "England", 6, 45))
    qpr.add_player(Player("Jake Clarke-Salter", 26, "CB", 76, 79, "England", 7, 40))
    qpr.add_player(Player("Kenneth Paal", 26, "LB", 78, 80, "Netherlands", 10, 50))
    qpr.add_player(Player("Paul Smyth", 26, "RB", 76, 78, "Northern Ireland", 7, 40))
    qpr.add_player(Player("Sam Field", 26, "CM", 77, 79, "England", 8, 45))
    qpr.add_player(Player("Ilias Chair", 26, "CAM", 78, 80, "Morocco", 10, 55))
    qpr.add_player(Player("Michael Frey", 29, "ST", 77, 78, "Switzerland", 8, 50))
    qpr.add_player(Player("Lyndon Dykes", 28, "ST", 78, 79, "Scotland", 9, 55))
    teams.append(qpr)
    
    # Reading
    reading = Team("Reading", 2, "Select Car Leasing Stadium", "Rubén Sellés")
    reading.add_player(Player("Joe Lumley", 29, "GK", 76, 77, "England", 6, 40))
    reading.add_player(Player("Tom McIntyre", 25, "CB", 76, 79, "England", 7, 40))
    reading.add_player(Player("Andy Yiadom", 32, "RB", 76, 77, "Ghana", 6, 40))
    reading.add_player(Player("Jeff Hendrick", 32, "CM", 77, 77, "Republic of Ireland", 6, 45))
    reading.add_player(Player("Kelvin Ehibhatiomhan", 22, "ST", 74, 79, "England", 6, 35))
    reading.add_player(Player("Lewis Wing", 28, "CM", 75, 77, "England", 6, 40))
    reading.add_player(Player("Sam Smith", 25, "ST", 75, 78, "England", 7, 45))
    reading.add_player(Player("Femi Azeez", 22, "RW", 74, 78, "England", 6, 35))
    teams.append(reading)
    
    # Rotherham United
    rotherham = Team("Rotherham United", 2, "New York Stadium", "Matt Taylor")
    rotherham.add_player(Player("Johannes Ertl", 33, "GK", 75, 75, "Austria", 4, 35))
    rotherham.add_player(Player("Cameron Dawson", 28, "GK", 76, 77, "England", 5, 35))
    rotherham.add_player(Player("Sean Raggett", 30, "CB", 76, 77, "Republic of Ireland", 6, 40))
    rotherham.add_player(Player("Cameron Humphreys", 21, "CM", 74, 80, "England", 6, 35))
    rotherham.add_player(Player("Jordan Hugill", 32, "ST", 77, 77, "England", 7, 50))
    rotherham.add_player(Player("Hakeem Odoffin", 25, "CDM", 75, 78, "England", 6, 40))
    rotherham.add_player(Player("Cafú", 30, "RB", 76, 77, "Portugal", 6, 40))
    rotherham.add_player(Player("Christ Tiehi", 25, "CM", 75, 77, "Ivory Coast", 6, 35))
    teams.append(rotherham)
    
    # Sheffield Wednesday
    sheffwed = Team("Sheffield Wednesday", 2, "Hillsborough", "Danny Röhl")
    sheffwed.add_player(Player("Cameron Dawson", 28, "GK", 77, 78, "England", 6, 40))
    sheffwed.add_player(Player("Liam Palmer", 32, "RB", 76, 76, "Scotland", 5, 40))
    sheffwed.add_player(Player("Di'Shon Bernard", 23, "CB", 76, 80, "Jamaica", 8, 40))
    sheffwed.add_player(Player("Marvin Johnson", 30, "LB", 76, 77, "England", 6, 40))
    sheffwed.add_player(Player("Barry Bannan", 34, "CM", 78, 78, "Scotland", 6, 50))
    sheffwed.add_player(Player("Josh Windass", 30, "CAM", 77, 78, "England", 7, 50))
    sheffwed.add_player(Player("Djeidi Gassama", 21, "RW", 75, 80, "Senegal", 8, 40))
    sheffwed.add_player(Player("Michael Smith", 32, "ST", 77, 77, "England", 7, 50))
    teams.append(sheffwed)
    
    # Southampton
    southampton = Team("Southampton", 2, "St Mary's Stadium", "Russell Martin")
    southampton.add_player(Player("Gavin Bazunu", 22, "GK", 78, 84, "Republic of Ireland", 12, 55))
    southampton.add_player(Player("Jack Stephens", 30, "CB", 77, 78, "England", 6, 45))
    southampton.add_player(Player("Taylor Harwood-Bellis", 22, "CB", 76, 81, "England", 8, 45))
    southampton.add_player(Player("Ryan Manning", 27, "LB", 78, 80, "Republic of Ireland", 10, 55))
    southampton.add_player(Player("Kyle Walker-Peters", 27, "RB", 79, 81, "England", 12, 60))
    southampton.add_player(Player("Flynn Downes", 25, "CDM", 78, 81, "England", 12, 55))
    southampton.add_player(Player("Joe Aribo", 27, "CM", 79, 81, "Nigeria", 12, 60))
    southampton.add_player(Player("Samuel Edozie", 21, "LW", 76, 82, "England", 10, 50))
    southampton.add_player(Player("Kamaldeen Sulemana", 22, "RW", 78, 83, "Ghana", 15, 60))
    southampton.add_player(Player("Che Adams", 27, "ST", 79, 81, "Scotland", 15, 65))
    teams.append(southampton)
    
    # Stoke City
    stoke = Team("Stoke City", 2, "bet365 Stadium", "Alex Neil")
    stoke.add_player(Player("Jack Butland", 31, "GK", 80, 81, "England", 10, 60))
    stoke.add_player(Player("Ben Wilmot", 24, "CB", 77, 81, "England", 10, 45))
    stoke.add_player(Player("Philipp Trechsel", 27, "CB", 76, 78, "Germany", 7, 40))
    stoke.add_player(Player("Lynden Gooch", 28, "RB", 77, 79, "USA", 8, 50))
    stoke.add_player(Player("Enda Stevens", 33, "LB", 77, 77, "Republic of Ireland", 5, 40))
    stoke.add_player(Player("Lewis Baker", 29, "CM", 78, 79, "England", 8, 55))
    stoke.add_player(Player("Joe Allen", 34, "CM", 78, 78, "Wales", 6, 50))
    stoke.add_player(Player("Million Manhoef", 22, "RW", 77, 82, "Netherlands", 12, 55))
    stoke.add_player(Player("Bae Jun-ho", 20, "LW", 75, 82, "South Korea", 10, 45))
    stoke.add_player(Player("Tyrese Campbell", 24, "ST", 76, 80, "England", 8, 45))
    teams.append(stoke)
    
    # Sunderland
    sunderland = Team("Sunderland", 2, "Stadium of Light", "Michael Beale")
    sunderland.add_player(Player("Anthony Patterson", 24, "GK", 77, 81, "England", 8, 45))
    sunderland.add_player(Player("Dan Ballard", 24, "CB", 77, 81, "Northern Ireland", 10, 50))
    sunderland.add_player(Player("Trai Hume", 22, "RB", 76, 81, "Northern Ireland", 10, 45))
    sunderland.add_player(Player("Dennis Cirkin", 22, "LB", 76, 81, "England", 10, 45))
    sunderland.add_player(Player("Dan Neil", 22, "CDM", 77, 82, "England", 12, 55))
    sunderland.add_player(Player("Jobe Bellingham", 18, "CM", 75, 85, "England", 15, 50))
    sunderland.add_player(Player("Jack Clarke", 23, "LW", 79, 83, "England", 18, 70))
    sunderland.add_player(Player("Romaine Mundle", 21, "RW", 76, 82, "England", 12, 55))
    sunderland.add_player(Player("Ross Stewart", 27, "ST", 78, 80, "Scotland", 12, 60))
    teams.append(sunderland)
    
    # Swansea City
    swansea = Team("Swansea City", 2, "Swansea.com Stadium", "Michael Duff")
    swansea.add_player(Player("Carl Rushworth", 22, "GK", 75, 81, "England", 6, 35))
    swansea.add_player(Player("Ben Cabango", 24, "CB", 77, 80, "Wales", 8, 45))
    swansea.add_player(Player("Nathan Wood", 22, "CB", 76, 81, "England", 8, 45))
    swansea.add_player(Player("Josh Key", 24, "RB", 75, 78, "England", 6, 40))
    swansea.add_player(Player("Ronald", 23, "LB", 76, 79, "Brazil", 7, 40))
    swansea.add_player(Player("Matt Grimes", 28, "CDM", 78, 79, "England", 8, 55))
    swansea.add_player(Player("Jay Fulton", 30, "CM", 77, 78, "Scotland", 7, 50))
    swansea.add_player(Player("Eoghan O'Connell", 29, "CB", 76, 77, "Republic of Ireland", 6, 40))
    swansea.add_player(Player("Jerry Yates", 27, "ST", 78, 79, "England", 9, 55))
    teams.append(swansea)
    
    # Watford
    watford = Team("Watford", 2, "Vicarage Road", "Valérien Ismaël")
    watford.add_player(Player("Daniel Bachmann", 29, "GK", 78, 79, "Austria", 8, 50))
    watford.add_player(Player("Ryan Porteous", 25, "CB", 77, 81, "Scotland", 10, 50))
    watford.add_player(Player("Wesley Hoedt", 30, "CB", 78, 79, "Netherlands", 8, 50))
    watford.add_player(Player("Jeremy Ngakia", 23, "RB", 76, 80, "England", 8, 45))
    watford.add_player(Player("Francisco Sierralta", 26, "LB", 77, 79, "Chile", 8, 45))
    watford.add_player(Player("Moussa Sissoko", 34, "CDM", 79, 79, "France", 6, 60))
    watford.add_player(Player("Tom Dele-Bashiru", 25, "CM", 76, 79, "Republic of Ireland", 7, 45))
    watford.add_player(Player("Imran Louza", 25, "CM", 77, 80, "Morocco", 9, 50))
    watford.add_player(Player("Vakoun Bayo", 27, "ST", 78, 80, "Ivory Coast", 10, 55))
    teams.append(watford)
    
    # West Bromwich Albion
    wba = Team("West Bromwich Albion", 2, "The Hawthorns", "Carlos Corberán")
    wba.add_player(Player("Alex Palmer", 27, "GK", 77, 79, "England", 7, 45))
    wba.add_player(Player("Kyle Bartley", 33, "CB", 78, 78, "England", 6, 50))
    wba.add_player(Player("Darnell Furlong", 28, "CB", 78, 79, "England", 8, 50))
    wba.add_player(Player("Conor Townsend", 31, "LB", 77, 78, "England", 7, 45))
    wba.add_player(Player("Alex Mowatt", 29, "CM", 78, 79, "England", 8, 55))
    wba.add_player(Player("Okay Yokuslu", 30, "CDM", 78, 79, "Turkey", 8, 55))
    wba.add_player(Player("Grady Diangana", 26, "RW", 78, 80, "DR Congo", 10, 55))
    wba.add_player(Player("Brandon Thomas-Asante", 25, "ST", 77, 80, "Ghana", 10, 50))
    teams.append(wba)
    
    return teams

# ============================================================================
# COMPETITIONS
# ============================================================================

class Competition:
    def __init__(self, name: str, comp_type: str):
        self.name = name
        self.comp_type = comp_type  # 'league', 'cup'
        self.teams: List[Team] = []
        self.fixtures: List[tuple] = []
        
class League(Competition):
    def __init__(self, name: str, division: int):
        super().__init__(name, 'league')
        self.division = division
        self.table: List[Dict] = []
        
    def update_table(self):
        """Sort teams by points, then goal difference"""
        self.table = sorted(
            [{'team': t, 'gd': t.gf - t.ga} for t in self.teams],
            key=lambda x: (x['team'].points, x['gd']),
            reverse=True
        )
        
    def display_table(self, top_n: int = None):
        self.update_table()
        print(f"\n{'='*80}")
        print(f"{self.name} - LEAGUE TABLE")
        print(f"{'='*80}")
        print(f"{'Pos':<4} {'Team':<25} {'P':<3} {'W':<3} {'D':<3} {'L':<3} {'GF':<3} {'GA':<3} {'GD':<4} {'Pts':<4}")
        print(f"{'-'*80}")
        
        entries = self.table[:top_n] if top_n else self.table
        for i, entry in enumerate(entries, 1):
            t = entry['team']
            gd = entry['gd']
            print(f"{i:<4} {t.name:<25} {t.played:<3} {t.won:<3} {t.drawn:<3} {t.lost:<3} {t.gf:<3} {t.ga:<3} {gd:<4} {t.points:<4}")
        
        print(f"{'='*80}\n")

class Cup(Competition):
    def __init__(self, name: str):
        super().__init__(name, 'cup')
        self.rounds = []
        self.current_round = 0
        self.winners = None
        
    def generate_fixtures(self):
        """Generate cup fixtures"""
        if len(self.teams) < 2:
            return
            
        random.shuffle(self.teams)
        self.fixtures = []
        for i in range(0, len(self.teams) - len(self.teams) % 2, 2):
            self.fixtures.append((self.teams[i], self.teams[i+1]))
            
        if len(self.teams) % 2 == 1:
            print(f"{self.teams[-1].name} gets a bye!")

# ============================================================================
# GAME ENGINE
# ============================================================================

class FIFACareerGame:
    def __init__(self):
        self.player_name = ""
        self.player_age = 16
        self.player_position = ""
        self.player_overall = 65
        self.player_potential = 88
        self.player_team: Optional[Team] = None
        self.player_value = 1.0  # millions
        self.player_wage = 5  # thousands per week
        self.career_year = 1
        self.leagues: Dict[int, League] = {}
        self.cups: List[Cup] = []
        self.all_teams: List[Team] = []
        self.match_history: List[Dict] = []
        self.transfer_offers: List[Dict] = []
        self.game_active = True
        
    def initialize_game(self):
        """Set up the game with all teams and competitions"""
        print("\n" + "="*80)
        print("FIFA CAREER MODE - ENGLAND DEMO")
        print("="*80)
        print("\nInitializing game...")
        
        # Create teams
        premier_league_teams = create_premier_league_teams()
        championship_teams = create_championship_teams()
        
        self.all_teams = premier_league_teams + championship_teams
        
        # Create leagues
        self.leagues[1] = League("Premier League", 1)
        self.leagues[1].teams = premier_league_teams
        
        self.leagues[2] = League("Sky Bet Championship", 2)
        self.leagues[2].teams = championship_teams
        
        # Create cups
        fa_cup = Cup("FA Cup")
        fa_cup.teams = self.all_teams.copy()
        self.cups.append(fa_cup)
        
        efl_cup = Cup("EFL Cup")
        efl_cup.teams = self.all_teams.copy()
        self.cups.append(efl_cup)
        
        print(f"✓ Created {len(premier_league_teams)} Premier League teams")
        print(f"✓ Created {len(championship_teams)} Championship teams")
        print(f"✓ Total players: {sum(len(t.players) for t in self.all_teams)}")
        print(f"✓ FA Cup initialized with {len(fa_cup.teams)} teams")
        print(f"✓ EFL Cup initialized with {len(efl_cup.teams)} teams")
        print("="*80 + "\n")
        
    def create_player(self):
        """Create the user's player"""
        print("\n" + "="*80)
        print("CREATE YOUR PLAYER")
        print("="*80)
        
        self.player_name = input("\nEnter your player name: ").strip()
        if not self.player_name:
            self.player_name = "Your Player"
            
        while True:
            try:
                self.player_age = int(input("Enter your age (16-40): "))
                if 16 <= self.player_age <= 40:
                    break
                print("Age must be between 16 and 40.")
            except ValueError:
                print("Please enter a valid number.")
                
        print("\nSelect position:")
        positions = ["GK", "CB", "LB", "RB", "CDM", "CM", "CAM", "LW", "RW", "ST"]
        for i, pos in enumerate(positions, 1):
            print(f"{i}. {pos}")
            
        while True:
            try:
                pos_choice = int(input(f"\nEnter position number (1-{len(positions)}): "))
                if 1 <= pos_choice <= len(positions):
                    self.player_position = positions[pos_choice - 1]
                    break
                print("Invalid choice.")
            except ValueError:
                print("Please enter a valid number.")
                
        # Set initial stats based on position
        base_overall = {"GK": 65, "CB": 68, "LB": 66, "RB": 66, "CDM": 67, 
                       "CM": 68, "CAM": 69, "LW": 70, "RW": 70, "ST": 71}
        self.player_overall = base_overall.get(self.player_position, 68)
        self.player_potential = random.randint(85, 93)
        
        print(f"\n{'='*80}")
        print(f"PLAYER CREATED!")
        print(f"{'='*80}")
        print(f"Name: {self.player_name}")
        print(f"Age: {self.player_age}")
        print(f"Position: {self.player_position}")
        print(f"Overall: {self.player_overall}")
        print(f"Potential: {self.player_potential}")
        print(f"Value: £{self.player_value:.1f}M")
        print(f"Wage: £{self.player_wage}k/week")
        print(f"{'='*80}\n")
        
    def select_team(self):
        """Let player choose their starting team"""
        print("\n" + "="*80)
        print("SELECT YOUR TEAM")
        print("="*80)
        
        print("\n--- PREMIER LEAGUE ---")
        pl_teams = self.leagues[1].teams
        for i, team in enumerate(pl_teams, 1):
            avg_rating = team.get_average_rating()
            print(f"{i:2}. {team.name:<30} (Avg: {avg_rating:.1f})")
            
        print("\n--- CHAMPIONSHIP ---")
        ch_teams = self.leagues[2].teams
        for i, team in enumerate(ch_teams, len(pl_teams) + 1):
            avg_rating = team.get_average_rating()
            print(f"{i:2}. {team.name:<30} (Avg: {avg_rating:.1f})")
            
        while True:
            try:
                choice = int(input(f"\nSelect team number (1-{len(self.all_teams)}): "))
                if 1 <= choice <= len(self.all_teams):
                    self.player_team = self.all_teams[choice - 1]
                    
                    # Add player to team
                    new_player = Player(
                        self.player_name, self.player_age, self.player_position,
                        self.player_overall, self.player_potential,
                        "England", self.player_value, self.player_wage
                    )
                    self.player_team.add_player(new_player)
                    
                    print(f"\n✓ You joined {self.player_team.name}!")
                    print(f"✓ Squad size: {len(self.player_team.players)} players")
                    break
                print("Invalid choice.")
            except ValueError:
                print("Please enter a valid number.")
                
    def simulate_match(self, team1: Team, team2: Team) -> tuple:
        """Simulate a match between two teams"""
        # Calculate team strengths
        strength1 = team1.get_average_rating()
        strength2 = team2.get_average_rating()
        
        # Home advantage
        strength1 += 2
        
        # Random factor
        strength1 += random.uniform(-3, 3)
        strength2 += random.uniform(-3, 3)
        
        # Determine goals
        diff = strength1 - strength2
        
        base_goals1 = max(0, (strength1 - 75) / 5)
        base_goals2 = max(0, (strength2 - 75) / 5)
        
        goals1 = int(max(0, base_goals1 + diff/3 + random.uniform(-1, 2)))
        goals2 = int(max(0, base_goals2 - diff/3 + random.uniform(-1, 2)))
        
        return goals1, goals2
        
    def play_match_day(self, league: League):
        """Play a match day for a league"""
        print(f"\n{'='*80}")
        print(f"PLAYING {league.name.upper()} MATCH DAY")
        print(f"{'='*80}")
        
        teams = league.teams.copy()
        random.shuffle(teams)
        
        for i in range(0, len(teams) - len(teams) % 2, 2):
            home = teams[i]
            away = teams[i+1]
            
            goals_home, goals_away = self.simulate_match(home, away)
            
            # Update stats
            home.played += 1
            away.played += 1
            home.gf += goals_home
            home.ga += goals_away
            away.gf += goals_away
            away.ga += goals_home
            
            if goals_home > goals_away:
                home.won += 1
                home.points += 3
                away.lost += 1
            elif goals_away > goals_home:
                away.won += 1
                away.points += 3
                home.lost += 1
            else:
                home.drawn += 1
                away.drawn += 1
                home.points += 1
                away.points += 1
                
            # Check if player's team is playing
            if self.player_team in [home, away]:
                print(f"\n*** YOUR TEAM: {home.name} {goals_home}-{goals_away} {away.name} ***")
                if goals_home > goals_away and home == self.player_team:
                    print("🎉 VICTORY! Your team won!")
                    self.player_overall = min(99, self.player_overall + 0.3)
                elif goals_away > goals_home and away == self.player_team:
                    print("🎉 VICTORY! Your team won!")
                    self.player_overall = min(99, self.player_overall + 0.3)
                elif goals_home == goals_away:
                    print("⚖️ DRAW")
                    self.player_overall = min(99, self.player_overall + 0.1)
                else:
                    print("❌ DEFEAT")
            else:
                print(f"{home.name} {goals_home}-{goals_away} {away.name}")
                
        league.update_table()
        
    def train(self):
        """Training session"""
        print(f"\n{'='*80}")
        print("TRAINING SESSION")
        print(f"{'='*80}")
        
        training_type = input("\nChoose training type:\n1. Technical\n2. Physical\n3. Tactical\n4. Position Specific\n> ")
        
        improvement = random.uniform(0.2, 0.8)
        
        if training_type == "1":
            print("\nYou worked on first touch, passing, and shooting...")
        elif training_type == "2":
            print("\nYou focused on stamina, strength, and speed...")
        elif training_type == "3":
            print("\nYou studied tactics and positioning...")
        elif training_type == "4":
            print(f"\nYou trained specifically for {self.player_position} role...")
        else:
            print("\nGeneral training session completed...")
            
        self.player_overall = min(99, self.player_overall + improvement)
        print(f"\n✓ Overall rating increased by {improvement:.1f}!")
        print(f"✓ New Overall: {self.player_overall:.1f}")
        
        # Update player in team
        for player in self.player_team.players:
            if player.name == self.player_name:
                player.overall = self.player_overall
                break
                
    def check_transfer_interest(self):
        """Check for transfer interest from other clubs"""
        interested_teams = []
        
        for team in self.all_teams:
            if team != self.player_team:
                # Higher rated teams more likely to be interested
                if team.get_average_rating() >= self.player_team.get_average_rating():
                    if random.random() < 0.3:  # 30% chance
                        interested_teams.append(team)
                        
        if interested_teams:
            print(f"\n{'='*80}")
            print("TRANSFER NEWS")
            print(f"{'='*80}")
            print("The following clubs are interested in you:")
            for team in interested_teams[:3]:  # Show max 3
                print(f"  • {team.name} ({self.leagues[team.division].name})")
                
            # Generate an offer
            if random.random() < 0.5 and interested_teams:
                offering_team = random.choice(interested_teams)
                offer_value = self.player_value * random.uniform(1.2, 2.0)
                offer_wage = self.player_wage * random.uniform(1.3, 2.5)
                
                print(f"\n💰 TRANSFER OFFER from {offering_team.name}!")
                print(f"   Transfer Fee: £{offer_value:.1f}M")
                print(f"   Weekly Wage: £{offer_wage:.1f}k")
                
                accept = input("\nAccept offer? (y/n): ").lower()
                if accept == 'y':
                    print(f"\n✓ Transfer accepted! You're now a {offering_team.name} player!")
                    
                    # Remove from old team
                    for i, player in enumerate(self.player_team.players):
                        if player.name == self.player_name:
                            self.player_team.players.pop(i)
                            break
                            
                    # Add to new team
                    new_player = Player(
                        self.player_name, self.player_age, self.player_position,
                        self.player_overall, self.player_potential,
                        "England", offer_value, offer_wage
                    )
                    offering_team.add_player(new_player)
                    self.player_team = offering_team
                    self.player_value = offer_value
                    self.player_wage = offer_wage
                    
    def view_squad(self):
        """View current team squad"""
        if not self.player_team:
            print("You don't have a team yet!")
            return
            
        print(f"\n{'='*80}")
        print(f"{self.player_team.name} SQUAD")
        print(f"{'='*80}")
        print(f"Manager: {self.player_team.manager}")
        print(f"Stadium: {self.player_team.stadium}")
        print(f"Squad Value: £{self.player_team.get_squad_value():.1f}M")
        print(f"Average Rating: {self.player_team.get_average_rating():.1f}")
        print(f"{'='*80}")
        
        # Sort by position then rating
        positions_order = ["GK", "CB", "LB", "RB", "CDM", "CM", "CAM", "LW", "RW", "ST"]
        sorted_players = sorted(
            self.player_team.players,
            key=lambda p: (positions_order.index(p.position) if p.position in positions_order else 99, -p.overall)
        )
        
        print(f"\n{'Position':<10} {'Name':<25} {'Age':<4} {'OVR':<4} {'POT':<4} {'Value':<8}")
        print(f"{'-'*80}")
        
        for player in sorted_players:
            marker = " ⭐" if player.name == self.player_name else ""
            print(f"{player.position:<10} {player.name:<25} {player.age:<4} {player.overall:<4} {player.potential:<4} £{player.value:.1f}M{marker}")
            
        print(f"{'='*80}\n")
        
    def view_career_stats(self):
        """View player career statistics"""
        print(f"\n{'='*80}")
        print(f"CAREER STATISTICS - {self.player_name}")
        print(f"{'='*80}")
        print(f"Age: {self.player_age}")
        print(f"Position: {self.player_position}")
        print(f"Current Club: {self.player_team.name if self.player_team else 'Free Agent'}")
        print(f"Overall: {self.player_overall:.1f}")
        print(f"Potential: {self.player_potential}")
        print(f"Market Value: £{self.player_value:.1f}M")
        print(f"Weekly Wage: £{self.player_wage}k")
        print(f"Career Year: {self.career_year}")
        print(f"{'='*80}\n")
        
    def end_season(self):
        """End the current season"""
        print(f"\n{'='*80}")
        print(f"END OF SEASON {self.career_year}")
        print(f"{'='*80}")
        
        # Show final tables
        for league in self.leagues.values():
            league.display_table(top_n=6)
            
        # Promotions and relegations
        print("\n--- PROMOTIONS & RELEGATIONS ---")
        
        # Premier League relegation
        pl_table = self.leagues[1].table
        relegated = [pl_table[-i]['team'] for i in range(1, 4)]
        print(f"\nRelegated from Premier League:")
        for team in relegated:
            print(f"  ❌ {team.name}")
            team.division = 2
            
        # Championship promotion
        ch_table = self.leagues[2].table
        promoted_auto = [ch_table[i]['team'] for i in range(2)]
        print(f"\nAutomatically Promoted to Premier League:")
        for team in promoted_auto:
            print(f"  ✅ {team.name}")
            team.division = 1
            
        # Playoff winner (simplified)
        playoff_teams = ch_table[2:6]
        playoff_winner = random.choice(playoff_teams)
        print(f"\nPlayoff Winner (Promoted):")
        print(f"  ✅ {playoff_winner.name}")
        playoff_winner.division = 1
        
        # Rebuild leagues
        self.leagues[1].teams = [t for t in self.all_teams if t.division == 1]
        self.leagues[2].teams = [t for t in self.all_teams if t.division == 2]
        
        # Age player
        self.player_age += 1
        self.career_year += 1
        
        print(f"\n✓ Season {self.career_year - 1} completed!")
        print(f"✓ You are now {self.player_age} years old")
        print(f"{'='*80}\n")
        
    def main_menu(self):
        """Display main menu"""
        print(f"\n{'='*80}")
        print(f"FIFA CAREER MODE - YEAR {self.career_year}")
        print(f"{'='*80}")
        print(f"Player: {self.player_name} ({self.player_position})")
        print(f"Club: {self.player_team.name if self.player_team else 'None'}")
        print(f"Overall: {self.player_overall:.1f} | Potential: {self.player_potential}")
        print(f"Value: £{self.player_value:.1f}M | Wage: £{self.player_wage}k/week")
        print(f"{'='*80}")
        print("\nMAIN MENU:")
        print("1. Play Match Day")
        print("2. Train")
        print("3. View Squad")
        print("4. View League Table")
        print("5. View Career Stats")
        print("6. Check Transfer Interest")
        print("7. End Season")
        print("8. Exit Game")
        
    def run(self):
        """Main game loop"""
        self.initialize_game()
        self.create_player()
        self.select_team()
        
        while self.game_active:
            self.main_menu()
            
            choice = input("\nEnter choice (1-8): ").strip()
            
            if choice == "1":
                div = self.player_team.division
                self.play_match_day(self.leagues[div])
            elif choice == "2":
                self.train()
            elif choice == "3":
                self.view_squad()
            elif choice == "4":
                div = self.player_team.division
                self.leagues[div].display_table()
            elif choice == "5":
                self.view_career_stats()
            elif choice == "6":
                self.check_transfer_interest()
            elif choice == "7":
                self.end_season()
            elif choice == "8":
                print(f"\nThank you for playing FIFA Career Mode, {self.player_name}!")
                print(f"Final Stats: Overall {self.player_overall:.1f}, Age {self.player_age}, Value £{self.player_value:.1f}M")
                self.game_active = False
            else:
                print("Invalid choice. Please try again.")

# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    game = FIFACareerGame()
    game.run()
