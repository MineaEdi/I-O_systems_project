import serial
import time
import matplotlib.pyplot as plt

PORT = "COM5"
BAUDRATE = 115200  # implicit pentru Pico

output_file = "vowels\\recognize.txt"

with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:#, open(output_file, "w") as f:
    print(f"Astept date de la Pico pe portul {PORT}...")

    start = False
    while True:
        line = ser.readline().decode().strip()

        if line == "READY":
            print("Pico e gata. Apasa butonul.")
        elif line == "DONE":
            print("Transmisie terminata!")
            break
        elif line:
            #f.write(line + "\n")
            print(line)

x = []
y = []
cnt = 0

with open(output_file, "r") as f:
    for line in f:
        value = line.strip()
        x.append(int(cnt))
        y.append(float(value))
        cnt += 1

# Plot
plt.xlim(0, 512)
plt.ylim(0, 4000)
plt.plot(x, y)
plt.xlabel("Index")
plt.ylabel("Valoare ADC")
plt.title("Semnal esantionat")
plt.grid(True)
plt.show()
