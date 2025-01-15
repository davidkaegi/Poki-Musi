
import mido
from mido.messages.messages import Message

class MusicPlayer:

    def __init__(self, midi_path, hw) -> None:
        self.messages = []
        for msg in mido.MidiFile(midi_path):
            self.messages.append(msg)
        self.hw = hw
        self.time = 0
        self.curr_msg = 0
        self.notes_on = [-1, -1]
    
    def tick(self):
        self.time += 1 / 60 
        while self.time >= self.messages[self.curr_msg].time:
            msg = self.messages[self.curr_msg]
            self.time -= msg.time
            if msg.type == 'note_on' and msg.velocity > 0:
                for i in range(len(self.notes_on)):
                    if self.notes_on[i] == -1:
                        self.hw.note_on(i, 110 * (2 ** ((msg.note - 57) / 12)))
                        self.notes_on[i] = msg.note
                        break
            if msg.type == 'note_on' and msg.velocity == 0:
                for i in range(len(self.notes_on)):
                    if self.notes_on[i] == msg.note:
                        self.hw.note_off(i)
                        self.notes_on[i] = -1 
                        break

            self.curr_msg += 1 
            self.curr_msg %= len(self.messages)
