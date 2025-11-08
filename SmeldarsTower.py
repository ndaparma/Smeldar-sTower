import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading
import builtins
import queue
import time
import sys




# We'll import main after monkey-patching so it doesn't execute the loop on import

class GuiTerminal:
    def __init__(self, root):
        self.root = root
        root.title('Smeldar\'s Tower')
        
        self.frame = tk.Frame(root,bg='darkred')
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.output = ScrolledText(self.frame, state='disabled', wrap='word', height=30, background='black', foreground='white', insertbackground='white', font=('Courier', 12))
        self.output.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        self.input_var = tk.StringVar()
        self.entry = tk.Entry(self.frame, textvariable=self.input_var, background="#2C2828", foreground='white', insertbackground='white', font=('Courier', 12))
        self.entry.pack(fill=tk.X, padx=6, pady=(0,6))
        self.entry.bind('<Return>', self.on_enter)

        # Directional buttons in diamond layout
        self.button_frame = tk.Frame(self.frame, background='darkred')
        self.button_frame.pack(pady=(0, 12))

        # Create directional buttons
        self.north_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='NORTH', width=10, command=lambda: self.action_input('NORTH'))
        self.east_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='EAST', width=10, command=lambda: self.action_input('EAST'))
        self.south_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='SOUTH', width=10, command=lambda: self.action_input('SOUTH'))
        self.west_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='WEST', width=10, command=lambda: self.action_input('WEST'))

        #Create regular action buttons
        self.Look_btn = tk.Button(self.button_frame, borderwidth=3, bg='#2C2828', fg='white', relief=tk.RAISED, text='LOOK', width=6, command=lambda: self.action_input('LOOK'))
        self.Search_btn = tk.Button(self.button_frame, borderwidth=3, bg='#2C2828', fg='white', relief=tk.RAISED, text='SEARCH', width=6, command=lambda: self.action_input('SEARCH'))
        self.map_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='MAP', width=6, command=lambda: self.action_input('MAP'))
        self.Yes_btn = tk.Button(self.button_frame, borderwidth=3, bg='#2C2828', fg='white', relief=tk.RAISED, text='YES', width=6, command=lambda: self.action_input('YES'))
        self.No_btn = tk.Button(self.button_frame, borderwidth=3, bg='#2C2828', fg='white', relief=tk.RAISED, text='NO', width=6, command=lambda: self.action_input('NO'))

        # Combat action buttons

        self.attack_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='ATTACK', width=8, command=lambda: self.action_input('ATTACK'))
        self.defend_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='DEFEND', width=8, command=lambda: self.action_input('DEFEND'))
        self.item_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='ITEM', width=8, command=lambda: self.action_input('ITEMS'))
        self.skill1_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='SKILL 1', width=8, command=lambda: self.action_input('SKILL 1'))
        self.skill2_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='SKILL 2', width=8, command=lambda: self.action_input('SKILL 2'))
        self.skill3_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='SKILL 3', width=8, command=lambda: self.action_input('SKILL 3'))
        self.skill4_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='SKILL 4', width=8, command=lambda: self.action_input('SKILL 4'))
        self.skill5_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='SKILL 5', width=8, command=lambda: self.action_input('SKILL 5'))
        self.flee_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='FLEE', width=8, command=lambda: self.action_input('FLEE'))

        # Helper action buttons

        
        self.stats_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='STATS', width=10, command=lambda: self.action_input('STATS'))
        self.equipment_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='EQUIPMENT', width=10, command=lambda: self.action_input('EQUIPMENT'))
        self.Settings_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='Settings', width=10, command=lambda: self.action_input('Settings'))
        self.save_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='SAVE', width=10, command=lambda: self.action_input('SAVE'))
        self.load_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='LOAD', width=10, command=lambda: self.action_input('LOAD'))
        self.help_btn = tk.Button(self.button_frame, borderwidth=5, bg='#2C2828', fg='white', relief=tk.RAISED, text='HELP', width=10, command=lambda: self.action_input('HELP'))

        # Diamond layout: (row, col)
        self.north_btn.grid(row=0, column=3, padx=2, pady=2)
        self.west_btn.grid(row=1, column=2, padx=2, pady=2)
        self.east_btn.grid(row=1, column=4, padx=2, pady=2)
        self.south_btn.grid(row=2, column=3, padx=2, pady=2)

        # Cross layout: (row, col)
        self.Look_btn.grid(row=0, column=2, padx=(2,2),pady=2, sticky='e') 
        self.Search_btn.grid(row=0, column=4, padx=(2,2), pady=2 , sticky='w')
        self.map_btn.grid(row=1, column=3, padx=2, pady=2)
        self.Yes_btn.grid(row=2, column=2, padx=(2,2), pady=2, sticky='e')
        self.No_btn.grid(row=2, column=4, padx=(2,2), pady=2, sticky='w')
        

        # Vertical layout: (row, col)
        self.attack_btn.grid(row=0, column=6, padx=(65,2), pady=2)
        self.defend_btn.grid(row=1, column=6, padx=(65,2), pady=2)
        self.item_btn.grid(row=2, column=6, padx=(65,2), pady=2)
        self.skill1_btn.grid(row=0, column=7, padx=(2,2), pady=2)
        self.skill2_btn.grid(row=1, column=7, padx=(2,2), pady=2)
        self.skill3_btn.grid(row=2, column=7, padx=(2,2), pady=2)
        self.skill4_btn.grid(row=0, column=8, padx=(2,2), pady=2)
        self.skill5_btn.grid(row=1, column=8, padx=(2,2), pady=2)
        self.flee_btn.grid(row=2, column=8, padx=(2,2), pady=2)

        self.Settings_btn.grid(row=2, column=1, padx=(2,100), pady=2)
        self.stats_btn.grid(row=1, column=0, padx=(2,2), pady=2)
        self.equipment_btn.grid(row=1, column=1, padx=(2,100), pady=2)

        self.save_btn.grid(row=0, column=0, padx=(2,2), pady=2)
        self.load_btn.grid(row=0, column=1, padx=(2,100), pady=2)
        self.help_btn.grid(row=2, column=0, padx=(2,2), pady=2)

        # Queues for communication
        self.input_queue = queue.Queue()
        self.print_queue = queue.Queue()

        # Periodically flush the print queue to the text widget
        self.poll_print_queue()

        # Periodically update skill buttons to reflect the player's learned skills
        self.poll_skill_buttons()

    def action_input(self, inputActions):
        # Echo the input in the terminal and inject into input queue //
        self.write("> " + inputActions + "\n")
        self.input_queue.put(inputActions)


    def on_enter(self, event=None):
        P_Input = self.input_var.get()
        self.input_var.set('')
        # Echo the player's input into the output area so it appears in the terminal
        # and then put into input queue for the game's input() to consume
        try:
            self.write("\n> " + P_Input + "\n\n")
        except Exception:
            pass
        self.input_queue.put(P_Input)
        return 'break'

    def write(self, text):
        # Called by our patched print to queue text for GUI
        self.print_queue.put(str(text))

    def poll_print_queue(self):
        try:
            while True:
                item = self.print_queue.get_nowait()
                self.output.configure(state='normal')
                self.output.insert(tk.END, item)
                self.output.see(tk.END)
                self.output.configure(state='disabled')
        except Exception:
            pass
        self.root.after(50, self.poll_print_queue)

    def get_input(self, prompt=''):
        # Show prompt in output
        if prompt:
            self.write(prompt)
        # Block until input is available
        try:
            P_Input = self.input_queue.get()
            return P_Input
        except Exception:
            return ''

    def poll_skill_buttons(self):
        """Update skill button labels, commands, and enabled state based on p1.skills in main module."""
        try:
            mod = sys.modules.get('main')
            p1 = getattr(mod, 'p1', None) if mod is not None else None
            skills = list(getattr(p1, 'skills', [])) if p1 is not None else []
        except Exception:
            skills = []

        # Update up to 5 skill buttons
        for i in range(5):
            btn_name = f'skill{i+1}_btn'
            btn = getattr(self, btn_name, None)
            if btn is None:
                continue
            if i < len(skills):
                skill_name = skills[i]
                # update label and enable button
                try:
                    btn.config(text=skill_name, state='normal')
                    # bind to send the exact skill name when clicked
                    btn.config(command=(lambda name=skill_name: self.action_input(name)))
                except Exception:
                    pass
            else:
                # no skill learned for this slot: disable button
                try:
                    btn.config(text=f'SKILL {i+1}', state='disabled')
                    btn.config(command=(lambda name=f'SKILL {i+1}': self.action_input(name)))
                except Exception:
                    pass

        # check again in 800ms
        try:
            self.root.after(800, self.poll_skill_buttons)
        except Exception:
            pass


def start_gui():
    root = tk.Tk()
    term = GuiTerminal(root)

    # Monkey-patch builtins.input and builtins.print so main.py uses GUI
    #orig_input = builtins.input
    #orig_print = builtins.print

    def gui_input(prompt=''):
        # Use the GUI to display the prompt and wait for input        
        return term.get_input(prompt)
    

    def gui_print(*args, sep=' ', end='\n', file=None, flush=False):
        text = sep.join(str(a) for a in args) + end
        term.write(text)

    builtins.input = gui_input
    builtins.print = gui_print

    # Also patch print_slow (from slowprint module) after importing it
    import Settings
    def gui_print_slow(text, typingActive='OFF', char_delay=0.01):
        """Print text to the GUI with an optional typing animation.

        If typingActive == 'ON', characters are sent one-by-one with a short
        sleep between characters to emulate the original console typing effect.
        Otherwise the whole text is written immediately.
        This function blocks the game thread while emitting characters so the
        original timing/ordering of printed text is preserved.
        """
        s = str(text)
        if typingActive == 'ON':
            # Emit characters one at a time
            for ch in s:
                gui_print(ch, end='')
                time.sleep(char_delay)
            # Ensure a newline at end if original text didn't include one
            if not s.endswith('\n'):
                gui_print('', end='\n')
        else:
            gui_print(s)

    Settings.print_slow = gui_print_slow

    # Run main.run_game in a background thread so the GUI remains responsive
    def run_game_thread():
        try:
            import main
            # Ensure modules which imported print_slow get the GUI version.
            # slowprint was already patched above; make sure main and other
            # common modules reference the same function object so their
            # calls go to the GUI.
            try:
                import Settings as _slow_mod
            except Exception:
                _slow_mod = None

            if _slow_mod is not None:
                gui_ps = _slow_mod.print_slow
                # update main module
                try:
                    setattr(main, 'print_slow', gui_ps)
                except Exception:
                    pass
                # update other likely modules if they exist and imported print_slow
                import sys as _sys
                for name in ('character', 'combat', 'world'):
                    if name in _sys.modules:
                        mod = _sys.modules[name]
                        try:
                            if hasattr(mod, 'print_slow'):
                                setattr(mod, 'print_slow', gui_ps)
                        except Exception:
                            pass

            # call run_game to start the game loop
            main.run_game()
        except SystemExit:
            root.destroy()  
            pass
        except Exception as e:
            gui_print('\n[Critical Error. Please close the game.] ' + str(e) + '\n')

    t = threading.Thread(target=run_game_thread, daemon=True)
    t.start()

    root.mainloop()


if __name__ == '__main__':
    start_gui()
