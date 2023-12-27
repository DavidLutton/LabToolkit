import numpy as np

from ..Instrument import Instrument


class Wiltron360(Instrument):
    """Wiltron 360.

    .. figure::  images/NetworkAnalyser/Wiltron360.jpg
    """
    
    def __init__(self, inst):
        super().__init__(inst)
        self.inst = inst
        self.inst.timeout = 5000  # Extend the default timeout as it can take a few seconds to get a trace
        self.inst.read_termination = ''
        self.inst.write_termination = '\n'

    def xaxis(self):
        return np.array(self.query('FMA OFV').replace(' ', '').strip().split('\n'), dtype=np.float64)

    def yaxis(self):
        return np.array(self.query('FMA OCD').strip().replace('\n', ',').split(','), dtype=np.float64).view(np.complex128)

    '''def traces(self):
        x = self.xaxis()
        store = {}

        LUT = {  # LookUp Table
            1: 'S11',
            2: 'S12',
            3: 'S21',
            4: 'S22',
        }
        for trace in 1, 2, 3, 4:
            self.select(trace)
            target = LUT[trace]
            store[target] = np.array(self.inst.query('FMA OCD').strip().replace('\n', ',').split(','), dtype=np.float64).view(np.complex128)

        # print(np.column_stack((x, y.real, y.imag)))
        return x, store
    '''

    def trace(self, trace=None):
        # x = self.xaxis()
        if trace:
            self.select(trace)
        # print(np.column_stack((x, y.real, y.imag)))
        # df = pd.DataFrame(np.column_stack((x, y.real, y.imag)), columns=['Hz', 'Real', 'Imag'])
        return self.xaxis(), self.yaxis()

    def traces(self):

        LUT = {  # LookUp Table
            1: 'S11',
            2: 'S12',
            3: 'S21',
            4: 'S22',
        }

        store = {}
        for trace in 1, 2, 3, 4:
            self.select(trace)
            target = LUT[trace]
            store[target] = self.yaxis()

        # print(np.column_stack((x, y.real, y.imag)))
        return self.xaxis(), store

    def select(self, trace):
        self.write(f'CH{trace}')

    @property
    def frequency(self):
        """."""
        return NotImplemented

    @frequency.setter
    def frequency(self, frequency):
        if type(frequency) is list:  # [6e9, 18e9]
            self.write(f'SRT {frequency[0]/1e6:.4f} MHZ STP {frequency[1]/1e6:.4f} MHZ')
        else:  # 12e9
            return NotImplementedError

    def points(self):
        self.write('FHI')

    def arange(self):  # arrange display / channels
        self.write('D14 CH1 S11 MAG CH2 S12 MAG CH3 S21 MAG CH4 S22 MAG FHI')  # TODO TBC, IFM

    def IDN(self):
        return self.query('OID').strip()


'''
print('Input a channel number to activate, or -1 to set 4 displays to LOG MAG')
while True:
    try:
        CH = int(input('CH? : '))

        if 4 >= CH >= 1:
            print('CH{}\n'.format(CH))
            inst.write('CH{}'.format(CH))

        if CH == -1:
            inst.write('D14 CH1 S11 MAG CH2 S12 MAG CH3 S21 MAG CH4 S22 MAG FHI')  # IFM

    except ValueError:
        print('ValueError')
'''

'''
D14 CH1 S11 MAG CH2 S12 MAG CH3 S21 MAG CH4 S22 MAG FHI IFM

SRT 40.0 MHZ STP 20.0 GHZ


CH1
CH2
CH3
CH4

AVG 1-4095
AOF
SON 0-20
SOF

'''

'''

colour = itertools.cycle(palette)
p = figure(title='Transmissive', x_axis_label='Frequency (MHz)', y_axis_label='dB', width=1440)  #, sizing_mode='scale_width')  # width=1800, height=900)

# p.line(x/1e6, complexto(y['S11'])['dB'], legend='op', color='black', alpha=1, line_width=2)
# p.line(x/1e6, complexto(y['S22'])['dB'], legend='op', color='black', alpha=1, line_width=2)
# p.line(x/1e6, complexto(y['S12'])['dB'], legend='op', color='black', alpha=1, line_width=2)
# p.line(x/1e6, complexto(y['S21'])['dB'], legend='op', color='black', alpha=1, line_width=2)
for s in StoCH.keys():
    if s[1]!=s[2]:
        p.line(x/1e6, complexto(y[s])['dB'], legend=s, color=next(colour), alpha=1, line_width=2)

# p.line(x/1e6, complexto(y)['dB'], legend='bar', color='blue', alpha=1, line_width=2)
# for k, v in complexto(y).items():
#    p.line(x/1e6, v, legend=k,  alpha=1, line_width=2)

# p.line(x/1e6, -6.3, legend='Limits', color='green', alpha=1, line_width=2)
# p.line(x/1e6, -5.7, legend='Limits', color='green', alpha=1, line_width=2)

# p.legend.location = "top_right"
p.legend.click_policy="hide"
p.legend.background_fill_color = "black"
p.legend.background_fill_alpha = 0.25

p.ygrid.minor_grid_line_color = 'black'
p.ygrid.minor_grid_line_alpha = 0.1

p.xgrid.minor_grid_line_color = 'black'
p.xgrid.minor_grid_line_alpha = 0.1
# p.background_fill_color = "gray"

# p.background_fill_alpha = 0.2
pb = figure(title='Reflective', x_axis_label='Frequency (MHz)', y_axis_label='dB', x_range=p.x_range,  width=1440)  #, sizing_mode='scale_width')
for s in StoCH.keys():
    if s[1]==s[2]:
        pb.line(x/1e6, complexto(y[s])['dB'], legend=s, color=next(colour), alpha=1, line_width=2)

# p.line(x/1e6, -6.3, legend='Limits', color='green', alpha=1, line_width=2)
# p.line(x/1e6, -5.7, legend='Limits', color='green', alpha=1, line_width=2)

# p.legend.location = "top_right"
pb.legend.click_policy="hide"
pb.legend.background_fill_color = "black"
pb.legend.background_fill_alpha = 0.25

pb.ygrid.minor_grid_line_color = 'black'
pb.ygrid.minor_grid_line_alpha = 0.1

pb.xgrid.minor_grid_line_color = 'black'
pb.xgrid.minor_grid_line_alpha = 0.1
# p.background_fill_color = "gray"

# p.background_fill_alpha = 0.2

# show(p)
ps = gridplot([[p],[pb]])

# show the results
show(ps)
'''

'''
colors = itertools.cycle(palette)
p = figure(title='Title', x_axis_label='Frequency (MHz)', y_axis_label='dB', width=1600)  #, sizing_mode='scale_width')  # width=1800, height=900)

# p.line(x/1e6, complexto(yy)['dB'], legend='op', color=next(colors), alpha=1, line_width=2)



p.line(x/1e6, complexto(y)['dB'], legend='...', color=next(colors), alpha=1, line_width=2)


# p.line(x/1e6, complexto(y['S11'])['dB'], legend='S11', color=next(colors), alpha=1, line_width=2)
# p.line(x/1e6, complexto(y['S12'])['dB'], legend='S12', color=next(colors), alpha=1, line_width=2)
# p.line(x/1e6, complexto(y['S21'])['dB'], legend='S21', color=next(colors), alpha=1, line_width=2)
# p.line(x/1e6, complexto(y['S22'])['dB'], legend='S22', color=next(colors), alpha=1, line_width=2)

# for k, v in complexto(y).items():
#    p.line(x/1e6, v, legend=k,  alpha=1, line_width=2)

# p.line(x/1e6, 0, legend='Limits', color='green', alpha=1, line_width=2)
# p.line(x/1e6, -3, legend='Limits', color='green', alpha=1, line_width=2)
# p.line(x/1e6, -10, legend='Limits', color='green', alpha=1, line_width=2)
# p.line(x/1e6, -20, legend='Limits', color='green', alpha=1, line_width=2)

# p.legend.location = "top_right"
p.legend.click_policy="hide"
p.legend.background_fill_color = "black"
p.legend.background_fill_alpha = 0.25

p.ygrid.minor_grid_line_color = 'black'
p.ygrid.minor_grid_line_alpha = 0.1

p.xgrid.minor_grid_line_color = 'black'
p.xgrid.minor_grid_line_alpha = 0.1
# p.background_fill_color = "gray"

# p.background_fill_alpha = 0.2

p.border_fill_color = 'whitesmoke'

# p.background_fill_alpha = 1
# p.background_fill_color = "gray"
p.x_range.range_padding = 0.025
p.y_range.range_padding = 0.1
'''

'''

inst.query('OFV')
# ' 040.000000000000000E+06\n 280.000000000000000E+06\n 520.000000100000000E+06\n 760.000000100000000E+06\n 001.000000000000000E+09\n 001.240000000000000E+09\n 001.480000000000000E+09\n 001.720000000000000E+09\n 001.960000000000000E+09\n 002.200000000000000E+09\n 002.440000000000000E+09\n 002.680000000000000E+09\n 002.920000000000000E+09\n 003.160000000000000E+09\n 003.400000000000000E+09\n 003.640000000000000E+09\n 003.880000000000000E+09\n 004.120000000000000E+09\n 004.360000000000000E+09\n 004.600000000000000E+09\n 004.840000000000000E+09\n 005.080000000000000E+09\n 005.320000000000000E+09\n 005.560000000000000E+09\n 005.800000000000000E+09\n 006.040000000000000E+09\n 006.280000000000000E+09\n 006.520000000000000E+09\n 006.760000000000000E+09\n 007.000000000000000E+09\n 007.240000000000000E+09\n 007.480000000000000E+09\n 007.720000000000000E+09\n 007.960000000000000E+09\n 008.200000000000000E+09\n 008.440000000000000E+09\n 008.680000000000000E+09\n 008.920000000000000E+09\n 009.160000000000000E+09\n 009.400000000000000E+09\n 009.640000000000000E+09\n 009.880000000000000E+09\n 010.120000000000000E+09\n 010.360000000000000E+09\n 010.600000000000000E+09\n 010.840000000000000E+09\n 011.080000000000000E+09\n 011.320000000000000E+09\n 011.560000000000000E+09\n 011.800000000000000E+09\n 012.040000000000000E+09\n 012.280000000000000E+09\n 012.520000000000000E+09\n 012.760000000000000E+09\n 013.000000000000000E+09\n 013.240000000000000E+09\n 013.480000000000000E+09\n 013.720000000000000E+09\n 013.960000000000000E+09\n 014.200000000000000E+09\n 014.440000000000000E+09\n 014.680000000000000E+09\n 014.920000000000000E+09\n 015.160000000000000E+09\n 015.400000000000000E+09\n 015.640000000000000E+09\n 015.880000000000000E+09\n 016.120000000000000E+09\n 016.360000000000000E+09\n 016.600000000000000E+09\n 016.840000000000000E+09\n 017.080000000000000E+09\n 017.320000000000000E+09\n 017.560000000000000E+09\n 017.800000000000000E+09\n 018.040000000000000E+09\n 018.280000000000000E+09\n 018.520000000000000E+09\n 018.760000000000000E+09\n 019.000000000000000E+09\n 019.240000000000000E+09\n 019.480000000000000E+09\n 019.720000000000000E+09\n 019.960000000000000E+09\n 020.200000000000000E+09\n 020.440000000000000E+09\n 020.680000000000000E+09\n 020.920000000000000E+09\n 021.160000000000000E+09\n 021.400000000000000E+09\n 021.640000000000000E+09\n 021.880000000000000E+09\n 022.120000000000000E+09\n 022.360000000000000E+09\n 022.600000000000000E+09\n 022.840000000000000E+09\n 023.080000000000000E+09\n 023.320000000000000E+09\n 023.560000000000000E+09\n 023.800000000000000E+09\n 024.040000000000000E+09\n 024.280000000000000E+09\n 024.520000000000000E+09\n 024.760000000000000E+09\n 025.000000000000000E+09\n 025.240000000000000E+09\n 025.480000000000000E+09\n 025.720000000000000E+09\n 025.960000000000000E+09\n 026.200000000000000E+09\n 026.440000000000000E+09\n 026.680000000000000E+09\n 026.920000000000000E+09\n 027.160000000000000E+09\n 027.400000000000000E+09\n 027.640000000000000E+09\n 027.880000000000000E+09\n 028.120000000000000E+09\n 028.360000000000000E+09\n 028.600000000000000E+09\n 028.840000000000000E+09\n 029.080000000000000E+09\n 029.320000000000000E+09\n 029.560000000000000E+09\n 029.800000000000000E+09\n 030.040000000000000E+09\n 030.280000000000000E+09\n 030.520000000000000E+09\n 030.760000000000000E+09\n 031.000000000000000E+09\n 031.240000000000000E+09\n 031.480000000000000E+09\n 031.720000000000000E+09\n 031.960000000000000E+09\n 032.200000000000000E+09\n 032.440000000000000E+09\n 032.680000000000000E+09\n 032.920000000000000E+09\n 033.160000000000000E+09\n 033.400000000000000E+09\n 033.640000000000000E+09\n 033.880000000000000E+09\n 034.120000000000000E+09\n 034.360000000000000E+09\n 034.600000000000000E+09\n 034.840000000000000E+09\n 035.080000000000000E+09\n 035.320000000000000E+09\n 035.560000000000000E+09\n 035.800000000000000E+09\n 036.040000000000000E+09\n 036.280000000000000E+09\n 036.520000000000000E+09\n 036.760000000000000E+09\n 037.000000000000000E+09\n 037.240000000000000E+09\n 037.480000000000000E+09\n 037.720000000000000E+09\n 037.960000000000000E+09\n 038.200000000000000E+09\n 038.440000000000000E+09\n 038.680000000000000E+09\n 038.920000000000000E+09\n 039.160000000000000E+09\n 039.400000000000000E+09\n 039.640000000000000E+09\n 039.880000000000000E+09\n 040.000000000000000E+09\n'

inst.query_ascii_values('OFV', separator='\n ')
'''
'''
[40000000.0,
 280000000.0,
 520000000.1,

 39640000000.0,
 39880000000.0,
 40000000000.0]
'''

# inst.query('OID')
# ' 360 0.04000040.000000-007.0 005.0 03.08\r\n'

# inst.query('OCD').strip(' ').split('\n')[:-1]

'''
['-434.136105500000000E-06, 012.652299400000000E-03',
 '-045.860499100000000E-03, 134.559795300000000E-03',
 '-184.055939400000000E-03, 188.549593100000000E-03',

 ' 387.497931800000000E-03,-231.315508500000000E-03']
'''
'''

  # print(wiltron.inst.query_ascii_values("OFV"))
    # wiltron.inst.write('FMA')
    # time.sleep(1)
    # data = wiltron.inst.query_binary_values('FMC MSB OFV', delay=0.2)
    wiltron.inst.write('FMC MSB OCD')
    data = wiltron.inst.read_raw()
    print(data)
'''


'''
OFV

OCD
'''

'''

    data = wiltron.inst.query('FMA MSB OFV', delay=0.2)
    # data = data.strip().split(" ")
    # data = wiltron.inst.query('FMA MSB OFV', delay=0.2)
    # print(wiltron.inst.read())
    print(data)
    print(len(data))
    
    data = wiltron.inst.query('FMA MSB OCD', delay=0.2)
    # data = data.strip().split(" ")
    # data = wiltron.inst.query('FMA MSB OFV', delay=0.2)
    # print(wiltron.inst.read())
    print(data)
    print(len(data))
    # data = wiltron.inst.query('FMA MSB OFV', delay=0.2)
    # print(wiltron.inst.read())
    # print(data)
    # print(len(data))
    wiltron.inst.write('FMA')
''' 

