import hashlib
from rich.console import Console
from datetime import datetime
import json
from rich.panel import Panel
from rich import box
from rich.prompt import Prompt

console = Console()


# === Utility Functions ===
def parse_note(raw_note):
    """
    Parse a raw note string into its components: note text, tags, and due date.
    Args:
        raw_note (str): A line of note text possibly containing tags and a due date, e.g.
        "Buy milk #groceries [due:2025-08-01]".
    Returns:
        dict: Contains 'note'(str), 'tags'(list), and 'due_date' (str or None)
    """

    note_part = raw_note
    tags = []
    due = None

    if "[due:" in raw_note:
        note_part, due_chunk = raw_note.rsplit("[due:", 1)
        due = due_chunk.rstrip("]").strip()

    tag_tokens = [word for word in note_part.strip().split() if word.startswith("#")]
    tags = tag_tokens
    clean_note = "".join(
        [word for word in note_part.strip().split() if not word.startswith("#")]
    )

    return {"note": clean_note.strip(), "tags": tags, "due_date": due}


def build_note_from_json(data):
    """
    Build a formatted note string from its JSON components.
    """

    note = data["note"]
    tags = " ".join(data["tags"]) if data["tags"] else ""
    due = f"[due:{data['due_date']}]" if data["due_date"] else ""

    return f"{note} {tags} {due}".strip()


def hash_password(password):
    """
    Return the SHA-256 of the given password.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def register_user():
    """
    Prompt the user to register a new account with a new username and password.
    The credentials (username and hashed password) are saved to 'users.txt'
    """
    username = input("Choose a username: ").strip()
    password = input("Choose a password: ").strip()

    hashed_pw = hash_password(password)

    # Check if user already exist
    try:
        with open("users.txt", "r") as file:
            for line in file:
                if line.startswith(username + ":"):
                    console.print("[bold red]Username already exists.[/bold red]")
                    return None

    except FileNotFoundError:
        pass

    # Save new user
    with open("users.txt", "a") as file:
        file.write(f"{username}:{hashed_pw}\n")
    console.print(
        f"User [bold green]'{username}'[/bold green] registered successfully!"
    )
    return username


def login_user():
    """
    Prompt for username and password, and validate against 'users.txt'
    """
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    hashed_pw = hash_password(password)

    try:
        with open("users.txt", "r") as file:
            for line in file:
                saved_user, saved_pw = line.strip().split(":")
                if saved_user == username and saved_pw == hashed_pw:
                    console.print(
                        f"[bold green]'{username}'[/bold green] Login successfull!"
                    )
                    return username

    except FileNotFoundError:
        pass

    console.print("[red]Login failed. Try again[/red]")
    return None


user = None
sc_notes = []
notes_file = f"notes_{user}.txt"


# Load the notes from the file if it exists
def load_notes_from_file():
    try:
        with open(notes_file, "r") as f:
            notes = [note.strip() for note in f.readlines()]  # cleanup newlines
            return notes
    except FileNotFoundError:
        return []


def show_due_alerts():
    """
    Scan notes and show a panel with count of overdue and due-today tasks.
    """
    saved_notes = load_notes_from_file()
    today = datetime.today().date()
    overdue = []
    due_today = []

    for note in saved_notes:
        if "[due:" in note:
            try:
                due_str = note.split("[due:")[1].split("]")[0]
                due_date = datetime.strptime(due_str, "%Y-%m-%d").date()

                if due_date < today:
                    overdue.append(due_date)

                elif due_date == today:
                    due_today.append(due_date)

            except Exception:
                continue

    if overdue or due_today:
        console.print(
            Panel.fit(
                f"[red]{len(overdue)} overdue[/red] | [bold yellow]{len(due_today)} due today[/bold yellow]",
                title="[bold green]Tasks Reminder[/bold green]",
                border_style="bright_red",
            )
        )
    else:
        console.print("[green]No Due tasks today. All clear[/green]")


# === App Entry ===


def main():
    console.print(
        "[bold cyan]Welcome to StarCoder Secure Notepad[/bold cyan]\n"
    )

    global user, notes_files
    user = None

    while not user:
        panel = Panel.fit(
            "\n[bold yellow]1.[/bold yellow] Login\n"
            "[bold yellow]2.[/bold yellow] Register\n"
            "[bold yellow]3.[/bold yellow] Exit",
            title="[bold green]Login Menu[/bold green]",
            border_style="bright_magenta",
            box=box.ROUNDED,
        )
        console.print(panel)
        auth_choice = Prompt.ask("Choice an option", choices=["1", "2", "3"])

        if auth_choice == "1":
            user = login_user()
        elif auth_choice == "2":
            user = register_user()
        elif auth_choice == "3":
            console.print("[bold green]Goodbye![/bold green]")
            exit()
        else:
            console.print("[bold red]Invalid choice.[/bold red]")

    notes_files = f"notes_{user}.txt"
    show_due_alerts()

    while True:
        panel = Panel.fit(
            "[bold cyan]Welcome to SmartNotepad CLI[/bold cyan]🚀\n\n"
            "[bold yellow]1.[/bold yellow]✍ Write a note\n"
            "[bold yellow]2.[/bold yellow]📖 View Saved notes\n"
            "[bold yellow]3.[/bold yellow]✏️ Edit a note\n"
            "[bold yellow]4.[/bold yellow]🔍 Search notes\n"
            "[bold yellow]5.[/bold yellow]🗑️ Delete a note\n"
            "[bold yellow]6.[/bold yellow]💣 Delete ALL notes\n"
            "[bold yellow]7.[/bold yellow]🏷️ View notes by tag\n"
            "[bold yellow]8.[/bold yellow]🕐 View notes with due date\n"
            "[bold yellow]9.[/bold yellow] Export notes as JSON\n"
            "[bold yellow]10.[/bold yellow] Import notes as JSON\n"
            "[bold yellow]11.[/bold yellow]❌ Exit",
            title="[bold green]Main Menu[/bold green]",
            border_style="bright_magenta",
            box=box.ROUNDED,
        )
        console.print(panel)
        choice = Prompt.ask(
            "Please enter your choice (1/2/3/4/5/6/7/8/9/10/11)"
        ).strip()

        if choice == "1":
            # Write a note with optional tags and due date
            your_note = input("Enter your note: ").strip()
            your_tags = input(
                "Add tags (comma-separated, e.g., todo,idea) or press 'Enter' to skip: "
            ).strip()
            due_input = input("Add due date (YYYY-MM-DD) or leave blank: ").strip()

            tag_list = [
                f"#{tag.strip()}" for tag in your_tags.split(",") if tag.strip()
            ]
            due_text = ""

            if due_input:
                try:
                    due_date = datetime.strptime(due_input, "%Y-%m-%d")
                    due_text = f"[due:{due_date.strftime('%Y-%m-%d')}]"

                except ValueError:
                    print("Invalid date format. Skipping due date")

            full_notes = your_note
            if tag_list:
                full_notes += " " + " ".join((tag_list))

            if due_text:
                full_notes += "" + due_text

            sc_notes.append(full_notes)
            print("Note saved successfully!")
            print(sc_notes)

            # Save the note to the file
            with open(notes_file, "a") as file:  # 'a' to append
                file.write(full_notes + "\n")

        elif choice == "2":
            saved_notes = load_notes_from_file()
            if saved_notes:
                print("\nYour notes are:")
                for i, note in enumerate(saved_notes, 1):
                    print(f"{i}. {note}")
            else:
                print("No notes saved yet!.")

        elif choice == "3":
            saved_notes = load_notes_from_file()
            if saved_notes:
                print("\nYour saved notes.")
                for idx, note in enumerate(saved_notes, 1):
                    print(f"{idx}. {note}")

                edit_choice = int(
                    input("Choose the number of the note you want to edit: ")
                )
                if 1 <= edit_choice <= len(saved_notes):
                    original = saved_notes[edit_choice - 1]
                    parsed = parse_note(original)

                    print(f"Current note: {parsed['note']}")
                    print(
                        f"Current tags: {','.join(parsed['tags']) if parsed['tags'] else 'None'}"
                    )
                    print(
                        f"Current due date: {parsed['due_date'] if parsed['due_date'] else 'None'}"
                    )

                    new_note = input(
                        "Update note (leave blank to keep current): "
                    ).strip()
                    new_tags = input(
                        "Update tags (comma-separated) or leave blank: "
                    ).strip()
                    new_due = input(
                        "Update due date (YYYY-MM-DD) or leave blank: "
                    ).strip()

                    # Apply updates if provided
                    if new_note:
                        parsed["note"] = new_note

                    if new_tags:
                        parsed["tags"] = [
                            f"#{tag.strip()}"
                            for tag in new_tags.split(",")
                            if tag.strip()
                        ]

                    if new_due:
                        try:
                            datetime.strptime(new_due, "%Y-%m-%d")
                            parsed["due_date"] = new_due

                        except ValueError:
                            print("Invalid date format. Keeping existing due date.")

            # Rebuild note
            updated_note = build_note_from_json(parsed)
            if updated_note in saved_notes:
                print("This updated note already exists. Not saving duplicates..")
                return
            saved_notes[edit_choice - 1] = updated_note

            # Save back to file
            with open(notes_file, "w") as file:
                for note in saved_notes:
                    file.write(note + "\n")

            print("Note updated successfully!")

        elif choice == "4":
            saved_notes = load_notes_from_file()
            if not saved_notes:
                print("No notes saved yet!")
            else:
                search_term = input("Enter a keyword to search: ").strip().lower()
                matched_notes = [
                    note for note in saved_notes if search_term in note.lower()
                ]
                if matched_notes:
                    print("\nFound the following matching notes:")
                    for idx, note in enumerate(matched_notes, 1):
                        print(f"{idx}. {note}")
                else:
                    print("No matching notes found.")

        elif choice == "5":
            saved_notes = load_notes_from_file()
            if saved_notes:
                print("Your saved notes.")
                for idx, item in enumerate(saved_notes, 1):
                    print(f"{idx}. {item}")

                input_str = input(
                    "Enter note numbers to delete (comma-separated, e.g., 2, 3): "
                ).strip()
                try:
                    to_delete = [int(num.strip()) for num in input_str.split(",")]
                    to_delete = list(set(to_delete))  # removes duplicates

                    invalid = [
                        num for num in to_delete if num < 1 or num > len(saved_notes)
                    ]
                    if invalid:
                        print(f"Invalid note numbers: {invalid}")

                    else:
                        print("You are about to delete the following notes: ")
                        for i in sorted(to_delete):
                            print(f"{i}. {saved_notes[i - 1]}")

                        confirm = (
                            input("Are you sure? This cannot be undone (y/n): ")
                            .strip()
                            .lower()
                        )
                        if confirm == "y":
                            # Delete in reverse to avoid index shift issues
                            for i in sorted(to_delete, reverse=True):
                                del saved_notes[i - 1]

                            # Rewrite the file
                            with open(notes_file, "w") as file:
                                for note in saved_notes:
                                    file.write(note + "\n")

                            print("Selected notes deleted successfully.")

                        else:
                            print("Deletion cancelled.")

                except ValueError:
                    print("Please enter a valid numbers separated by commas.")

            else:
                print("No notes to delete.")

        elif choice == "6":
            saved_notes = load_notes_from_file()
            if not saved_notes:
                print("There are no notes to delete.")
            else:
                confirm = (
                    input(
                        "Are you absolutely sure you want to delete ALL notes? (y/n): "
                    )
                    .strip()
                    .lower()
                )
                if confirm == "y":
                    saved_notes.clear()
                    with open(notes_file, "w") as file:
                        pass  # Clears the file
                    print("All notes deleted successfully.")
                else:
                    print("Deletion cancelled. Your brain remains intact...")

        elif choice == "7":
            saved_notes = load_notes_from_file()
            if saved_notes:
                tag = input("Enter tag to filter by (e.g., #todo): ").strip()
                tagged = [note for note in saved_notes if tag in note]
                if tagged:
                    print(f"\nNotes tagged with {tag}: ")
                    for idx, note in enumerate(tagged, 1):
                        print(f"{idx}. {note}")
                else:
                    print("No notes found with that tag.")
            else:
                print("No notes saved yet.")

        elif choice == "8":

            # View notes with due dates
            saved_notes = load_notes_from_file()
            found = False
            today = datetime.today().date()

            print("\nNotes with Due Dates:")
            for idx, note in enumerate(saved_notes, 1):
                if "[due:" in note:
                    try:
                        due_str = note.split("[due:")[1].split("]")[0]
                        due_date = datetime.strptime(due_str, "%Y-%m-%d").date()

                        status = ""
                        if due_date < today:
                            status = "OVERDUE"
                        elif due_date == today:
                            status = "DUE TODAY"
                        else:
                            status = f"(Due in {(due_date - today).days} days)"

                        print(f"{idx}. {note} {status}")
                        found = True
                    except Exception:
                        continue
            if not found:
                print("No notes with valid due dates.")

        elif choice == "9":
            saved_notes = load_notes_from_file()
            parsed = [parse_note(n) for n in saved_notes]

            with open(f"{user}_notes_export.json", "w") as f:
                json.dump(parsed, f, indent=4)
            print(f"Exported {len(parsed)} notes to {user}_notes_export.json")

        elif choice == "10":
            try:
                with open(f"{user}_notes_export.json", "r") as f:
                    data = json.load(f)

                notes = [build_note_from_json(item) for item in data]

                with open(notes_file, "w") as file:
                    for note in notes:
                        file.write(note + "\n")

                print(f"Imported {len(notes)} notes from {user}_notes_export.json")

            except FileNotFoundError:
                print("No export file found.")
            except json.JSONDecodeError:
                console.print("[bold red]Invalid JSON format.[/bold red]")

        elif choice == "11":
            console.print("\n[bold green]Goodbye...[/bold green]")
            exit()

        else:
            console.print("[bold red]Invalid choice, please try again![/bold red]")


if __name__ == "__main__":
    main()
