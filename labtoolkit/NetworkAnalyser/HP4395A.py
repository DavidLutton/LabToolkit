from ..IEEE488 import IEEE488
# from ..SCPI import SCPI

import numpy as np
import pandas as pd


class HP4395A(IEEE488):
    """HP 4395A.

    Programming Manual: HP 04395-90031, fifth edition

    .. figure::  images/NetworkAnalyser/HP4395A.jpg
    """

    @property
    def trace(self):
        self.inst.write('FORM4')
        x, y = self.inst.query_ascii_values('OUTPSWPRM?', container=np.float64), self.inst.query_ascii_values('OUTPDATA?', container=np.float64).view(np.complex128)
        # return x, y
        db = 20 * np.log10(np.abs(y))
        df = pd.DataFrame(
            np.column_stack((x, db, y.real, y.imag)), 
            columns=['Frequency (Hz)', 'dB', 'Real', 'Imag']
        )
        return df.set_index('Frequency (Hz)')

    @property
    def points(self):
        """Sweep Points, max 801."""
        return int(self.query("POIN?"))

    @points.setter
    def points(self, points=801):
        self.write(f"POIN {int(points)}")

    @property
    def bandwidth(self):
        """IF Bandwidth.

        2, 10, 30, 100, 300, 1000 (=1k), 3000 (=3k), 10000 (=10k), 30000 (=30k)
        """
        return float(self.query("BW?"))

    @bandwidth.setter
    def bandwidth(self, frequency=1000):
        self.write(f"BW {int(frequency)}HZ")

    @property
    def form(self):
        """Format.

        LOGM, PHAS, DELA, LINM, SWR, REAL, IMAG, SMITH, POLA, EXPP, ADMIT, SPECT, NOISE, LINY
        """
        return self.query("FMT?")

    @form.setter
    def form(self, form='LOGM'):
        self.write(f"FMT {form}")

    @property
    def sweepformat(self):
        """Format.

        LOGF, LINF, LIST, POWE
        Log frequency (Network and impedance analyzers only)
        """
        return self.query("SWPT?")

    @sweepformat.setter
    def sweepformat(self, form='LOGF'):
        self.write(f"SWPT {form}")

    @property
    def paramater(self):
        """Measure paramater.

        AR, RB, R, A, B, S11, S12, S21, S22, IMAG, IPH, IRE, IIM, AMAG, APH, ARE, AIM, RCM, RCPH, RCM, RCPH, RCR, RCIM, CP, CS, LP, LS, D, Q, RP, RS
        """
        return self.query("MEAS?")

    @paramater.setter
    def paramater(self, paramater='S11'):
        self.write(f"MEAS {paramater}")

    @property
    def attenuationr(self):
        """Port attenuation R dB.

        0, 10, 20, 30, 40, 50
        """
        return float(self.query("ATTR?"))

    @attenuationr.setter
    def attenuationr(self, attenuation=20):
        self.write(f"ATTR {int(attenuation)}DB")

    @property
    def attenuationa(self):
        """Port attenuation A dB.

        0, 10, 20, 30, 40, 50
        """
        return float(self.query("ATTA?"))

    @attenuationa.setter
    def attenuationa(self, attenuation=20):
        self.write(f"ATTA {int(attenuation)}DB")

    @property
    def attenuationb(self):
        """Port attenuation B dB.

        0, 10, 20, 30, 40, 50
        """
        return float(self.query("ATTB?"))

    @attenuationb.setter
    def attenuationb(self, attenuation=20):
        self.write(f"ATTB {int(attenuation)}DB")

    @property
    def sourcepower(self):
        """Source power dBm."""
        return float(self.query("POWE?"))

    @sourcepower.setter
    def sourcepower(self, power=0):
        self.write(f"POWE {int(power)}")

    @property
    def start(self):
        """Start frequency."""
        return float(self.query("STAR?"))

    @start.setter
    def start(self, frequency):
        self.write(f"STAR {frequency}")

    @property
    def stop(self):
        """Stop frequency."""
        return float(self.query("STOP?"))

    @stop.setter
    def stop(self, frequency):
        self.write(f"STOP {frequency}")

'''

53 54 41 52 3F                                  STAR?
53 54 4F 50 3F                                  STOP?
4E 41 3F                                        NA?

31 0A                                           1.

4D 45 41 53 3F                                  MEAS?

46 4F 52 4D 34 3B                               FORM4;

4F 55 54 50 44 54 52 43 3F                      OUTPDTRC?
'''
'''
import visa
import time
import pprint

pp = pprint.PrettyPrinter(indent=4)
rm = visa.ResourceManager()
# print(rm.list_resources())

common = "TRGS INT;CONT;POIN 801;BW 1000;"
impedence = common + "CHAN1;FMT SMITH;MEAS S11;"
insertionloss = common + "CHAN1;FMT LOGM;MEAS B;"

lists = [
    ["Impedence 9kHz - 150kHz", impedence + "STAR 0.009E+6;STOP 0.150E+6;"],
    ["Impedence 9kHz - 1MHz", impedence + "STAR 0.009E+6;STOP 1E+6;"],
    ["Impedence 150kHz - 1MHz", impedence + "STAR 0.150E+6;STOP 1E+6;"],
    ["Impedence 1MHz - 30MHz", impedence + "STAR 1E+6;STOP 30E+6;"],
    ["Insertion loss 9kHz - 150kHz", insertionloss + "STAR 0.009E+6;STOP 0.150E+6;"],
    ["Insertion loss 150kHz - 1MHz", insertionloss + "STAR 0.150E+6;STOP 1E+6;"],
    ["Insertion loss 1MHz - 30MHz", insertionloss + "STAR 1E+6;STOP 30E+6;"],
    ["Insertion loss 9kHz - 30MHz LOG", insertionloss + "STAR 0.009E+6;STOP 30E+6;SWPT LOGF;"],

    ["Impedence 150kHz - 80MHz for CDNs", impedence + "STAR 0.150E+6;STOP 80E+6;"],
    ["Insertion loss 150kHz - 30MHz for CDNs", insertionloss + "STAR 0.150E+6;STOP 30E+6;"],
    ["Insertion loss 100kHz - 500MHz, -20 dBm source", insertionloss + "STAR 100E+3;STOP 500E+6;POWE -20;"],
]
# pp.pprint(lists)

if __name__ == "__main__":
    for i, v in enumerate(lists):
        print(str(i) + " :  " + lists[i][0])  # Show index and name

    try:
        setup = int(input("Select setup :  "))
        if setup <= len(lists):
            print(lists[setup][1])
            inst = rm.open_resource('GPIB0::17::INSTR')
            IDN = inst.query('*IDN?')
            print(IDN.strip())
            if IDN == "HEWLETT-PACKARD,4395A,JP1KE01895,REV1.12\n":
                inst.write('*RST')
                time.sleep(1)
                inst.write(lists[setup][1])  # Send setup command to instrument
            print("Done")

    except ValueError:
        print("NaN")
'''
    

'''
HEWLETT-PACKARD,4395A,JP1KE01895,REV1.12
inst.query('STAR?')
inst.query('STOP?')
inst.query('NA?')
inst.query('SA?')
inst.query('ZA?')
float(inst.query('SWET?'))
inst.query('BW?')
inst.query('MEAS?')
inst.query('FMT?')
inst.query('POWE?')

container = vna.complexto(y)
print(container.keys())


data = np.column_stack((x, y.real, y.imag))
print(data)

np.savetxt('testLPE374.s1p', data, fmt='%i %9.8f %9.8f', header='! '+'\n! '.join(['Created by Python, David', 'Trace details', 'Frequency S-Parameter(RI)'])+'\n# HZ S RI R 50', comments='')




#p = figure()
p = figure(title='bar', x_axis_label='Frequency (MHz)', y_axis_label='Impedance (Ω)', width=1224)  #, sizing_mode='scale_width')  # width=1800, height=900)
# , x_axis_type="log"
# p.x_range = Range1d(150e3, 30e6)
# p.y_range = Range1d(130, 170)


p.line(x, container['impedance'], legend='Impedance', color='black', alpha=1, line_width=2)
p.legend.location = "top_right"
p.legend.click_policy="hide"
p.legend.background_fill_color = "black"
p.legend.background_fill_alpha = 0.25

p.ygrid.minor_grid_line_color = 'black'
p.ygrid.minor_grid_line_alpha = 0.1

p.xgrid.minor_grid_line_color = 'black'
p.xgrid.minor_grid_line_alpha = 0.1
# p.background_fill_color = "gray"

# p.background_fill_alpha = 0.2
p.extra_y_ranges = {"Phase": Range1d(start=-180, end=180)}  # , "Temp": Range1d(start=-40, end=40)}
p.add_layout(LinearAxis(y_range_name="Phase", axis_label="Phase (°)", axis_line_color='Blue', major_tick_line_color='Blue', minor_tick_line_color='Blue', axis_line_width=2), 'left')

p.line(x, container['phase'], legend='Phase', color='blue', alpha=1, line_width=2, y_range_name="Phase")
# 

show(p)









#p = figure()
p = figure(title='bar', x_axis_label='Frequency (MHz)', x_axis_type="log", y_axis_label='Attenuation (dB)', width=1700)  #, sizing_mode='scale_width')  # width=1800, height=900)
# , x_axis_type="log"
p.x_range = Range1d(0.009e6, 200e6)
p.y_range = Range1d(-11, -9)


p.line(x, container['dB'], legend='Atten', color='black', alpha=1, line_width=2)
p.legend.location = "top_right"
p.legend.click_policy="hide"
p.legend.background_fill_color = "black"
p.legend.background_fill_alpha = 0.25

p.ygrid.minor_grid_line_color = 'black'
p.ygrid.minor_grid_line_alpha = 0.3
p.ygrid.grid_line_color = 'black'
p.ygrid.grid_line_alpha = 0.3

p.xgrid.minor_grid_line_color = 'black'
p.xgrid.minor_grid_line_alpha = 0.5
p.xgrid.grid_line_color = 'black'
p.xgrid.grid_line_alpha = 0.5
# p.background_fill_color = "gray"

# p.background_fill_alpha = 0.2
# p.extra_y_ranges = {"Phase": Range1d(start=-180, end=180)}  # , "Temp": Range1d(start=-40, end=40)}
# p.add_layout(LinearAxis(y_range_name="Phase", axis_label="Phase (°)", axis_line_color='Blue', major_tick_line_color='Blue', minor_tick_line_color='Blue', axis_line_width=2), 'left')

# p.line(x, container['phase'], legend='Phase', color='blue', alpha=1, line_width=2, y_range_name="Phase")
# 

show(p)

'''
'''
if IDN.startswith("HEWLETT-PACKARD,4395A,JP1KE01895,REV1.12"):
    print(IDN)
    inst.write('*RST')
    time.sleep(1)
    # inst.write("CHAN1;FMT LOGM;MEAS S11;TRGS INT;CONT;POIN 801")
    inst.write("CHAN1;FMT SMITH;MEAS S11;TRGS INT;CONT;POIN 801")
    inst.write("STAR 0.150E+6;" + "STOP 80.E+6;")
    time.sleep(2)

    #input("wait for CAL")
    #inst.write("MSI \":MEMORY\"")
    #inst.write("SAVDASC test")'''
'''    inst.write("STODMEMO")
    inst.write("CLES")
    inst.write("ROPEN \";555.sta;\"")
    inst.write("READ?")
    inst.write("READ?")
    inst.write("READ?")
    print(inst.read_raw())
'''
'''    
    inst.write("FORM3")
    inst.write("OUTPCALC1?")
    data = inst.read_raw()
    print(len(data))
    with open('before.data', mode='wb') as a_file: # , encoding='utf-8'
        a_file.write(data)
    
    
    with open('after.data', mode='rb') as a_file: # , encoding='utf-8'
        data = a_file.read()
    print(len(data))

    inst.write("CALI S111;REFL;CLASS11A")
    inst.write_raw(b"INPUCALC1 " + data )
    inst.write("SAV1")
    time.sleep(1)
    inst.write("SAVC")
    inst.write("CORR ON")
'''

'''
?F??O??R?M??A??T??:?L??O??G???M??A??G?? FMT LOGM
?P??H??A?S??E?? FMT PHAS
?D??E??L?A??Y?? FMT DELA
?S??M??I?T??H???C??H??A??R??T?? 
?P??O??L?A??R???C??H??A??R??T?? FMT POLA
?M??O??R?E??
?F??O?R??M??A??T?:??L??I??N???M??A??G?? FMT LINM
?S??W?R??? FMT SWR
?R??E?A??L?? FMT REAL
?I??M?A??G??I??N?A??R??Y?? FMT IMAG
?A??D?M??I??T??T?A??N??C??E???C??H??A?R??T?? FMT ADMIT
?R??E?T??U??R??N??
?P??H?A??S??E???U??N??I??T???[??D??E?G??]?? PHAU fDEGjRADg
?E??X?P????P??H?A??S??E???O??N????o?f??f?? EXPP fONjOFFg
?P??H??A?S??E???U??N??I??T???[??D??E??G?]?? PHAU fDEGjRADg
?E??X??P???P??H??A?S??E???O??N????o??f?f?? EXPP fONjOFFg

'''

'''
!Fig.2-2 Basic Measurement
30 !
40 ASSIGN @Hp4395 TO 717 ! When iBASIC is used, change "717" to "800".
50 !
60 OUTPUT @Hp4395;"PRES" ! Preset 4395A
70 OUTPUT @Hp4395;"CHAN1;NA;MEAS S21;FMT LOGM"
80 INPUT "Enter center frequency (Hz).",F_cent
90 INPUT "Enter frequency span (Hz).",F_span
100 OUTPUT @Hp4395;"CENT ";F_cent
110 OUTPUT @Hp4395;"SPAN ";F_span
120 !
130 ! Frequency Response Calibration
140 OUTPUT @Hp4395;"CALK N50" ! Select 50 ohm type-N Cal. kit
150 OUTPUT @Hp4395;"CALI RESP" ! Select Response cal.
160 OUTPUT @Hp4395;"CLES" ! Clear all status
170 INPUT "Connect THRU, then press [Enter].",Dum$
180 OUTPUT @Hp4395;"*SRE 4;ESNB 1" ! Set enable STB and ESB
190 ON INTR 7 GOTO Cal_end ! \ When iBASIC is used, change "7" to "8".
200 ENABLE INTR 7;2 ! /
210 OUTPUT @Hp4395;"STANC" ! Measure THRU
220 Calibrating: GOTO Calibrating
230 Cal_end: !
240 OUTPUT @Hp4395;"RESPDONE" ! Calculating cal coefficients
250 OUTPUT @Hp4395;"*OPC?" ! \ Waiting calculation end
260 ENTER @Hp4395;Dum ! /
270 DISP "Response cal completed."
280 !
290 ! Measurement
300 INPUT "Connect DUT, then press [Enter].",Dum$
310 OUTPUT @Hp4395;"CLES" ! Clear all status registers
320 OUTPUT @Hp4395;"*SRE 4;ESNB 1"
330 ON INTR 7 GOTO Sweep_end ! \ When iBASIC is used,
340 ENABLE INTR 7;2 ! / change "7" to "8"
350 OUTPUT @Hp4395;"SING" ! Sweep mode is SINGLE
360 Measuring: GOTO Measuring
370 Sweep_end: !
380 OUTPUT @Hp4395;"MKR ON" ! Marker 1 ON
390 OUTPUT @Hp4395;"SEAM MAX" ! Search MAX
400 OUTPUT @Hp4395;"OUTPMKR?" ! Output marker value
410 ENTER @Hp4395;Val1,Val2,Swp
420 PRINT "Max val:",Val1;"dB"
430 PRINT "Swp.Prmtr:",Swp;"Hz"
440 END

'''
