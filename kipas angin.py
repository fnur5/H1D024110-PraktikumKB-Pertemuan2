import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Variabel input
suhu = ctrl.Antecedent(np.arange(0, 41, 1), 'suhu')
kelembapan = ctrl.Antecedent(np.arange(0, 101, 1), 'kelembapan')

# Variabel output
kecepatan = ctrl.Consequent(np.arange(0, 101, 1), 'kecepatan')

# Himpunan suhu
suhu['dingin'] = fuzz.trimf(suhu.universe, [0, 0, 20])
suhu['normal'] = fuzz.trimf(suhu.universe, [15, 25, 35])
suhu['panas'] = fuzz.trimf(suhu.universe, [30, 40, 40])

# Himpunan kelembapan
kelembapan['kering'] = fuzz.trimf(kelembapan.universe, [0, 0, 50])
kelembapan['sedang'] = fuzz.trimf(kelembapan.universe, [30, 50, 70])
kelembapan['lembap'] = fuzz.trimf(kelembapan.universe, [60, 100, 100])

# Himpunan kecepatan kipas
kecepatan['lambat'] = fuzz.trimf(kecepatan.universe, [0, 0, 40])
kecepatan['sedang'] = fuzz.trimf(kecepatan.universe, [30, 50, 70])
kecepatan['cepat'] = fuzz.trimf(kecepatan.universe, [60, 100, 100])

# Aturan
rule1 = ctrl.Rule(suhu['dingin'] & kelembapan['kering'], kecepatan['lambat'])
rule2 = ctrl.Rule(suhu['normal'] & kelembapan['sedang'], kecepatan['sedang'])
rule3 = ctrl.Rule(suhu['panas'] | kelembapan['lembap'], kecepatan['cepat'])
rule4 = ctrl.Rule(suhu['panas'] & kelembapan['kering'], kecepatan['cepat'])
rule5 = ctrl.Rule(suhu['dingin'] & kelembapan['lembap'], kecepatan['sedang'])

# Sistem kontrol
fan_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5])
fan_sim = ctrl.ControlSystemSimulation(fan_ctrl)

def hitung_kecepatan(nilai_suhu, nilai_kelembapan):
    fan_sim.input['suhu'] = nilai_suhu
    fan_sim.input['kelembapan'] = nilai_kelembapan
    fan_sim.compute()
    return fan_sim.output['kecepatan']

# Pengujian
contoh = [(31, 45), (21, 70), (27, 55)]
hasil = []

for s, k in contoh:
    hasil.append({
        'suhu': s,
        'kelembapan': k,
        'kecepatan_fan': round(hitung_kecepatan(s, k), 2)
    })

for row in hasil:
    print(row)
