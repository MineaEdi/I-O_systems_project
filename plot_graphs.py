import serial
import time
import matplotlib.pyplot as plt

PORT = "COM6"
BAUDRATE = 115200  # implicit pentru Pico

output_file = "vowels\\date_adc_U_1.txt"

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
            if "," in line:
                #f.write(line + "\n")
                print(line)

x = []
y = []

with open(output_file, "r") as f:
    for line in f:
        parts = line.strip().split(",")
        if len(parts) == 2:
            x.append(int(parts[0]))
            y.append(float(parts[1]))

# Plot
plt.xlim(0, 3000)
plt.ylim(0, 4000)
plt.plot(x, y)
plt.xlabel("Index")
plt.ylabel("Valoare ADC")
plt.title("Semnal esantionat")
plt.grid(True)
plt.show()
