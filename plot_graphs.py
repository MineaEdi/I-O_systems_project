import serial
import time
import matplotlib.pyplot as plt
import numpy as np
import os

COM_PORT = "COM5"
BAUDRATE = 115200  # implicit pentru Pico
RECOGNIZE_FILE = "vowels/recognize.txt"
DATA_FOLDER = "vowels"
WINDOW_SIZE = 350
NUM_SAMPLES = 512

## dynamic time warping function ##
def dtw(s1, s2):
    n, m = len(s1), len(s2)
    dtw_matrix = np.full((n + 1, m + 1), np.inf)
    dtw_matrix[0, 0] = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = abs(s1[i - 1] - s2[j - 1])
            dtw_matrix[i, j] = cost + min(
                dtw_matrix[i - 1, j],
                dtw_matrix[i, j - 1],
                dtw_matrix[i - 1, j - 1]
            )
    return dtw_matrix[n, m]
## dynamic time warping function ##

## aditional functions ##
def load_signal(path):
    with open(path, "r") as f:
        return [float(l.strip()) for l in f if l.strip()]

def extract_window(signal, size=WINDOW_SIZE):
    mid = len(signal) // 2
    return signal[mid - size // 2 : mid + size // 2]

def save_graphic(signal, filename="signal_test.png"):
    x = list(range(len(signal)))
    y = signal

    plt.figure(figsize=(10, 4))
    plt.xlim(0, 512)
    plt.ylim(0, 4000)
    plt.plot(x, y)
    plt.xlabel("Index")
    plt.ylabel("Valoare ADC")
    plt.title("Semnal esantionat")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
## aditional functions ##


## waiting data from pico and save it to recognize.txt
print(f"[INFO] Open port {COM_PORT}...")

try:
    with serial.Serial(COM_PORT, BAUDRATE, timeout=1) as ser, open(RECOGNIZE_FILE, "w") as fout:
        print("[INFO] Waiting data from Pico...")
        while True:
            line = ser.readline().decode().strip()
            if line == "READY":
                print("[PICO] Ready. Push button to record.")
            elif line == "DONE":
                print("[PICO] Done transmitting.")
                break
            elif line:
                fout.write(line + "\n")
except Exception as e:
    print("[ERORR]:", e)
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("[INFO] COM port closed.")

## load signal for test
print("[INFO] Load signal for test...")
signal_test = load_signal(RECOGNIZE_FILE)
window_test = extract_window(signal_test)
save_graphic(signal_test)


## load all samples
labels = {}
print("[INFO] Load existing vowels samples...")
for vowels_file in os.listdir(DATA_FOLDER):
    if vowels_file.startswith("date_adc_") and vowels_file.endswith(".txt"):
        parts = vowels_file.split("_")
        if len(parts) >= 3:
            vowel_from_file = parts[2]  # A, E, I, O, U
            path_of_vowel_sample = os.path.join(DATA_FOLDER, vowels_file)
            signal_of_vowel_sample = load_signal(path_of_vowel_sample)
            window_of_vowel_sample = extract_window(signal_of_vowel_sample)
            labels.setdefault(vowel_from_file, []).append(window_of_vowel_sample)


## apply dtw and print recognized vowel
print("[INFO] Apply DTW for recognizing...")
scores = {}
for vowel, ferestre in labels.items():
    scor_min = min(dtw(window_test, et) for et in ferestre)
    scores[vowel] = scor_min

recognized_vowel = min(scores, key=scores.get)

## print result
print("\nRecognized vowel: ", recognized_vowel)
print("DTW scores:")
for voc, score in scores.items():
    print(f"  {voc}: {score:.2f}")
