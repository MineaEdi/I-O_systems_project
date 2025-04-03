from machine import Pin, PWM, ADC
import time

# --- CONFIGURARE PINI ---
pwm = PWM(Pin(16))         # Semnal dreptunghiular PWM
pwm.freq(1000)             # 1kHz
pwm.duty_u16(32768)        # 50% duty cycle

adc = ADC(Pin(26))         # ADC0 pe GP26
buton = Pin(14, Pin.IN, Pin.PULL_UP)  # Buton pe GP14

# Parametri esantionare
num_samples = 512
delay = 40  # 40us => 25kHz

while 1:
    print("READY")

    while buton.value():
        time.sleep(0.01)

    print("Buton apasat! Astept 500ms...")
    time.sleep(0.5)

    values = []
    
    for i in range(num_samples):
        val = adc.read_u16()
        voltaj = val * 3.3 / 65535 * 1000
        values.append(voltaj)
        time.sleep_us(delay)

    for i, val in enumerate(values):
        print(f"{i},{val}") # trimitere pe seriala

    print("DONE")
    