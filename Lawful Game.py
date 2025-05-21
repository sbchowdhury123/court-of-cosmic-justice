import random
import re
import time

class Judge:
    """Represents Judge AstraLex with varying personalities"""
    def __init__(self):
        self.personalities = {
            "Stern": {"tone": "formal", "weight": 0.4, "prefix": "Hear ye, the Court decrees:"},
            "Sarcastic": {"tone": "witty", "weight": 0.3, "prefix": "Oh, really? The Court sighs:"},
            "Poetic": {"tone": "dramatic", "weight": 0.2, "prefix": "In the stars’ grand verse:"},
            "Cheerful": {"tone": "upbeat", "weight": 0.1, "prefix": "Huzzah! The Court proclaims:"}
        }
        self.personality = random.choices(
            list(self.personalities.keys()),
            weights=[p["weight"] for p in self.personalities.values()],
            k=1
        )[0]
        self.articles = [
            "Article {0} of the Galactic Code",
            "Stellar Statute {0}B",
            "Nebula Edict {0}.X",
            "Cosmic Canon {0}-Z"
        ]
        self.penalties = [
            ("restitution", "pay {0} moonstones in compensation"),
            ("mediation", "attend a {0}-session cosmic mediation"),
            ("penalty", "perform {0} hours of asteroid polishing"),
            ("warning", "receive a formal warning from the Nebula Council")
        ]

    def generate_ruling(self, problem, category, severity):
        """Generate a lawful ruling based on problem, category, and severity"""
        article = random.choice(self.articles).format(random.randint(1, 100))
        penalty_type, penalty_text = random.choices(
            self.penalties,
            weights=[0.5, 0.3, 0.15, 0.05] if severity < 5 else [0.2, 0.4, 0.3, 0.1],
            k=1
        )[0]
        penalty_value = random.randint(1, 5) if penalty_type in ["restitution", "penalty"] else random.randint(1, 3)
        tone = self.personalities[self.personality]["tone"]
        
        # Response templates by category
        templates = {
            "property": (
                f"{self.personalities[self.personality]['prefix']} By {article}, the offense of {category} disruption "
                f"is noted. The court orders you to {penalty_text.format(penalty_value)}. "
                f"{'Cease such antics, or face the Void!' if tone == 'formal' else 'Next time, keep your space cows tethered!' if tone == 'witty' else 'Thus, harmony restores the cosmic herd!' if tone == 'dramatic' else 'Let’s keep the galaxy moo-ving smoothly!'}"
            ),
            "ethics": (
                f"{self.personalities[self.personality]['prefix']} Under {article}, ethical breaches demand scrutiny. "
                f"You shall {penalty_text.format(penalty_value)}. "
                f"{'Reflect on your duties, citizen!' if tone == 'formal' else 'Really, cloning without consent? Tsk tsk!' if tone == 'witty' else 'Seek wisdom in the stars’ light!' if tone == 'dramatic' else 'Let’s clone some good vibes instead!'}"
            ),
            "interpersonal": (
                f"{self.personalities[self.personality]['prefix']} Per {article}, discord among stars is forbidden. "
                f"The court mandates you {penalty_text.format(penalty_value)}. "
                f"{'Foster peace, or answer to the Court!' if tone == 'formal' else 'Stop rebooting their coffee maker, you rogue!' if tone == 'witty' else 'Let love guide your cosmic dance!' if tone == 'dramatic' else 'Hug it out, space pals!'}"
            ),
            "technology": (
                f"{self.personalities[self.personality]['prefix']} By {article}, tech tampering disrupts the cosmos. "
                f"You are ordered to {penalty_text.format(penalty_value)}. "
                f"{'Respect the circuits of justice!' if tone == 'formal' else 'Hacking the holodeck again? Seriously?' if tone == 'witty' else 'Code flows smoothly in starlight!' if tone == 'dramatic' else 'Let’s debug with a smile!'}"
            ),
            "unknown": (
                f"{self.personalities[self.personality]['prefix']} Under {article}, ambiguous grievances perplex the Court. "
                f"You must {penalty_text.format(penalty_value)}. "
                f"{'Clarify your plea next time!' if tone == 'formal' else 'What even is this problem? Stars above!' if tone == 'witty' else 'Mysteries veil the cosmic truth!' if tone == 'dramatic' else 'Let’s sort this out with a cosmic grin!'}"
            )
        }
        return templates.get(category, templates["unknown"])

class Case:
    """Represents a single case with problem, category, severity, and ruling"""
    def __init__(self, problem, category, severity, ruling):
        self.problem = problem
        self.category = category
        self.severity = severity
        self.ruling = ruling
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

class Player:
    """Tracks player’s case history and achievements"""
    def __init__(self):
        self.cases = []
        self.achievements = {
            "First Case": False,
            "Master Litigant": False,
            "Persistent Appellant": False
        }
        self.appeals = 0

    def add_case(self, case):
        """Add a case and check achievements"""
        self.cases.append(case)
        if len(self.cases) == 1:
            self.achievements["First Case"] = True
        if len(self.cases) >= 5:
            self.achievements["Master Litigant"] = True

    def add_appeal(self):
        """Track appeals for achievements"""
        self.appeals += 1
        if self.appeals >= 3:
            self.achievements["Persistent Appellant"] = True

class Game:
    """Manages the game loop and state"""
    def __init__(self):
        self.judge = Judge()
        self.player = Player()
        self.categories = {
            "property": ["steal", "stole", "theft", "property", "cow", "belong", "take", "taken"],
            "ethics": ["ethic", "moral", "right", "wrong", "crime", "clone", "cheat", "lie"],
            "interpersonal": ["friend", "neighbor", "dispute", "fight", "argue", "conflict", "roommate"],
            "technology": ["robot", "tech", "hack", "reboot", "machine", "coffee maker", "holodeck"]
        }

    def analyze_problem(self, problem):
        """Analyze problem for category and severity"""
        problem = problem.lower()
        category = "unknown"
        severity = 1

        for cat, keywords in self.categories.items():
            if any(re.search(r'\b' + re.escape(k) + r'\b', problem) for k in keywords):
                category = cat
                severity += sum(1 for k in keywords if re.search(r'\b' + re.escape(k) + r'\b', problem))
                break

        # Additional severity for serious terms
        if any(word in problem for word in ["crime", "serious", "major", "urgent"]):
            severity += 3
        severity = min(severity, 10)  # Cap at 10
        return category, severity

    def display_achievements(self):
        """Show unlocked achievements"""
        unlocked = [name for name, unlocked in self.player.achievements.items() if unlocked]
        if unlocked:
            print("\nAchievements Unlocked:")
            for name in unlocked:
                print(f"- {name}")
        else:
            print("\nNo achievements unlocked yet. Keep litigating!")

    def display_history(self):
        """Show case history"""
        if not self.player.cases:
            print("\nNo cases filed yet. Present a problem to the Court!")
            return
        print("\nCase History:")
        for i, case in enumerate(self.player.cases, 1):
            print(f"Case {i} ({case.timestamp}):")
            print(f"  Problem: {case.problem}")
            print(f"  Category: {case.category.capitalize()}")
            print(f"  Severity: {case.severity}/10")
            print(f"  Ruling: {case.ruling}\n")

    def run(self):
        """Main game loop"""
        print("Welcome to the Court of Cosmic Justice!")
        print("Present your problem to Judge AstraLex, and receive a lawful ruling.")
        print("Type 'q' to quit, 'history' to view cases, 'achievements' for progress, or your problem.")

        while True:
            print(f"\nJudge AstraLex ({self.judge.personality} demeanor) awaits your plea:")
            action = input("> ").strip()

            if action.lower() == 'q':
                print("\nThe Court of Cosmic Justice adjourns. Farewell, citizen!")
                break
            elif action.lower() == 'history':
                self.display_history()
                continue
            elif action.lower() == 'achievements':
                self.display_achievements()
                continue
            elif not action:
                print("The Court requires a problem, not silence! Try again.")
                continue

            # Analyze and process the problem
            category, severity = self.analyze_problem(action)
            ruling = self.judge.generate_ruling(action, category, severity)
            case = Case(action, category, severity, ruling)
            self.player.add_case(case)

            # Display ruling
            print(f"\n*** Ruling from Judge AstraLex ***")
            print(f"Problem: {action}")
            print(f"Category: {category.capitalize()}")
            print(f"Severity: {severity}/10")
            print(f"Ruling: {ruling}\n")

            # Offer appeal or continue
            print("Options: (1) Appeal this ruling, (2) Present new problem, (3) View history, (4) Quit")
            choice = input("Choose (1-4): ").strip()
            if choice == '1':
                self.player.add_appeal()
                print("\nAppeal granted! The Court reconsiders...")
                time.sleep(1)
                ruling = self.judge.generate_ruling(action, category, severity + 1)  # Slightly harsher
                case.ruling = ruling
                print(f"\n*** Revised Ruling ***")
                print(f"Ruling: {ruling}\n")
            elif choice == '3':
                self.display_history()
            elif choice == '4':
                print("\nThe Court adjourns. Return when justice calls!")
                break
            # Else continue to new problem

if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nThe Court is abruptly dismissed. Farewell!")
    except Exception as e:
        print(f"\nCosmic error in the Court: {e}")