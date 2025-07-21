# SmartNotepad CLI - A Smart, Secure Notes CLI

> "For Coders who take notes like developers."
> _Built with ❤️ by StarCoder

---

## 🚀 Overview

SmartNotepad CLI is a feature-rich command-line notepad that lets you:

- ✍️ Write, edit, search, and delete notes
- 🏷️ Tag and organize your thoughts
- 🕐 Track due dates and receive alerts
- 🔐 Register and log in securely
- 📦 Import/export notes as JSON
- 🖥️ Enjoy a beautiful CLI with `rich` formatting

Perfect for developers, researchers, or anyone who prefers quick terminal-based productivity.

---

## 📁 Project Structure

smartnotepad-cli/

├── smartnotepad/ # Main application package

│ ├── init.py

│ └── app.py # Main CLI logic

├── users.txt # Stores user credentials (SHA-256 hashed)

├── sample_data/ # Optional example files

├── README.md

├── .gitignore

└── requirements.txt


---

## ⚙️ Features

- **Secure Login & Registration**  
  SHA-256 hashed passwords stored in `users.txt`.

- **Rich CLI UI**  
  Styled with the [`rich`](https://github.com/Textualize/rich) library for better UX.

- **Smart Notes**  
  Add tags (`#todo`, `#idea`) and due dates like `[due:2025-08-01]`.

- **Task Alerts**  
  Automatically alerts overdue or due-today tasks.

- **Data Persistence**  
  Notes are saved in a file per user: `notes_<username>.txt`.

- **Editing & Deletion**  
  Edit or remove notes by number.

- **Filtering**  
  Search by keyword, tag, or due date.

- **Data Portability**  
  Export/import notes in JSON format.

---

## 📦 Installation

1. **Clone this repo**

   ```bash
   git clone https://github.com/StarCoderSC/smartnotepad-cli.git
   cd secondmind-cli

    Create a virtual environment (optional but recommended)

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies

    pip install -r requirements.txt

🛠 Requirements

    Python 3.7+

    rich for UI rendering

Install manually (if needed):

pip install rich

🔑 Usage

Run the CLI:

python -m smartnotepad.app

You'll be prompted to login or register. From there, enjoy a powerful, stylish CLI to manage your thoughts!
🧪 Sample Note Syntax

    Learn Typer CLI #todo #python [due:2025-07-30]

    ✅ Tags start with #
    📅 Due dates follow [due:YYYY-MM-DD]

