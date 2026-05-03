#!/usr/bin/env python3
"""
Murder Mystery: The Case of the Midnight Manor
An interactive text-based detective game
"""

import random
import time
from datetime import datetime

class MurderMysteryGame:
    def __init__(self):
        self.game_state = "intro"
        self.current_location = "study"
        self.clues_found = []
        self.suspects_interviewed = []
        self.notes = []
        self.accusation_made = False
        self.game_won = False
        
        # Game data
        self.victim = "Lord Blackwood"
        self.murderer = "Victoria Sterling"
        self.murder_weapon = "poisoned tea"
        self.murder_time = "between 10 PM and midnight"
        
        self.locations = {
            "study": {
                "name": "The Study",
                "description": "Lord Blackwood's private study. Books line the walls, and a large desk sits in the center. The body was found here.",
                "clues": ["empty teacup", "torn letter", "overturned chair"],
                "visited": False
            },
            "kitchen": {
                "name": "The Kitchen",
                "description": "A large Victorian kitchen with copper pots hanging from the ceiling. The smell of herbs lingers in the air.",
                "clues": ["missing tea tin", "strange powder residue", "cleaned counter"],
                "visited": False
            },
            "library": {
                "name": "The Library",
                "description": "Floor-to-ceiling bookshelves filled with ancient tomes. A comfortable reading chair faces the fireplace.",
                "clues": ["hidden diary", "bookmark with initials", "burnt paper fragments"],
                "visited": False
            },
            "garden": {
                "name": "The Garden",
                "description": "A well-maintained garden with roses and lavender. A small greenhouse stands at the far end.",
                "clues": ["trampled flowers", "footprints", "broken glass vial"],
                "visited": False
            },
            "drawing_room": {
                "name": "The Drawing Room",
                "description": "An elegant room with velvet furniture and portraits of ancestors watching from the walls.",
                "clues": ["overheard conversation note", "missing jewelry box", "wine glass with lipstick"],
                "visited": False
            }
        }
        
        self.suspects = {
            "Victoria Sterling": {
                "relation": "Lord Blackwood's niece",
                "motive": "Inheritance - stands to gain the entire fortune",
                "alibi": "Claims she was reading in the library",
                "personality": "Nervous, avoids eye contact, speaks quickly",
                "truths": ["Was seen near the kitchen around 9:30 PM", "Had financial troubles"],
                "lies": ["Claims she never left the library", "Denies knowing about the tea"],
                "interviewed": False
            },
            "James Morrison": {
                "relation": "Lord Blackwood's business partner",
                "motive": "Blackwood was going to expose his embezzlement",
                "alibi": "Says he was in the drawing room drinking wine",
                "personality": "Confident, defensive, changes subject often",
                "truths": ["Was arguing with Blackwood earlier that day", "Has access to all rooms"],
                "lies": ["Claims the argument was friendly", "Denies financial troubles"],
                "interviewed": False
            },
            "Mrs. Hudson": {
                "relation": "The housekeeper",
                "motive": "Blackwood threatened to fire her after 30 years of service",
                "alibi": "States she was in the kitchen preparing tomorrow's meals",
                "personality": "Elderly, speaks softly, seems genuinely grieving",
                "truths": ["Prepared the tea at 9 PM", "Knows everyone's routines"],
                "lies": ["Claims she saw nothing suspicious", "Hides knowledge of missing items"],
                "interviewed": False
            },
            "Dr. Chen": {
                "relation": "Lord Blackwood's personal physician",
                "motive": "Blackwood discovered he was prescribing fake medications",
                "alibi": "Claims he was called away on an emergency at 8 PM",
                "personality": "Calm, professional, too eager to help",
                "truths": ["Has knowledge of poisons", "Was seen leaving the manor"],
                "lies": ["No emergency call was made", "Claims he returned after Blackwood died"],
                "interviewed": False
            }
        }
        
        self.key_clues = [
            "poisoned tea",
            "Victoria's handwriting on torn letter",
            "financial records showing Victoria's debts",
            "witness testimony placing Victoria near study",
            "missing poison from Dr. Chen's bag"
        ]
    
    def display_intro(self):
        print("=" * 70)
        print("🔍 MURDER MYSTERY: THE CASE OF THE MIDNIGHT MANOR 🔍")
        print("=" * 70)
        print()
        print("London, 1895. You are Detective Inspector Alexander Cross,")
        print("called to investigate the mysterious death of Lord Blackwood.")
        print()
        print("The wealthy aristocrat was found dead in his study at midnight.")
        print("Four suspects remain in the manor. One of them is the killer.")
        print()
        print("Your mission:")
        print("  • Search locations for clues")
        print("  • Interview suspects")
        print("  • Piece together the evidence")
        print("  • Accuse the murderer before they escape!")
        print()
        print("Commands:")
        print("  • 'locations' - List available locations")
        print("  • 'go [place]' - Move to a location")
        print("  • 'search' - Search current location for clues")
        print("  • 'suspects' - List suspects")
        print("  • 'interview [name]' - Interview a suspect")
        print("  • 'clues' - Review collected clues")
        print("  • 'notes' - View your investigation notes")
        print("  • 'accuse [name]' - Make your final accusation")
        print("  • 'help' - Show this help message")
        print("  • 'quit' - End the game")
        print()
        print("=" * 70)
        input("Press Enter to begin your investigation...")
        print()
    
    def display_location(self):
        loc = self.locations[self.current_location]
        print(f"\n📍 {loc['name']}")
        print("-" * 50)
        print(loc['description'])
        if loc['visited'] and not loc['clues']:
            print("\n(You've already searched this location thoroughly)")
        elif loc['clues']:
            print(f"\n💡 There may be clues here to discover. (Type 'search')")
        print()
    
    def list_locations(self):
        print("\n🏠 Available Locations:")
        print("-" * 30)
        for key, loc in self.locations.items():
            status = "✓ visited" if loc['visited'] else "• unvisited"
            print(f"  • {key} ({loc['name']}) - {status}")
        print()
    
    def list_suspects(self):
        print("\n👥 Suspects:")
        print("-" * 30)
        for name, suspect in self.suspects.items():
            status = "✓ interviewed" if suspect['interviewed'] else "• not interviewed"
            print(f"  • {name} ({suspect['relation']}) - {status}")
        print()
    
    def search_location(self):
        loc = self.locations[self.current_location]
        
        if not loc['clues']:
            print("\nYou've already searched this area thoroughly. No more clues to find.")
            return
        
        print(f"\n🔍 Searching {loc['name']}...")
        time.sleep(1)
        
        found_clue = loc['clues'].pop(0)
        self.clues_found.append(found_clue)
        loc['visited'] = True
        
        print(f"\n✨ You found: {found_clue.upper()}")
        
        # Add context to certain clues
        clue_contexts = {
            "empty teacup": "The teacup smells faintly of almonds. Interesting...",
            "torn letter": "The letter mentions 'inheritance' and is signed with 'V.S.'",
            "missing tea tin": "The Earl Grey tea tin is missing. Mrs. Hudson says she saw it yesterday.",
            "strange powder residue": "A white powder residue on the counter. Could be poison?",
            "hidden diary": "A diary hidden behind books mentions 'Victoria's mounting debts'",
            "bookmark with initials": "A bookmark with 'V.S.' initials - Victoria Sterling's mark",
            "trampled flowers": "Someone recently trampled through the garden path hurriedly",
            "broken glass vial": "Small glass fragments with chemical residue - possibly poison container",
            "overheard conversation note": "A note mentioning 'embezzlement' and 'exposure'",
            "wine glass with lipstick": "Red lipstick on the glass - matches Victoria's usual color"
        }
        
        if found_clue in clue_contexts:
            print(f"   Note: {clue_contexts[found_clue]}")
        
        print(f"\nTotal clues collected: {len(self.clues_found)}")
        print()
    
    def interview_suspect(self, suspect_name):
        # Find the suspect (case-insensitive partial match)
        suspect_key = None
        for name in self.suspects.keys():
            if suspect_name.lower() in name.lower():
                suspect_key = name
                break
        
        if not suspect_key:
            print(f"\n❌ '{suspect_name}' is not a valid suspect.")
            print("Available suspects:", ", ".join(self.suspects.keys()))
            return
        
        suspect = self.suspects[suspect_key]
        
        if suspect['interviewed']:
            print(f"\nYou've already interviewed {suspect_key}.")
            print(f"Recall: {suspect['personality']}")
            print(f"Alibi: {suspect['alibi']}")
            print(f"Motive: {suspect['motive']}")
            return
        
        print(f"\n🗣️ Interviewing {suspect_key}...")
        print("-" * 50)
        print(f"Relation: {suspect['relation']}")
        print(f"Personality: {suspect['personality']}")
        print()
        time.sleep(1)
        
        print(f"Detective: 'Where were you {self.murder_time}?'\n")
        time.sleep(0.5)
        print(f"{suspect_key}: '{suspect['alibi']}'\n")
        time.sleep(0.5)
        
        print(f"Detective: 'Do you have any reason to want Lord Blackwood dead?'\n")
        time.sleep(0.5)
        print(f"{suspect_key}: *looks uncomfortable* 'Of course not! We had our differences, but...'\n")
        time.sleep(0.5)
        
        # Reveal some truths and lies
        truth = random.choice(suspect['truths'])
        lie = random.choice(suspect['lies'])
        
        print(f"During the interview, you learn:")
        print(f"  • {truth}")
        print(f"  • They claim: '{lie}'")
        print()
        
        suspect['interviewed'] = True
        self.suspects_interviewed.append(suspect_key)
        
        # Add interview notes
        self.notes.append(f"Interviewed {suspect_key}: {suspect['motive']}")
        
        print(f"✅ Interview complete. {suspect_key} seems {'nervous' if suspect_key == 'Victoria Sterling' else 'evasive'}.")
        print()
    
    def show_clues(self):
        if not self.clues_found:
            print("\n📋 You haven't found any clues yet.")
            return
        
        print(f"\n📋 Collected Clues ({len(self.clues_found)}):")
        print("-" * 50)
        for i, clue in enumerate(self.clues_found, 1):
            print(f"  {i}. {clue}")
        print()
        
        # Check if player has enough clues to make accusation
        critical_clues = sum(1 for clue in self.clues_found if any(key in clue.lower() for key in ['victoria', 'v.s.', 'poison', 'tea', 'debt']))
        if critical_clues >= 3:
            print("💡 You have gathered significant evidence. Ready to make an accusation?")
        print()
    
    def show_notes(self):
        if not self.notes:
            print("\n📝 No notes yet. Start investigating!")
            return
        
        print(f"\n📝 Investigation Notes ({len(self.notes)}):")
        print("-" * 50)
        for i, note in enumerate(self.notes, 1):
            print(f"  {i}. {note}")
        print()
    
    def make_accusation(self, suspect_name):
        # Find the suspect (case-insensitive partial match)
        suspect_key = None
        for name in self.suspects.keys():
            if suspect_name.lower() in name.lower():
                suspect_key = name
                break
        
        if not suspect_key:
            print(f"\n❌ '{suspect_name}' is not a valid suspect.")
            print("Available suspects:", ", ".join(self.suspects.keys()))
            return
        
        if self.accusation_made:
            print("\nYou've already made your accusation!")
            return
        
        self.accusation_made = True
        
        print("\n" + "=" * 70)
        print("⚖️  FINAL ACCUSATION  ⚖️")
        print("=" * 70)
        print(f"\nDetective Cross gathers all suspects in the drawing room...")
        time.sleep(1)
        print(f"\n'After careful investigation, I have determined that...'")
        time.sleep(2)
        print(f"\n🎯 YOU ACCUSE: {suspect_key.upper()}")
        print()
        
        if suspect_key == self.murderer:
            self.game_won = True
            print("✅ CORRECT! Victoria Sterling breaks down and confesses!")
            print()
            print("Victoria: 'Yes, it was me! Uncle was going to cut me off from")
            print("the inheritance. I was drowning in debts from gambling. I poisoned")
            print("his evening tea with arsenic I stole from Dr. Chen's medical bag.'")
            print()
            print("She explains how she waited until everyone was occupied, then")
            print("slipped into the study while Lord Blackwood was reading. She")
            print("offered to bring him fresh tea, and he unsuspectingly drank it.")
            print()
            print("🏆 CONGRATULATIONS, DETECTIVE!")
            print("You solved the case of the Midnight Manor!")
            print()
            print(f"Final Statistics:")
            print(f"  • Clues found: {len(self.clues_found)}")
            print(f"  • Suspects interviewed: {len(self.suspects_interviewed)}")
            print(f"  • Locations searched: {sum(1 for loc in self.locations.values() if loc['visited'])}")
        else:
            print(f"❌ INCORRECT! {suspect_key} is innocent!")
            print()
            print(f"The real murderer, {self.murderer}, smirks as {suspect_key} is arrested.")
            print()
            print(f"{suspect_key}: 'How could you make such a mistake?!'")
            print()
            print("Without enough evidence, the true killer escapes justice...")
            print()
            print("💀 GAME OVER - The murderer goes free")
            print()
            print(f"The killer was: {self.murderer}")
            print(f"The murder weapon was: {self.murder_weapon}")
            print(f"The murder occurred: {self.murder_time}")
        
        print("\n" + "=" * 70)
        print("Thank you for playing Murder Mystery: The Case of the Midnight Manor!")
        print("=" * 70)
    
    def show_help(self):
        print("\n📖 HELP - Investigation Commands:")
        print("-" * 50)
        print("  locations          - List all available locations")
        print("  go [place]         - Move to a location (e.g., 'go study')")
        print("  search             - Search current location for clues")
        print("  suspects           - List all suspects")
        print("  interview [name]   - Interview a suspect (e.g., 'interview Victoria')")
        print("  clues              - Review all collected clues")
        print("  notes              - View investigation notes")
        print("  accuse [name]      - Accuse someone of the murder")
        print("  help               - Show this help message")
        print("  quit               - Exit the game")
        print()
        print("💡 Tips:")
        print("  • Search every location thoroughly")
        print("  • Interview all suspects before accusing")
        print("  • Look for connections between clues")
        print("  • Pay attention to inconsistencies in alibis")
        print()
    
    def play(self):
        self.display_intro()
        
        while not self.game_won and not (self.accusation_made and not self.game_won):
            try:
                command = input("\n🔍 Detective Cross > ").strip().lower()
                
                if not command:
                    continue
                
                parts = command.split(maxsplit=1)
                action = parts[0]
                target = parts[1] if len(parts) > 1 else ""
                
                if action in ["quit", "exit", "q"]:
                    print("\nGoodbye, Detective. The case remains unsolved...")
                    break
                
                elif action == "help":
                    self.show_help()
                
                elif action == "locations":
                    self.list_locations()
                
                elif action == "suspects":
                    self.list_suspects()
                
                elif action == "go":
                    if not target:
                        print("Go where? Specify a location.")
                        continue
                    if target in self.locations:
                        self.current_location = target
                        self.display_location()
                    else:
                        print(f"'{target}' is not a valid location.")
                        print("Try:", ", ".join(self.locations.keys()))
                
                elif action == "search":
                    self.search_location()
                
                elif action == "interview":
                    if not target:
                        print("Interview whom? Specify a suspect.")
                        continue
                    self.interview_suspect(target)
                
                elif action == "clues":
                    self.show_clues()
                
                elif action == "notes":
                    self.show_notes()
                
                elif action == "accuse":
                    if not target:
                        print("Accuse whom? Specify a suspect.")
                        continue
                    self.make_accusation(target)
                    if self.accusation_made:
                        break
                
                else:
                    print(f"Unknown command: '{action}'")
                    print("Type 'help' for available commands.")
                    
            except KeyboardInterrupt:
                print("\n\nInvestigation interrupted. Goodbye, Detective!")
                break
            except EOFError:
                print("\n\nGoodbye!")
                break


def main():
    print("\n" + "🔍" * 35)
    print(" Welcome to Murder Mystery: The Case of the Midnight Manor ".center(70, " "))
    print("🔍" * 35 + "\n")
    
    game = MurderMysteryGame()
    game.play()


if __name__ == "__main__":
    main()
