import tkinter as tk
import random
import requests
from tkinter import messagebox
import tkinter.ttk as ttk
import math
import json

lyrics_database = {
    "And I know I'm gonna be with you so I take my time.": "Taylor Swift - Wildest Dreams",
    "We could get married, have a few kids and live in the suburbs.": "Taylor Swift - Love Story",
    "I'd like to be my old self again, but I'm still trying to find it.": "Taylor Swift - All Too Well",
    "I once believed love would be burning red, but it's golden.": "Taylor Swift - Lover",
    "You should've been there, should've burst through the door.": "Taylor Swift - All Too Well",
    "But I got smarter, I got harder in the nick of time.": "Taylor Swift - Blank Space",
    "My mind forgets to remind me, your a bad idea.": "Taylor Swift - I Knew You Were Trouble",
    "The rain came pouring down, when I was drowning, that's when I could finally breathe.": "Taylor Swift - Clean",
    "In dreams, I meet you in warm conversation.": "Taylor Swift - Enchanted",
    "So I'll watch your life in pictures like I used to watch you sleep.": "Taylor Swift - Last Kiss",
    "My baby's fly like a jet stream, high above the whole scene.": "Taylor Swift - Call It What You Want",
    "They say all's well that ends well, but I'm in a new hell every time you double-cross my mind.": "Taylor Swift - Right Where You Left Me",
    "We're happy, free, confused, and lonely at the same time.": "Taylor Swift - 22",
    "And I lived in your chess game, but you changed the rules every day.": "Taylor Swift - White Horse",
    "Long live all the mountains we moved, I had the time of my life fighting dragons with you.": "Taylor Swift - Long Live",
    "I'm not a princess, this ain't a fairy tale.": "Taylor Swift - White Horse",
    "I'm captivated by you, baby, like a fireworks show.": "Taylor Swift - Sparks Fly",
    "I'm shining like fireworks over your sad, empty town.": "Taylor Swift - Dear John",
    "You call me up again just to break me like a promise.": "Taylor Swift - All Too Well",
    "So don't you worry your pretty little mind, people throw rocks at things that shine.": "Taylor Swift - Ours",
    "My reputation's never been worse, so you must like me for me.": "Taylor Swift - Delicate",
    "Just because you're clean, don't mean you don't miss it.": "Taylor Swift - Clean",
    "I never miss a beat, I'm lightning on my feet.": "Taylor Swift - Style",
    "The best people in life are free.": "Taylor Swift - New Romantics",
    "I could build a castle out of all the bricks they threw at me.": "Taylor Swift - New Romantics",
    "They're burning all the witches even if you aren't one.": "Taylor Swift - I Did Something Bad",
    "The monsters turned out to be just trees.": "Taylor Swift - Out of The Woods",
    "And I'll be 1989, you and me.": "Taylor Swift - Dress",
    "But we are alone, just you and me, up in your room and our slates are clean.": "Taylor Swift - Holy Ground",
    "I'm dying to know, is it killing you like it's killing me?": "Taylor Swift - I Almost Do",
    "The rest of the world was black and white, but we were in screaming color.": "Taylor Swift - Out of The Woods",
    "I don't wanna look at anything else now that I saw you.": "Taylor Swift - Style",
    "You're still all over me like a wine-stained dress I can't wear anymore.": "Taylor Swift - Delicate",
    "My heart's been borrowed and yours has been blue.": "Taylor Swift - Lover",
}



class LyricsGameGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Taylor Swift Lyrics Game - Score: 0")  # Set title directly

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        window_width = 600
        window_height = 400
        x = math.floor((screen_width - window_width) / 2)
        y = math.floor((screen_height - window_height) / 2)
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.score = 0
        self.num_questions = 5
        self.current_question = 0

        self.question_text = tk.StringVar()
        self.choices_text = [tk.StringVar() for _ in range(4)]

        self.question_label = tk.Label(master, textvariable=self.question_text, wraplength=500,
                                       font=("Helvetica", 16, "bold"), bg="#ffffff", fg="#333333")
        self.question_label.pack(pady=20)

        self.button_styles = []
        self.choices_buttons = []  # Add the choices_buttons attribute here
        for i in range(4):
            style_name = f"Color{i}.TButton"
            style = ttk.Style()
            style.map(style_name,
                      background=[("active", "black"), ("!active", "black")],
                      foreground=[("active", "purple"), ("!active", "purple")])
            self.button_styles.append(style)

            choice_button = ttk.Button(master, textvariable=self.choices_text[i], width=40,
                                       command=lambda idx=i: self.check_selection(idx), style=style_name)
            choice_button.pack(pady=20)
            self.choices_buttons.append(choice_button)
        self.next_question()

    def update_title(self):
        self.master.title(f"Taylor Swift Lyrics Game - Score: {self.score}")

    def next_question(self):
        if self.current_question >= self.num_questions:
            messagebox.showinfo("Game Over", f"Your final score is {self.score}/{self.num_questions}")
            self.master.destroy()
            return

        question, answer = get_random_question()
        choices = random.sample(list(lyrics_database.values()), k=3)
        choices.append(answer)
        random.shuffle(choices)

        self.question_text.set(question)
        for i in range(4):
            self.choices_text[i].set(choices[i])

        # Generate color palette using Colormind API
        palette = generate_color_palette()
        if palette:
            # Assign a unique color to each choice button from the generated palette
            for i, button in enumerate(self.choices_buttons):
                color = palette[i % len(palette)]
                bg_color = rgb_to_hex(color)

                style = ttk.Style()
                style_name = f"Color{i}.TButton"
                style.configure(style_name, background=bg_color, foreground="#ffffff")

                button.configure(style=style_name)

            # Assign a color to the master window and the question label
            color = palette[-1]
            bg_color = rgb_to_hex(color)
            self.master.configure(bg=bg_color)
            self.question_label.configure(bg=bg_color)

        self.current_question += 1

    def check_selection(self, selected):
        if check_answer(self.question_text.get(), [choice.get() for choice in self.choices_text],
                        lyrics_database[self.question_text.get()], selected):
            self.score += 1
            self.update_title()  # Update title here
        self.next_question()


def get_random_question():
    question = random.choice(list(lyrics_database.keys()))
    answer = lyrics_database[question]
    return question, answer


def check_answer(question, choices, answer, selected):
    if choices[selected] == answer:
        messagebox.showinfo("Result", "Correct!")
        return True
    else:
        messagebox.showinfo("Result", f"Wrong! The correct answer is:\n{answer}")
        return False


def generate_color_palette():
    url = 'http://colormind.io/api/'
    data = {
        'model': 'default'
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = json.loads(response.content)
        colors = result['result']
        return colors
    else:
        print(f"Failed to generate color palette. Error: {response.status_code}")
        return None


def rgb_to_hex(color):
    return f"#{''.join(f'{c:02x}' for c in color)}"


def play_game():
    root = tk.Tk()
    root.config(bg="#111111")
    ttk.Style().configure('TButton', font=('Helvetica', 14), foreground='black')
    game = LyricsGameGUI(root)
    root.mainloop()


if __name__ == "__main__":
    play_game()
