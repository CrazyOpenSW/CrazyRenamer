# 📂 Advanced Selective File Renamer

A powerful Python GUI tool for bulk file renaming. Unlike standard renamers, this software allows you to define precise transformations using an instruction-based syntax, enabling you to manipulate filenames by position, content, or extension.

## ✨ Key Features

- **Intuitive Interface**: Simple file selection via standard dialog windows.
- **Real-time Preview**: See exactly how files will be renamed before applying any changes.
- **Flexible Syntax**: Supports a wide range of commands to crop, replace, add, or filter parts of the filename.
- **Safety First**: Requires explicit confirmation before proceeding with the final operation.

## 🛠 Renaming Instructions (Syntax)

Instructions are entered in the text field and can be separated by commas to be applied sequentially.

| Command | Description | Example | Result (on `old_document.pdf`) |
| :--- | :--- | :--- | :--- |
| **`X-Y`** | **Keep** only characters from position X to Y. Everything else is deleted. | `1-5` | `old_d.pdf` |
| **`D X`** | **Delete** the single character at position X. | `D 1` | `ld_document.pdf` |
| **`DEL X-Y`** | **Delete** the block of characters from position X to Y. | `DEL 5-9` | `old_ument.pdf` |
| **`R X=TEXT`** | **Replace** the character at position X with the specified text. | `R 1=A` | `Ald_document.pdf` |
| **`S OLD=NEW`** | **Replace** all occurrences of OLD with NEW (if NEW is empty, OLD is removed). | `S old=new` | `new_document.pdf` |
| **`L N`** | **Delete N** characters immediately before the extension. | `L 3` | `old_docume.pdf` |
| **`A TEXT`** | **Add** text to the beginning of the name (Prefix). | `A backup_` | `backup_old_document.pdf` |
| **`Z TEXT`** | **Add** text to the end of the name, before the extension (Suffix). | `Z _v1` | `old_document_v1.pdf` |
| **`C X`** | **Cut** (delete) from the start up to character X (exclusive). | `C 5` | `document.pdf` |
| **`T X`** | **Cut** from character X (inclusive) to the end of the name. | `T 10` | `old_docum.pdf` |
| **`E .EXT`** | **Change Extension** to .EXT. | `E .txt` | `old_document.txt` |

> **Note:** For position-based commands (`D`, `DEL`, `R`, `X-Y`), the count starts at **1** and includes both the filename and the extension.

## 🚀 Installation and Setup

### Windows Portable Version (Recommended)
A pre-compiled portable version is available as **`CrazyRenamer.exe`**. You don't need to install Python to use it:
1. Download **`CrazyRenamer.exe`** from the **Releases** section.
2. Run the application directly.

### Source Code Setup
If you prefer to run the code or contribute:
If you prefer to run the code or contribute:

#### Prerequisites
You must have Python installed on your system.
- [Download Python](https://www.python.org/downloads/)

#### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/CrazyOpenSW/CrazyRenamer.git
   cd CrazyRenamer
   ```

#### Running the App
The application uses only standard Python libraries (`tkinter`, `os`), so no external packages are required. Start the program with:
```bash
python main.py
```

## 📖 How to Use

1. **Select Files**: Click the "Select Files" button and choose the files you wish to rename.
2. **Enter Instructions**: Type the desired commands in the text field. You can combine them, e.g.: `DEL 5-8, R 9=X, S old=new`.
3. **Preview**: Click "Preview Rename" to see the list of new names without actually modifying the files.
4. **Execute**: If the preview looks correct, click the yellow **"RENAME FILES!"** button to apply changes permanently.

## ⚠️ Warning
The renaming operation is **permanent** and cannot be undone through the software. It is strongly recommended to always use the preview and, if necessary, create a backup of your files before proceeding.

---

## 📄 License & Author

**Author:** CrazyOpenSW

This project is licensed under the **MIT License**. This means it is open-source and you are free to use, copy, modify, and distribute the software for any purpose, provided that the original copyright notice and permission notice are included.
