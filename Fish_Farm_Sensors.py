import math


def ConvertPH(analog_val, calibration_val):
    pH_volts = analog_val*5/1024
    ph = -5.7*pH_volts + 21.34 + calibration_val
    
    return ph

def ConvertTemp(analog_val, calibration_val = 100000):
    R1 = calibration_val
    c1, c2, c3 = 1.009249522e-03, 2.378405444e-04, 2.019202697e-07
    R2 = R1 * (1023.0 / analog_val - 1.0)
    logR2 = math.log(R2)
    temperature = (1.0 / (c1 + c2 * logR2 + c3 * logR2 * logR2 * logR2))
    temperature = temperature - 273.15
    
    return temperature # degree celcius

def ConvertTDS(analog_val, temperature = 25, calibration = 0.05):
    analog_volts = analog_val*5/1024
    compensationCoefficient=1.0+0.02*(temperature-25.0)
    compensationVolatge = analog_volts/compensationCoefficient
    tds=(133.42*compensationVolatge**3 - 255.86*compensationVolatge**2 + 857.39*compensationVolatge)*calibration
    
    return tds # ppm or mg/L

def ConvertBattery(analog_val):
    min_volts = 3.0
    max_volts = 4.2
    
    analog_volts = analog_val*5/1024
    analog_percentage = (analog_volts - min_volts)*100/(max_volts - min_volts)
    
    return analog_percentage
    
print("pH:",ConvertPH(490, 0))
print("TDS", ConvertTDS(75, ConvertTemp(920), calibration=0.05))
# print("Battery:", ConvertBattery(102))
print("Temperature:", ConvertTemp(920, 100000))
