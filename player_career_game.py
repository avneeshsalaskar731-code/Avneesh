class PlayerCareerGame:
    def __init__(self, player_name, age):
        self.player_name = player_name
        self.age = age
        self.level = 1
        self.experience = 0
        self.is_playing = True

    def train(self):
        print(f"{self.player_name} is training...")
        self.experience += 10
        print(f"Experience: {self.experience}")
        self.check_level_up()

    def play_match(self):
        print(f"{self.player_name} is playing a match...")
        self.experience += 20
        print(f"Experience: {self.experience}")
        self.check_level_up()

    def check_level_up(self):
        if self.experience >= 100:
            self.level += 1
            self.experience = 0
            print(f"Congratulations! {self.player_name} leveled up to Level {self.level}!")

    def display_status(self):
        print(f"Player: {self.player_name}, Age: {self.age}, Level: {self.level}, Experience: {self.experience}")

    def start_game(self):
        print(f"Welcome to the Player Career Game, {self.player_name}!")
        while self.is_playing:
            action = input("Choose an action: train, play, status, exit: ").lower()
            if action == "train":
                self.train()
            elif action == "play":
                self.play_match()
            elif action == "status":
                self.display_status()
            elif action == "exit":
                print(f"Exiting game. Goodbye, {self.player_name}!")
                self.is_playing = False
            else:
                print("Invalid action. Please try again.")

# Example usage
if __name__ == '__main__':
    player_name = input("Enter your player name: ")
    player_age = int(input("Enter your player age: "))
    game = PlayerCareerGame(player_name, player_age)
    game.start_game()