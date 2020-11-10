from time import sleep

from tqdm import tqdm

from helper.frequency import FrequencyGroup
from helper.modulation import Modulation


def ModulationAM(testspec, generator, modulationmeter, spectrumanalyser=None):
    try:
        if spectrumanalyser:
            spectrumanalyser.resbw = 3e6
            spectrumanalyser.span = 0
            freqgrp = FrequencyGroup([generator, spectrumanalyser])
        else:
            freqgrp = FrequencyGroup([generator])

        measurand = modulationmeter.MeasureAM()
        generator.output = True

        for index, row in tqdm(testspec.iterrows(), total=len(testspec)):

            frequency = row['Frequency (Hz)']
            freqgrp.frequency = frequency
            if spectrumanalyser:
                spectrumanalyser.reflevel = row['Amplitude (dBm)'] + 5.1 + 2
            generator.amplitude = row['Amplitude (dBm)']
            generator.modulation = Modulation('AM', rate=row['Modulation Frequency (Hz)'], depth=row['Modulation Depth (%)'], dontpresetmodulation=False)
            sleep(3)

            depth = next(measurand)
            # print(f'AM: {depth} % @ {frequency/1e6:^6} MHz')
            testspec.loc[index, 'Result (%)'] = depth

    finally:
        measurand.send(False)
        generator.output = False

    return testspec
# testspec.to_clipboard(index=False)
