"""."""

import pandas as pd

drivers = pd.DataFrame(
    [
        ['Marconi Instruments', '2187', 'Attenuator', 'MI2187'],
        ['MI Wave', '511', 'Attenuator', 'MIWave5nn'],
        ['Hewlett Packard', '8903B', 'AudioAnalyser', 'HP8903B'],
        ['Hewlett Packard', '34401A', 'DigitalMultimeter', 'HP34401A'],
        ['Hewlett Packard', '3457A', 'DigitalMultimeter', 'HP3457A'],
        ['Thurlby Thandar', '1705', 'DigitalMultimeter', 'TTI1705'],
        ['Lumiloop', 'LSProbe', 'FieldStrength', 'LumiloopLSProbe'],
        ['Wandel Goltermann', 'EMC20', 'FieldStrength', 'WandelGoltermannEMC20'],
        ['Narda', '601', 'FieldStrength', 'Narda601'],
        ['Agilent Technologies', 'N9039A', 'FilterRF', 'AgilentN9039A'],
        ['Hewlett Packard', '53132A', 'FrequencyCounter', 'HP53132A'],
        ['Racal', '1992', 'FrequencyCounter', 'Racal1992'],
        ['Hewlett Packard', '8901B', 'ModulationMeter', 'HP8901B'],
        ['Marconi Instuments', '2305', 'ModulationMeter', 'MI2305'],
        ['Hewlett Packard', '4395A', 'NetworkAnalyser', 'HP4395A'],
        ['Agilent Technologies', 'E8357A', 'NetworkAnalyser', 'AgilentE8357A'],
        ['Anritsu', 'MS46122B', 'NetworkAnalyser', 'AnritsuShockline'],
        ['Wiltron', '360', 'NetworkAnalyser', 'Wiltron360'],
        ['Keysight Technologies', 'DSO-X 3034T', 'Oscilloscope', 'KeysightInfiniiVisionX'],
        ['Agilent Technologies', 'DSO5052A', 'Oscilloscope', 'KeysightInfiniiVisionX'],  # KeysightDSO50bpA
        ['Agilent Technologies', 'DSO5034A', 'Oscilloscope', 'KeysightInfiniiVisionX'],  # KeysightDSO50bpA
        ['Tektronix', 'TDS7104', 'Oscilloscope', 'TektronixTDS7104'],
        ['Rigol Technologies', 'DS1104Z', 'Oscilloscope', 'RigolDS1nnnZ'],
        ['Hewlett Packard', '437B', 'PowerMeter', 'HP437B'],
        ['Hewlett Packard', 'E4418B', 'PowerMeter', 'AgilentE4418B'],  # TBC
        ['Agilent Technologies', 'E4418B', 'PowerMeter', 'AgilentE4418B'],
        ['Rohde Schwarz', 'NRVS', 'PowerMeter', 'RohdeSchwarzNRVS'],
        ['VDI', 'PM5B', 'PowerMeter', 'VDIPM5B'],
        ['ELVA', 'DPM', 'PowerMeter', 'ELVA1DPM'],
        ['Hewlett Packard', '59501B', 'PowerSourceDC', 'HP59501B'],  # No IDN / ID capablity
        ['Agilent Technologies', 'N7972A', 'PowerSourceDC', 'AgilentN7972A'],
        ['TTI', 'PL330P', 'PowerSourceDC', 'TTIPL330P'],  # 'IDN?'?
        ['Marconi Instruments', '2030', 'SignalGenerator', 'MarconiInstruments203N'],
        ['Marconi Instruments', '2031', 'SignalGenerator', 'MarconiInstruments203N'],
        ['Marconi Instruments', '2032', 'SignalGenerator', 'MarconiInstruments203N'],
        ['Rohde Schwarz', 'SMH52', 'SignalGenerator', 'RohdeSchwarzSHM52'],  # 100 kHz to 2 GHz
        ['Hewlett Packard', '8657A', 'SignalGenerator', 'HP8657A'],  # 100 kHz to 1040 MHz
        ['Hewlett Packard', '8664A', 'SignalGenerator', 'HP866nX'],  # 100 kHz to 3 GHz
        ['Hewlett Packard', '8665B', 'SignalGenerator', 'HP866nX'],  # 100 kHz to 6 GHz
        ['Hewlett Packard', '85645A', 'SignalGenerator', 'HP85645A'],  # 300 kHz - 26.5 GHz SG/TG
        ['Hewlett Packard', '83752B', 'SignalGenerator', 'HP83752B'],  # 0.01 - 20 GHz
        # ['Hewlett Packard', '83650B', 'SignalGenerator', 'HP83650B'],  # 0.01 - 50 GHz
        ['Hewlett Packard', '83650B', 'SignalGenerator', 'Agilent83650B'],  # 0.01 - 50 GHz
        ['Hewlett Packard', 'ESG-3000A', 'SignalGenerator', 'SCPISignalGenerator'],
        ['Hewlett Packard', 'ESG-3000B', 'SignalGenerator', 'SCPISignalGenerator'],  # labeled HP, E4421B
        ['Hewlett Packard', 'ESG-4000B', 'SignalGenerator', 'SCPISignalGenerator'],  # labeled HP, E4422B
        ['Hewlett Packard', '8648C', 'SignalGenerator', 'SCPISignalGenerator'],  # labeled Agilent, 8648C
        ['Agilent Technologies', '8648C', 'SignalGenerator', 'SCPISignalGenerator'],  # not needed ? HP FW
        ['Hewlett Packard', 'E4421B', 'SignalGenerator', 'SCPISignalGenerator'],
        ['Agilent Technologies', 'E4422B', 'SignalGenerator', 'SCPISignalGenerator'],
        ['Agilent Technologies', 'E4438C', 'SignalGenerator', 'AgilentE4438C'],
        ['Agilent Technologies', 'E4433B', 'SignalGenerator', 'AgilentE4438C'],  ## TODO checks
        ['Keysight Technologies', 'N5173B', 'SignalGenerator', 'SCPISignalGenerator'],
        ['Agilent Technologies', 'N5181A', 'SignalGenerator', 'SCPISignalGenerator'],
        ['Agilent Technologies', 'N5182A', 'SignalGenerator', 'SCPISignalGenerator'],
        ['Anritsu', 'MG3710A', 'SignalGenerator', 'AnritsuMG3710A'],  # VSG as opt
        # MG369nA Series
        ['Anritsu', 'MG3691A', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3692A', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3693A', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3694A', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3695A', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3696A', 'SignalGenerator', 'AnritsuMG369nAB'],
        # MG369nB Series
        ['Anritsu', 'MG3691B', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3692B', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3693B', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3694B', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3695B', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MG3696B', 'SignalGenerator', 'AnritsuMG369nAB'],
        ['Anritsu', 'MS2668C', 'SpectrumAnalyser', 'AnritsuMS266nC'],
        # MG369nC Series
        # SCPI capable, may differ from A,B series
        ['Keysight Technologies', 'N9000B', 'SpectrumAnalyser', 'KeysightN90nnB'],  # CXA
        ['Keysight Technologies', 'N9010B', 'SpectrumAnalyser', 'KeysightN90nnB'],  # EXA
        ['Keysight Technologies', 'N9020B', 'SpectrumAnalyser', 'KeysightN90nnB'],  # MXA
        ['Keysight Technologies', 'N9021B', 'SpectrumAnalyser', 'KeysightN90nnB'],  # MXA
        ['Keysight Technologies', 'N9030B', 'SpectrumAnalyser', 'KeysightN90nnB'],  # PXA
        ['Keysight Technologies', 'N9040B', 'SpectrumAnalyser', 'KeysightN90nnB'],  # UXA
        ['Keysight Technologies', 'N9041B', 'SpectrumAnalyser', 'KeysightN90nnB'],  # UXA
        ['Keysight Technologies', 'N9042B', 'SpectrumAnalyser', 'KeysightN90nnB'],  # UXA
        ['Agilent Technologies', 'E4440A', 'SpectrumAnalyser', 'AgilentE44nn'],  # PSA 26.5 GHz
        ['Agilent Technologies', 'E4443A', 'SpectrumAnalyser', 'AgilentE44nn'],  # PSA GHz
        ['Hewlett Packard', 'E4406A', 'SpectrumAnalyser', 'AgilentE4406A'],  # VSA
        ['Rohde&Schwarz', 'ESW-8', 'SpectrumAnalyser', 'RaSESW'],
        ['Rohde&Schwarz', 'ESW-26', 'SpectrumAnalyser', 'RaSESW'],
        ['Rohde&Schwarz', 'ESW-44', 'SpectrumAnalyser', 'RaSESW'],
        ['Rohde&Schwarz', 'FSW-8', 'SpectrumAnalyser', 'RaSESW'],
        ['Rohde&Schwarz', 'FSW-13', 'SpectrumAnalyser', 'RaSESW'],
        ['Rohde&Schwarz', 'FSW-26', 'SpectrumAnalyser', 'RaSESW'],
        ['Rohde&Schwarz', 'FSW-43', 'SpectrumAnalyser', 'RaSESW'],
        ['Rohde&Schwarz', 'FSW-50', 'SpectrumAnalyser', 'RaSESW'],
        ['Rohde&Schwarz', 'FSW-67', 'SpectrumAnalyser', 'RaSESW'],
        ['Rohde&Schwarz', 'FSW-85', 'SpectrumAnalyser', 'RaSESW'],
        ['Rohde&Schwarz', 'FPL1003', 'SpectrumAnalyser', 'RaSESW'],
        ['Rohde&Schwarz', 'FPL1007', 'SpectrumAnalyser', 'RaSESW'],
        ['Rohde&Schwarz', 'FPL1014', 'SpectrumAnalyser', 'RaSESW'],
        ['Rohde&Schwarz', 'FPL1026', 'SpectrumAnalyser', 'RaSESW'],
        ['Rohde&Schwarz', 'ETL', 'SpectrumAnalyser', 'RaSESW'],
        ['Rohde&Schwarz', 'ETH', 'SpectrumAnalyser', 'RaSESW'],
        ['Rohde&Schwarz', 'FSV', 'SpectrumAnalyser', 'RaSESW'],
        ['Rohde&Schwarz', 'CMW', 'WirelessTestSet', 'RaSCMW500'],
        # 'HP8546A': HP8546A,
        # 'HP8563E': HP8563E,
        # 'HP8564E': HP8564E,
        # 'HP8594E': HP8594E,
        # 'HP8596E': HP8596E,
        # Benchview supported N9040B UXA, N9030A/B PXA, N9020A/B MXA,
        # N9010A/B EXA, N9000A/B CXA, M9290A CXA-m
        # Benchview supported N9320B, N9322C
        # Benchview supported N9342C, N9343C, N9344C
        # Benchview supported E4440A, E4443A, E4445A, E4446A, E4447A, E4448A
        # Benchview supported E4402B, E4404B, E4405B, E4407B
        # Benchview supported E4403B, E4411B, E4408B
        # Agilent Technologies ESA-E Series
        # E4401B (9 kHz- 1.5 GHz)
        # E4402B (9 kHz - 3.0 GHz)
        # E4404B (9 kHz - 6.7 GHz)
        # E4405B (9 kHz - 13.2 GHz)
        # E4407B (9 kHz - 26.5 GHz)
        ['Agilent Technologies', 'E4404B', 'SpectrumAnalyser', 'AgilentE44nn'],
        ['Hewlett Packard', 'E4401B', 'SpectrumAnalyser', 'AgilentE44nn'],
        ['Hewlett Packard', 'E4402B', 'SpectrumAnalyser', 'AgilentE44nn'],
        ['Hewlett Packard', 'E4404B', 'SpectrumAnalyser', 'AgilentE44nn'],
        # FW reports HP, branded Agilent
        ['Hewlett Packard', 'E4405B', 'SpectrumAnalyser', 'AgilentE44nn'],
        ['Hewlett Packard', 'E4407B', 'SpectrumAnalyser', 'AgilentE44nn'],
        # Agilent Technologies ESA-L Series
        # E4411B (9 kHz- 1.5 GHz)
        # E4403B (9 kHz - 3.0 GHz)
        # E4408B (9 kHz - 26.5 GHz)
        ['Hewlett Packard', 'E4411B', 'SpectrumAnalyser', 'AgilentE44nn'],
        ['Hewlett Packard', 'E4403B', 'SpectrumAnalyser', 'AgilentE44nn'],
        ['Hewlett Packard', 'E4408B', 'SpectrumAnalyser', 'AgilentE44nn'],
        ['Hewlett Packard', '8563A', 'SpectrumAnalyser', 'HPGreenScreen'],
        ['Hewlett Packard', '8563E', 'SpectrumAnalyser', 'HPGreenScreen'],
        ['Hewlett Packard', '8564E', 'SpectrumAnalyser', 'HPGreenScreen'],
        ['Hewlett Packard', '8593E', 'SpectrumAnalyser', 'HPGreenScreen'],
        ['Hewlett Packard', '8594E', 'SpectrumAnalyser', 'HPGreenScreen'],
        ['Advantest', 'R3172', 'SpectrumAnalyser', 'AdvantestR3172'],
        ['Hewlett Packard', '3488A', 'Switch', 'HP3488A'],
        ['Keithley Instruments', '7999-6', 'Switch', 'Keithley79996'],
        ['Hewlett Packard', '33120A', 'WaveformGenerator', 'HP33120A'],
        ['Hewlett Packard', '8116A', 'WaveformGenerator', 'HP8116A'],  # 'ID?'?
        ['Thurlby Thandar', 'PL330P', 'PowerSourceDC', 'TTIPL330P'],
        # ['', '', '', '']
    ],
    columns=['Manufacturer', 'Model', 'Type', 'Driver'],
)
