from time import sleep

from tqdm import tqdm

from helper.frequency import FrequencyGroup
from helper.modulation import Modulation


def ModulationFM(testspec, generator, modulationmeter, spectrumanalyser=None):
    
    try:
        if spectrumanalyser:
            spectrumanalyser.resbw = 3e6
            spectrumanalyser.span = 0
            freqgrp = FrequencyGroup([generator, spectrumanalyser])
        else:
            freqgrp = FrequencyGroup([generator])

        measurand = modulationmeter.MeasureFM()
        generator.output = True

        for index, row in tqdm(testspec.iterrows(), total=len(testspec)):
            freqgrp.frequency = row['Frequency (Hz)']
            if spectrumanalyser:
                spectrumanalyser.reflevel = row['Amplitude (dBm)'] + 2
            generator.amplitude = row['Amplitude (dBm)']
            generator.modulation = Modulation('FM', rate=row['Modulation Frequency (Hz)'], deviation=row['Frequency Deviation (Hz)'], dontpresetmodulation=True)

            sleep(3)

            deviation = next(measurand)
            testspec.loc[index, 'Result Deviation (Hz)'] = deviation

    finally:
        measurand.send(False)
        generator.output = False

    return testspec
# testspec.to_clipboard(index=False)
