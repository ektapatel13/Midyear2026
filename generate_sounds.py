"""Generate placeholder sound effect .wav files for the Kitchen Game."""
import wave
import struct
import math
import os

SAMPLE_RATE = 44100
DIR = os.path.dirname(os.path.abspath(__file__))


def generate_tone(filename, duration_sec, freq, volume=0.5, wave_type="sine"):
    """Generate a simple tone wav file."""
    n_samples = int(SAMPLE_RATE * duration_sec)
    filepath = os.path.join(DIR, filename)
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        for i in range(n_samples):
            t = i / float(SAMPLE_RATE)
            if wave_type == "sine":
                val = math.sin(2 * math.pi * freq * t)
            elif wave_type == "square":
                val = 1.0 if math.sin(2 * math.pi * freq * t) >= 0 else -1.0
            elif wave_type == "sawtooth":
                val = 2.0 * (t * freq - math.floor(t * freq + 0.5))
            else:
                val = math.sin(2 * math.pi * freq * t)
            # Apply fade in/out to avoid clicks
            fade_samples = int(SAMPLE_RATE * 0.01)
            if i < fade_samples:
                val *= i / float(fade_samples)
            elif i > n_samples - fade_samples:
                val *= (n_samples - i) / float(fade_samples)
            sample = int(val * volume * 32767)
            sample = max(-32768, min(32767, sample))
            wf.writeframes(struct.pack('<h', sample))
    print("Created: " + filename)


def generate_toaster_sound():
    """Warm humming/buzzing sound for toaster."""
    n_samples = int(SAMPLE_RATE * 2.0)
    filepath = os.path.join(DIR, "toaster_sound.wav")
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        for i in range(n_samples):
            t = i / float(SAMPLE_RATE)
            # Low hum with slight wobble
            val = 0.4 * math.sin(2 * math.pi * 120 * t)
            val += 0.2 * math.sin(2 * math.pi * 240 * t)
            val += 0.1 * math.sin(2 * math.pi * 60 * t * (1 + 0.1 * math.sin(2 * math.pi * 2 * t)))
            fade = min(1.0, i / (SAMPLE_RATE * 0.05), (n_samples - i) / (SAMPLE_RATE * 0.05))
            sample = int(val * fade * 0.3 * 32767)
            sample = max(-32768, min(32767, sample))
            wf.writeframes(struct.pack('<h', sample))
    print("Created: toaster_sound.wav")


def generate_oven_sound():
    """Deep rumble for oven."""
    n_samples = int(SAMPLE_RATE * 2.0)
    filepath = os.path.join(DIR, "oven_sound.wav")
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        for i in range(n_samples):
            t = i / float(SAMPLE_RATE)
            val = 0.5 * math.sin(2 * math.pi * 80 * t)
            val += 0.3 * math.sin(2 * math.pi * 160 * t)
            val += 0.15 * math.sin(2 * math.pi * 40 * t)
            # Add slight crackle
            val += 0.05 * math.sin(2 * math.pi * 800 * t * (1 + 0.5 * math.sin(2 * math.pi * 3 * t)))
            fade = min(1.0, i / (SAMPLE_RATE * 0.05), (n_samples - i) / (SAMPLE_RATE * 0.05))
            sample = int(val * fade * 0.25 * 32767)
            sample = max(-32768, min(32767, sample))
            wf.writeframes(struct.pack('<h', sample))
    print("Created: oven_sound.wav")


def generate_pan_sound():
    """Sizzling sound for pan."""
    import random as rnd
    rnd.seed(42)
    n_samples = int(SAMPLE_RATE * 2.0)
    filepath = os.path.join(DIR, "pan_sound.wav")
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        for i in range(n_samples):
            t = i / float(SAMPLE_RATE)
            # White noise filtered to sound like sizzle
            noise = rnd.random() * 2 - 1
            # Mix with some high-frequency tones
            val = 0.6 * noise
            val += 0.2 * math.sin(2 * math.pi * 3000 * t * (1 + 0.3 * math.sin(2 * math.pi * 5 * t)))
            val += 0.1 * math.sin(2 * math.pi * 5000 * t)
            fade = min(1.0, i / (SAMPLE_RATE * 0.05), (n_samples - i) / (SAMPLE_RATE * 0.05))
            sample = int(val * fade * 0.15 * 32767)
            sample = max(-32768, min(32767, sample))
            wf.writeframes(struct.pack('<h', sample))
    print("Created: pan_sound.wav")


def generate_kaching_sound():
    """Cash register cha-ching sound."""
    n_samples = int(SAMPLE_RATE * 0.8)
    filepath = os.path.join(DIR, "kaching_sound.wav")
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        for i in range(n_samples):
            t = i / float(SAMPLE_RATE)
            # Bright metallic ring
            val = 0.4 * math.sin(2 * math.pi * 2000 * t) * math.exp(-t * 5)
            val += 0.3 * math.sin(2 * math.pi * 3000 * t) * math.exp(-t * 6)
            val += 0.2 * math.sin(2 * math.pi * 4500 * t) * math.exp(-t * 8)
            # Second hit delayed
            t2 = max(0, t - 0.15)
            if t2 > 0:
                val += 0.5 * math.sin(2 * math.pi * 2500 * t2) * math.exp(-t2 * 4)
                val += 0.3 * math.sin(2 * math.pi * 3500 * t2) * math.exp(-t2 * 5)
            fade = min(1.0, i / (SAMPLE_RATE * 0.005), (n_samples - i) / (SAMPLE_RATE * 0.02))
            sample = int(val * fade * 0.5 * 32767)
            sample = max(-32768, min(32767, sample))
            wf.writeframes(struct.pack('<h', sample))
    print("Created: kaching_sound.wav")


def generate_alarm_sound():
    """Alarm clock beeping sound."""
    n_samples = int(SAMPLE_RATE * 1.5)
    filepath = os.path.join(DIR, "alarm_sound.wav")
    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        for i in range(n_samples):
            t = i / float(SAMPLE_RATE)
            # Beep pattern: on 0.15s, off 0.1s
            cycle = t % 0.25
            if cycle < 0.15:
                val = 0.6 * math.sin(2 * math.pi * 880 * t)
                val += 0.3 * math.sin(2 * math.pi * 1760 * t)
            else:
                val = 0.0
            fade = min(1.0, i / (SAMPLE_RATE * 0.01), (n_samples - i) / (SAMPLE_RATE * 0.05))
            sample = int(val * fade * 0.4 * 32767)
            sample = max(-32768, min(32767, sample))
            wf.writeframes(struct.pack('<h', sample))
    print("Created: alarm_sound.wav")


def generate_background_music():
    """Simple looping background melody."""
    n_samples = int(SAMPLE_RATE * 8.0)
    filepath = os.path.join(DIR, "background_music.wav")
    # Simple C major melody notes (frequencies)
    notes = [262, 294, 330, 349, 392, 440, 494, 523]  # C4 to C5
    melody = [0, 2, 4, 5, 4, 2, 0, 2, 4, 7, 5, 4, 2, 0, 4, 5]
    note_dur = 0.5  # seconds per note

    with wave.open(filepath, 'w') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        for i in range(n_samples):
            t = i / float(SAMPLE_RATE)
            note_idx = int(t / note_dur) % len(melody)
            freq = notes[melody[note_idx]]
            # Soft sine with harmonics
            val = 0.5 * math.sin(2 * math.pi * freq * t)
            val += 0.2 * math.sin(2 * math.pi * freq * 2 * t)
            val += 0.1 * math.sin(2 * math.pi * freq * 3 * t)
            # Note envelope
            note_t = (t % note_dur) / note_dur
            envelope = min(1.0, note_t * 10) * max(0.0, 1.0 - (note_t - 0.7) * 3.33) if note_t > 0.7 else min(1.0, note_t * 10)
            val *= envelope
            # Overall fade
            fade = min(1.0, i / (SAMPLE_RATE * 0.1), (n_samples - i) / (SAMPLE_RATE * 0.1))
            sample = int(val * fade * 0.2 * 32767)
            sample = max(-32768, min(32767, sample))
            wf.writeframes(struct.pack('<h', sample))
    print("Created: background_music.wav")


if __name__ == "__main__":
    print("Generating sound files...")
    generate_toaster_sound()
    generate_oven_sound()
    generate_pan_sound()
    generate_kaching_sound()
    generate_alarm_sound()
    generate_background_music()
    print("Done! All sound files created.")
