from machine import Pin, PWM, ADC
import time

# --- CONFIGURARE PINI ---
pwm = PWM(Pin(16))         # Semnal dreptunghiular PWM
pwm.freq(1000)             # 1kHz
pwm.duty_u16(32768)        # 50% duty cycle

adc = ADC(Pin(26))         # ADC0 pe GP26
buton = Pin(14, Pin.IN, Pin.PULL_UP)  # Buton pe GP14

# Parametri esantionare
num_samples = 3000
delay = 0.001  # 1ms => 1kHz

print("Astept apasarea butonului...")

while buton.value():
    time.sleep(0.01)

print("Buton apasat! Astept 50ms...")
time.sleep(0.05)

# Esantionare
print("Incep esantionarea...")
samples = []
for i in range(num_samples):
    valoare = adc.read_u16()
    samples.append(valoare)
    time.sleep(delay)

print("Esantionare completa. Salvez in fisier...")

# Salvare în fișier .txt
with open("date_adc.txt", "w") as f:
    for i, val in enumerate(samples):
        f.write(f"{i},{val}\n")
        print(f"{i}. valoare adc: {val}")

# Preview
# print("Primele 10 valori:")
# print(samples[:10])
