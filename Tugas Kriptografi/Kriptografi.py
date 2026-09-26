class EnigmaRotor:

  def __init__(self, wiring, notch, ring_setting=1, position="A"):
    self.wiring = wiring
    self.notch = notch
    self.ring_setting = ring_setting - 1
    self.position = ord(position) - 65

  def step(self):
    self.position = (self.position + 1) % 26

  def is_at_notch(self):
    return chr(self.position + 65) == self.notch

  def forward(self, c_idx):
    shift = self.position - self.ring_setting

    input_idx = (c_idx + shift) % 26
    out_char = self.wiring[input_idx]

    out_idx = (ord(out_char) - 65 - shift) % 26

    return out_idx

  def backward(self, c_idx):
    shift = self.position - self.ring_setting

    input_idx = (c_idx + shift) % 26
    out_char = chr(input_idx + 65)

    target_idx = self.wiring.index(out_char)
    out_idx = (target_idx - shift) % 26

    return out_idx


class EnigmaMachine:

  def __init__(
      self,
      rotors,
      reflector,
      ring_settings,
      initial_positions,
      plugboard_pairs,
  ):

    ROTOR_WIRINGS = {
        "I": ("EKMFLGDQVZNTOWYHXUSPAIBRCJ", "Q"),
        "II": ("AJDKSIRUXBLHWTMCQGZNPYFVOE", "E"),
        "III": ("BDFHJLCPRTXVZNYEIWGAKMUSQO", "V"),
    }

    REFLECTOR_B = "YRUHQSLDPXNGOKMIEBFZCWVJAT"

    self.rotors = []

    for r_name, ring, pos in zip(
        rotors, ring_settings, initial_positions
    ):
      wiring, notch = ROTOR_WIRINGS[r_name]

      self.rotors.append(
          EnigmaRotor(
              wiring,
              notch,
              ring_setting=ring,
              position=pos
          )
      )

    self.reflector = REFLECTOR_B
    self.plugboard = {}

    for pair in plugboard_pairs:
      a, b = pair.split("-")
      self.plugboard[a] = b
      self.plugboard[b] = a

  def _step_rotors(self):
    r_left = self.rotors[0]
    r_middle = self.rotors[1]
    r_right = self.rotors[2]

    middle_at_notch = r_middle.is_at_notch()
    right_at_notch = r_right.is_at_notch()

    if middle_at_notch:
      r_left.step()
      r_middle.step()
      r_right.step()

    elif right_at_notch:
      r_middle.step()
      r_right.step()
    else:
      r_right.step()

  def decrypt_char(self, char):
    if not char.isalpha():return char
    self._step_rotors()
    char = self.plugboard.get(char, char)
    c_idx = ord(char) - 65

    for r in reversed(self.rotors):c_idx = r.forward(c_idx)
    ref_char = self.reflector[c_idx]
    c_idx = ord(ref_char) - 65

    for r in self.rotors:c_idx = r.backward(c_idx)
    out_char = chr(c_idx + 65)
    out_char = self.plugboard.get(out_char, out_char)
    return out_char

  def process_text(self, text):
    hasil = ""
    for c in text:hasil = hasil + self.decrypt_char(c)
    return hasil


rotors_order = ["I", "II", "III"]

ring_settings = [18, 1, 16]

initial_positions = ["S", "M", "P"]

plugboard = ["G-R", "U-E"]

ciphertext = "XTDQAMLVTBBDFXABSDKNAZZHLCESIOWIHVYZVAYHT"

enigma = EnigmaMachine(
    rotors=rotors_order,
    reflector="B",
    ring_settings=ring_settings,
    initial_positions=initial_positions,
    plugboard_pairs=plugboard,
)

plaintext = enigma.process_text(ciphertext)

print("Ciphertext :", ciphertext)
print("Plaintext  :", plaintext)