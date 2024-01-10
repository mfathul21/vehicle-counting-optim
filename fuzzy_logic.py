import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


def optim_traffic(input_mobil, input_motor):
    # Variabel input
    jumlah_motor = ctrl.Antecedent(np.arange(0, 31, 1), 'jumlah_motor')
    jumlah_mobil = ctrl.Antecedent(np.arange(0, 11, 1), 'jumlah_mobil')

    # Variabel output
    duration = ctrl.Consequent(np.arange(0, 61, 1), 'duration')

    # Fungsi keanggotaan untuk variabel input dan output
    jumlah_motor['low'] = fuzz.trimf(jumlah_motor.universe, [0, 0, 15])
    jumlah_motor['medium'] = fuzz.trimf(jumlah_motor.universe, [0, 15, 30])
    jumlah_motor['high'] = fuzz.trimf(jumlah_motor.universe, [15, 30, 30])

    jumlah_mobil['low'] = fuzz.trimf(jumlah_mobil.universe, [0, 0, 5])
    jumlah_mobil['medium'] = fuzz.trimf(jumlah_mobil.universe, [0, 5, 10])
    jumlah_mobil['high'] = fuzz.trimf(jumlah_mobil.universe, [5, 10, 10])

    duration['short'] = fuzz.trimf(duration.universe, [0, 0, 20])
    duration['medium'] = fuzz.trapmf(duration.universe, [10, 20, 40, 50])
    duration['long'] = fuzz.trimf(duration.universe, [40, 60, 60])

    # Rule base
    rule1 = ctrl.Rule(jumlah_motor['low'], duration['short'])
    rule2 = ctrl.Rule(jumlah_motor['medium'], duration['medium'])
    rule3 = ctrl.Rule(jumlah_motor['high'], duration['long'])
    rule4 = ctrl.Rule(jumlah_mobil['low'], duration['short'])
    rule5 = ctrl.Rule(jumlah_mobil['medium'], duration['medium'])
    rule6 = ctrl.Rule(jumlah_mobil['high'], duration['long'])
    rule7 = ctrl.Rule(jumlah_motor['low'] & jumlah_mobil['low'], duration['short'])
    rule8 = ctrl.Rule(jumlah_motor['low'] & jumlah_mobil['medium'], duration['medium'])
    rule9 = ctrl.Rule(jumlah_motor['low'] & jumlah_mobil['high'], duration['long'])
    rule10 = ctrl.Rule(jumlah_motor['medium'] & jumlah_mobil['low'], duration['medium'])
    rule11 = ctrl.Rule(jumlah_motor['medium'] & jumlah_mobil['medium'], duration['medium'])
    rule12 = ctrl.Rule(jumlah_motor['medium'] & jumlah_mobil['high'], duration['long'])
    rule13 = ctrl.Rule(jumlah_motor['high'] & jumlah_mobil['low'], duration['long'])
    rule14 = ctrl.Rule(jumlah_motor['high'] & jumlah_mobil['medium'], duration['long'])
    rule15 = ctrl.Rule(jumlah_motor['high'] & jumlah_mobil['high'], duration['long'])

    # Rule evaluation
    traffic_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10,
                                       rule11, rule12, rule13, rule14, rule15])
    traffic_duration = ctrl.ControlSystemSimulation(traffic_ctrl)

    # Input values
    traffic_duration.input['jumlah_mobil'] = input_mobil
    traffic_duration.input['jumlah_motor'] = input_motor

    # Perhitungan nilai output
    traffic_duration.compute()

    # Output
    output = traffic_duration.output['duration']
    return np.round(output, 2)