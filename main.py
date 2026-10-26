import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import os

class FileRenamerApp:
    def __init__(self, master):
        self.master = master
        master.title("Rinomina File Selettiva Avanzata")

        self.selected_files = []

        master.grid_rowconfigure(2, weight=1) 
        master.grid_columnconfigure(0, weight=1)

        main_frame = tk.Frame(master)
        main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # --- 1. Selezione File e Display ---
        tk.Label(main_frame, text="**1. Seleziona i File**", font=('Arial', 10, 'bold')).pack(pady=(0, 5))
        self.btn_select = tk.Button(main_frame, text="Seleziona File", command=self.select_files)
        self.btn_select.pack(pady=5)

        tk.Label(main_frame, text="File Selezionati:").pack(anchor='w')
        
        file_frame = tk.Frame(main_frame)
        file_frame.pack(fill='both', expand=True, pady=5)
        file_frame.grid_rowconfigure(0, weight=1)
        file_frame.grid_columnconfigure(0, weight=1)
        
        self.file_list_display = scrolledtext.ScrolledText(file_frame, height=8, width=70, state=tk.DISABLED)
        self.file_list_display.grid(row=0, column=0, sticky="nsew")
        
        # --- 2. Istruzioni e Legenda ---
        tk.Label(main_frame, text="").pack()
        tk.Label(main_frame, text="**2. Istruzioni di Rinomina**", font=('Arial', 10, 'bold')).pack(pady=(5, 0))

        legend_text = (
            "Sintassi Istruzioni (separate da virgola): \n"
            "• **X-Y**: **Mantieni** i caratteri dalla posizione **X** alla **Y** (entrambi inclusi). **TUTTO** il resto viene eliminato. Esempio: `1-3`\n"
            "• **D X**: **Elimina** il carattere alla posizione **X**. Esempio: `D 4`\n"
            "• **DEL X-Y**: **Elimina** il blocco di caratteri dalla posizione **X** alla **Y** (inclusi). Esempio: `DEL 5-8`\n"
            "• **R X=TESTO**: **Sostituisci** il carattere alla posizione **X** con TESTO. Esempio: `R 10=NEW`\n"
            "• **S OLD=NEW**: **Sostituisci** tutte le occorrenze di OLD con NEW. Se NEW è vuoto, OLD viene eliminato. Esempio: `S _OLD=_`\n"
            "• **L N**: **Elimina N** caratteri **prima** dell'estensione. Esempio: `L 3`\n"
            "• **A TESTO**: **Aggiungi** TESTO all'inizio del nome.\n"
            "• **Z TESTO**: **Aggiungi** TESTO alla fine del nome (prima dell'estensione).\n"
            "• **C X**: **Taglia** dall'inizio fino al carattere **X** (escluso) del nome (esclusa estensione). Esempio: `C 5`\n"
            "• **T X**: **Taglia** dal carattere **X** (incluso) fino alla fine del nome (esclusa estensione). Esempio: `T 5`\n"
            "• **E .EST**: **Cambia Estensione** in .EST. Esempio: `E .png`\n"
            
            "\n*Nota: Le posizioni (X, Y) per DEL, D, R, e X-Y iniziano da **1** e includono nome ed estensione.*"
        )
        tk.Label(main_frame, text=legend_text, justify=tk.LEFT, relief=tk.GROOVE, padx=5, pady=5).pack(fill='x', pady=5)


        tk.Label(main_frame, text="Inserisci Istruzioni (Suggerimento per test: DEL 5-8, R 9=X, S old=new):").pack(anchor='w')
        self.rename_instruction = tk.Entry(main_frame, width=70)
        self.rename_instruction.insert(0, "1-19") 
        self.rename_instruction.pack(fill='x')

        self.btn_preview = tk.Button(main_frame, text="3. Anteprima Rinomina", command=self.preview_rename)
        self.btn_preview.pack(pady=10)

        # --- 4. Anteprima e Pulsante di Esecuzione ---
        
        tk.Label(main_frame, text="Anteprima Nomi Rinominati:").pack(anchor='w')
        
        preview_frame = tk.Frame(main_frame)
        preview_frame.pack(fill='both', expand=True, pady=5)
        preview_frame.grid_rowconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)

        self.preview_display = scrolledtext.ScrolledText(preview_frame, height=8, width=70, state=tk.DISABLED)
        self.preview_display.grid(row=0, column=0, sticky="nsew")
        
        self.btn_rename = tk.Button(main_frame, text="4. RINOMINA I FILE! (Operazione definitiva)", command=self.execute_rename, fg="red", bg="yellow")
        self.btn_rename.pack(pady=(15, 0))

    # --- FUNZIONI DI BASE ---
    
    def select_files(self):
        f_names = filedialog.askopenfilenames(title="Seleziona i file da rinominare")
        self.selected_files = list(f_names)
        
        self.file_list_display.config(state=tk.NORMAL)
        self.file_list_display.delete(1.0, tk.END)
        if self.selected_files:
            for f in self.selected_files:
                self.file_list_display.insert(tk.END, os.path.basename(f) + "\n")
        else:
            self.file_list_display.insert(tk.END, "Nessun file selezionato.")
            
        self.file_list_display.config(state=tk.DISABLED)
        self.preview_display.config(state=tk.NORMAL)
        self.preview_display.delete(1.0, tk.END)
        self.preview_display.config(state=tk.DISABLED)

    # --- LOGICA AVANZATA DI RINOMINA (CORRETTA) ---
    def apply_rename_logic(self, original_name, instructions):
        name, ext = os.path.splitext(original_name)
        full_name_to_modify = name + ext 
        parts = [p.strip() for p in instructions.split(',') if p.strip()]
        
        # Variabili che possono essere modificate dalle istruzioni
        current_name_base = name
        
        chars_to_keep_explicit = set() # Caratteri da mantenere solo se c'è X-Y
        chars_to_delete = set()       # Caratteri da eliminare (D, DEL)
        replacements_index = {}       # Caratteri da sostituire (R)
        
        string_replacements = {}
        prefix = ""
        suffix = ""
        new_ext = ext
        
        # Bandiere per rilevare l'uso delle varie logiche
        index_logic_used = False
        mantieni_range_used = False # Rileva se è stato usato X-Y
        string_logic_used = False
        
        # --- PRIMO PASSAGGIO: Analisi e pre-processamento (C, T, L sono applicate QUI sul nome originale) ---
        temp_name_base = name 
        
        for part in parts:
            try:
                # Logica basata sull'indice (Raccolta indici da mantenere, eliminare e sostituire)
                if '-' in part and not part.startswith('DEL '):
                    # MANTIENI ESPLICITO: X-Y (Attiva la modalità "filtro")
                    index_logic_used = True
                    mantieni_range_used = True
                    start, end = map(int, part.split('-'))
                    for i in range(start - 1, end): 
                        chars_to_keep_explicit.add(i)
                elif part.startswith('R ') and '=' in part:
                    # SOSTITUISCI PER INDICE: R X=TESTO
                    index_logic_used = True
                    idx_part, new_text = part[2:].split('=', 1)
                    index_to_replace = int(idx_part) - 1
                    replacements_index[index_to_replace] = new_text
                elif part.startswith('D ') and part[2:].isdigit():
                    # ELIMINA SINGOLO: D X
                    index_logic_used = True
                    index_to_delete = int(part[2:]) - 1
                    chars_to_delete.add(index_to_delete)
                elif part.startswith('DEL ') and '-' in part[4:]:
                    # ELIMINA RANGE: DEL X-Y
                    index_logic_used = True
                    range_part = part[4:].strip()
                    start, end = map(int, range_part.split('-'))
                    for i in range(start - 1, end):
                        chars_to_delete.add(i)

                # Logica basata sul nome base (C, T, L)
                elif part.startswith('L ') and part[2:].isdigit():
                    num_chars = int(part[2:])
                    if num_chars > 0: temp_name_base = temp_name_base[:-num_chars]
                elif part.startswith('C ') and part[2:].isdigit():
                    index_start = int(part[2:]) - 1
                    if index_start < 0: index_start = 0
                    temp_name_base = temp_name_base[index_start:]
                elif part.startswith('T ') and part[2:].isdigit():
                    index_end = int(part[2:]) - 1
                    if index_end < 0: index_end = 0
                    temp_name_base = temp_name_base[:index_end]

                # Logica basata su stringa/prefisso/suffisso/estensione
                elif part.startswith('S ') and '=' in part:
                    string_logic_used = True
                    old_str, new_str = part[2:].split('=', 1)
                    string_replacements[old_str] = new_str
                elif part.startswith('A '):
                    prefix = part[2:].strip()
                elif part.startswith('Z '):
                    suffix = part[2:].strip()
                elif part.startswith('E .'):
                    new_ext = part[2:].strip()
                    if not new_ext.startswith('.'): new_ext = '.' + new_ext
                else:
                    return f"Errore: Istruzione non valida o incompleta: {part}"
            except ValueError:
                return f"Errore: Formato numerico non valido in: {part}"
            except IndexError:
                return f"Errore: Indice fuori limite: {part}"

        # Assegniamo il risultato delle operazioni C, T, L al nome base
        current_name_base = temp_name_base
        
        # --- SECONDO PASSAGGIO: Applicazione Logica Basata sulle Stringhe (S) ---
        processed_full_name = full_name_to_modify
        if string_logic_used:
            for old, new in string_replacements.items():
                processed_full_name = processed_full_name.replace(old, new)
            
        name_base_after_string_logic, _ = os.path.splitext(processed_full_name)


        # --- TERZO PASSAGGIO: Determinazione del Nome Base Finale (Correzione Logica Indice) ---
        
        final_base_name_result = current_name_base # Risultato di C, T, L (se usate)
        
        if index_logic_used:
            # Se è stata usata la logica indice, dobbiamo ricostruire il nome
            result_by_index = []
            string_to_process = processed_full_name 
            
            # --- CORREZIONE CHIAVE ---
            # Se NON è stato usato X-Y (Mantieni Range), dobbiamo mantenere tutto di default
            # e poi eliminare solo ciò che è specificato da D/DEL.
            if not mantieni_range_used:
                # In assenza di X-Y, consideriamo TUTTI gli indici come da mantenere (e poi togliamo D/DEL)
                chars_to_keep_default = set(range(len(string_to_process)))
                
                # Rimuoviamo gli indici specificati da D e DEL
                chars_to_keep_final = chars_to_keep_default - chars_to_delete
            else:
                # Se X-Y è stato usato, manteniamo SOLO ciò che è in chars_to_keep_explicit 
                # e rispettiamo le eliminazioni D/DEL e le sostituzioni R.
                chars_to_keep_final = chars_to_keep_explicit - chars_to_delete
            # -------------------------
            
            for i, char in enumerate(string_to_process):
                if i in replacements_index:
                    # R X=TESTO (Priorità massima)
                    result_by_index.append(replacements_index[i])
                elif i in chars_to_keep_final:
                    # Carattere mantenuto (X-Y o Default - D/DEL)
                    result_by_index.append(char)
                # Altrimenti, il carattere è eliminato
            
            final_base_name_full = "".join(result_by_index)
            final_base_name_result, _ = os.path.splitext(final_base_name_full)
        
        elif string_logic_used:
            # Se è stata usata solo S (e C/T/L non sono state usate)
            final_base_name_result = name_base_after_string_logic
            
        # Altrimenti, final_base_name_result rimane il risultato di C, T, L.


        # --- QUARTO PASSAGGIO: Applicazione Prefisso/Suffisso e Estensione finale ---
        
        final_name = prefix + final_base_name_result + suffix + new_ext
        
        return final_name

    # --- FUNZIONI DI ESECUZIONE (Rimaste invariate) ---

    def preview_rename(self):
        if not self.selected_files:
            messagebox.showwarning("Avviso", "Seleziona prima dei file.")
            return

        instructions = self.rename_instruction.get()
        if not instructions:
            messagebox.showwarning("Avviso", "Inserisci le istruzioni di rinomina.")
            return

        self.preview_display.config(state=tk.NORMAL)
        self.preview_display.delete(1.0, tk.END)

        for full_path in self.selected_files:
            original_name = os.path.basename(full_path)
            new_name = self.apply_rename_logic(original_name, instructions)
            
            self.preview_display.insert(tk.END, f"{new_name}\n")

        self.preview_display.config(state=tk.DISABLED)

    def execute_rename(self):
        if not self.selected_files:
            messagebox.showwarning("Avviso", "Seleziona prima dei file.")
            return

        instructions = self.rename_instruction.get()
        if not instructions:
            messagebox.showwarning("Avviso", "Inserisci le istruzioni di rinomina.")
            return
            
        if not messagebox.askyesno("Conferma Rinomina", f"Sei sicuro di voler rinominare {len(self.selected_files)} file? Questa operazione non è annullabile."):
            return

        count = 0
        for full_path in self.selected_files:
            directory = os.path.dirname(full_path)
            original_name = os.path.basename(full_path)
            
            new_name = self.apply_rename_logic(original_name, instructions)
            
            if new_name.startswith("Errore"):
                print(f"Skipping {original_name}: {new_name}")
                continue 
            
            new_full_path = os.path.join(directory, new_name)

            try:
                os.rename(full_path, new_full_path)
                count += 1
            except Exception as e:
                messagebox.showerror("Errore Rinomina", f"Impossibile rinominare {original_name} in {new_name}. Errore: {e}")

        messagebox.showinfo("Completato", f"Rinomina completata. {count} file rinominati con successo.")
        self.selected_files = []
        self.file_list_display.config(state=tk.NORMAL)
        self.file_list_display.delete(1.0, tk.END)
        self.file_list_display.insert(tk.END, "Nessun file selezionato.")
        self.file_list_display.config(state=tk.DISABLED)
        self.preview_display.config(state=tk.NORMAL)
        self.preview_display.delete(1.0, tk.END)
        self.preview_display.config(state=tk.DISABLED)

# --- Avvio dell'applicazione GUI ---
if __name__ == "__main__":
    root = tk.Tk()
    app = FileRenamerApp(root)
    root.mainloop()
