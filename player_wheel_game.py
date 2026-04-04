import random

class Player:
    def __init__(self, name):
        self.name = name
        self.stats = {"skill": 50, "fitness": 50, "experience": 0}
        self.sponsorships = []
        self.injuries = []
        self.achievements = []

    def train(self):
        gain = random.randint(1, 10)
        self.stats["skill"] += gain
        self.stats["fitness"] -= 5  # Training impacts fitness
        print(f"{self.name} trained and gained {gain} skill!")

    def rest(self):
        self.stats["fitness"] += 10
        print(f"{self.name} rested and regained fitness!")

    def add_sponsorship(self, sponsorship):
        self.sponsorships.append(sponsorship)
        print(f"{self.name} acquired sponsorship: {sponsorship}")

class SpinWheel:
    def __init__(self):
        self.segments = ["Match Win", "Match Loss", "Sponsorship", "Injury", "Training Boost"]

    def spin(self):
        outcome = random.choice(self.segments)
        print(f"Spun the wheel and got: {outcome}")
        return outcome

class Game:
    def __init__(self):
        self.players = []
        self.wheel = SpinWheel()

    def add_player(self, player):
        self.players.append(player)
        print(f"Player {player.name} added to the game!")

    def play_turn(self, player):
        outcome = self.wheel.spin()
        if outcome == "Match Win":
            player.stats["experience"] += 10
            print(f"{player.name} won the match!")
        elif outcome == "Match Loss":
            player.stats["experience"] -= 5
            print(f"{player.name} lost the match.")
        elif outcome == "Sponsorship":
            player.add_sponsorship("New Sponsor")
        elif outcome == "Injury":
            player.injuries.append("Minor Injury")
            print(f"{player.name} got injured.")
        elif outcome == "Training Boost":
            player.train()

    def show_stats(self, player):
        print(f"Stats for {player.name}: {player.stats}")

if __name__ == '__main__':
    game = Game()
    player1 = Player("Player1")
    player2 = Player("Player2")
    game.add_player(player1)
    game.add_player(player2)

    for _ in range(5):  # Simulate 5 turns
        game.play_turn(player1)
        game.show_stats(player1)
        game.play_turn(player2)
        game.show_stats(player2)
