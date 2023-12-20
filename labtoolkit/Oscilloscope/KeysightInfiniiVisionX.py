from ..IEEE488 import IEEE488
from ..SCPI import SCPI
import numpy as np
import pandas as pd

import PIL.Image as Image
import io

'''
inst.write(':WAVEFORM:SOURCE CHANNEL 1')
print(int(inst.query(':ACQuire:POINts?')))
print(inst.query(':CHANNEL1:UNITs?'))
inst.write(':WAVEeform:POINts:MODE MAXimum')
print(int(inst.query(':ACQuire:POINts?')))
# inst.write(':WAVEeform:POINts 2000000')
inst.write(':OPER:COND?')
inst.write(':STOP;:DIGITIZE:CHANNEL1')
inst.write(':WAVEFORM:BYTEORDER LSBFIRST')
inst.write(':WAVEFORM:FORMAT WORD')
inst.write(':WAVEFORM:UNSIGNED 1')
print(inst.query(':WAVEFORM:YORIGIN?'))
print(inst.query(':WAVEFORM:YREFERENCE?'))
print(inst.query(':WAVEFORM:YINCREMENT?'))
print(inst.query(':WAVEFORM:XORIGIN?'))
print(inst.query(':WAVEFORM:XREFERENCE?'))
print(inst.query(':WAVEFORM:XINCREMENT?'))
print(inst.query(':WAVEFORM:TYPE?'))
# :WAV:DATA?
y = inst.query_binary_values(':WAV:DATA?')
print(inst.query(':TIMEBASE:RANGE?'))
print(inst.query(':TIMEBASE:POSITION?'))
print(inst.query(':TIMEBASE:REFERENCE?'))
inst.write(':RUN?')
plt.figure(figsize=[6.4*3, 4.8*3])
plt.plot(y)

# x
# plt.plot(x, y)
# xy = np.array([x, y])
# np.save('xy.npy', xy)

float(inst.query(':MEASure:FREQuency?'))
inst.query(':SYSTem:SETup?')  # '#800136414<setup prod="InfiniiVision" ver="04.08.2016071801" srver="3.0">\r'



GSInfiniivision.query(':SYSTEM:DSP "";*OPC?') # Turns off previously displayed (non-error) messages

#The following command defines whether the image background will be black or white.
#If you want to save ink, turn on this 'inksaver' setting.
GSInfiniivision.write(":HARDCOPY:INKSAVER OFF")
# Ask scope for screenshot in png format
if generation == "Older_Series":
    GSInfiniivision.write(":DISPlAY:DATA? PNG, SCREEN, COLOR") # The older InfiniiVisions have 3 parameters
elif generation == "X_Series":
    GSInfiniivision.write(":DISPlAY:DATA? PNG, COLOR") # The newer InfiniiVision-Xs do not have the middle parameter above



'''


class KeysightInfiniiVisionX(IEEE488, SCPI):
    '''.

    ## DSO5000A, DSO/MSO6000A/L, DSO/MSO7000A/B, DSO/MSO-X2000A, DSO/MSO-X3000A/T, DSO/MSO-X4000A, DSO/MSO-X6000A
    https://www.keysight.com/gb/en/support/key-35068/infiniivision-3000t-x-series-oscilloscopes.html#drivers
    # '''

    def __post__(self):
        self.clock_update()
        
    
    def screenshot(self):
        self.query(':SYSTEM:DSP "";*OPC?')  # clear messages
        self.write(":HARDCOPY:INKSAVER OFF")

        model = self.IDN.split(',')[1]
        if model[3] == "-" or model[1] == "9":
            screenshot_command = ":DISPlAY:DATA? PNG, COLOR"  # DSOX series
        else:
            screenshot_command = ":DISPlAY:DATA? PNG, SCREEN, COLOR"  # DSO series

        return Image.open(io.BytesIO(self.query_binary_values(
            screenshot_command,
            datatype='B',
            is_big_endian=False,
            container=bytearray)))

    @property    
    def channels(self):
        IDN = str(self.query('*IDN?'))
        IDN = IDN.split(',')  # IDN parts are separated by commas, so parse on the commas
        MODEL = IDN[1]
        if list(MODEL[1]) == '9':  # This is the test for the PXIe scope, M942xA)
            NUMBER_ANALOG_CHS = 2
        else:
            NUMBER_ANALOG_CHS = int(MODEL[len(MODEL) - 2])
        return np.arange(1, NUMBER_ANALOG_CHS + 1)

    def displayed(self, channel):
        return self.query_bool(f':CHANnel{channel}:DISPlay?')

    def get_traces_from_displayed_channels(self):
        # # Actually find which channels are on, have acquired data, and get the pre-amble info if needed.
        # # The assumption here is that, if the channel is off, even if it has data behind it, data will not be retrieved from it.
        # # Note that this only has to be done once for repetitive acquisitions if the channel scales (and on/off) are not changed.

        displayed_channels = [channel for channel in self.channels if self.displayed(channel) == True]

        return displayed_channels

    def trace(self, channel):
        self.write(f':WAVEFORM:SOURCE CHANNEL{channel}')
        self.write(":WAVeform:POINts:MODE MAX")  # MAX mode works for all acquisition types, so this is done here to avoid Acq. Type vs points mode problems. Adjusted later for specific acquisition types.

        # Pre = self.query(f":WAVeform:SOURce CHANnel{channel};:WAVeform:PREamble?").split(',')
        Pre = self.query(f":WAVeform:PREamble?").split(',')
        Y_INCrement = float(Pre[7])  # Voltage difference between data points; Could also be found with :WAVeform:YINCrement? after setting :WAVeform:SOURce
        Y_ORIGin    = float(Pre[8])  # Voltage at center screen; Could also be found with :WAVeform:YORigin? after setting :WAVeform:SOURce
        Y_REFerence = float(Pre[9])  # Specifies the data point where y-origin occurs, always zero; Could also be found with :WAVeform:YREFerence? after setting :WAVeform:SOURce
        # # The programmer's guide has a very good description of this, under the info on :WAVeform:PREamble.
        # # In most cases this will need to be done for each channel as the vertical scale and offset will differ. However,
        # # if the vertical scales and offset are identical, the values for one channel can be used for the others.
        # # For math waveforms, this should always be done.
        # # Determine Acquisition Type to set points mode properly

        ACQ_TYPE = self.query(":ACQuire:TYPE?")
                ## This can also be done when pulling pre-ambles (pre[1]) or may be known ahead of time, but since the script is supposed to find everything, it is done now.
        if ACQ_TYPE == "AVER" or ACQ_TYPE == "HRES": # Don't need to check for both types of mnemonics like this: if ACQ_TYPE == "AVER" or ACQ_TYPE == "AVERage": becasue the scope ALWAYS returns the short form
            POINTS_MODE = "NORMal" # Use for Average and High Resoultion acquisition Types.
                ## If the :WAVeform:POINts:MODE is RAW, and the Acquisition Type is Average, the number of points available is 0. If :WAVeform:POINts:MODE is MAX, it may or may not return 0 points.
                ## If the :WAVeform:POINts:MODE is RAW, and the Acquisition Type is High Resolution, then the effect is (mostly) the same as if the Acq. Type was Normal (no box-car averaging).
                ## Note: if you use :SINGle to acquire the waveform in AVERage Acq. Type, no average is performed, and RAW works. See sample script "InfiniiVision_2_Simple_Synchronization_Methods.py"
        else:
            POINTS_MODE = "RAW" # Use for Acq. Type NORMal or PEAK
            ## Note, if using "precision mode" on 5/6/70000s or X6000A, then you must use POINTS_MODE = "NORMal" to get the "precision record."

        ## Note:
            ## :WAVeform:POINts:MODE RAW corresponds to saving the ASCII XY or Binary data formats to a USB stick on the scope
            ## :WAVeform:POINts:MODE NORMal corresponds to saving the CSV or H5 data formats to a USB stick on the scope

        ###########################################################################################################
        ## Find max points for scope as is, ask for desired points, find how many points will actually be returned
            ## KEY POINT: the data must be on screen to be retrieved.  If there is data off-screen, :WAVeform:POINts? will not "see it."
                ## Addendum 1 shows how to properly get all data on screen, but this is never needed for Average and High Resolution Acquisition Types,
                ## since they basically don't use off-screen data; what you see is what you get.

        # # First, set waveform source to any channel that is known to be on and have points, here the FIRST_CHANNEL_ON - if we don't do this, it could be set to a channel that was off or did not acquire data.
        # ## self.write(":WAVeform:SOURce CHANnel" + str(FIRST_CHANNEL_ON))
        self.write(f":WAVeform:SOURce CHANnel{channel}")

        # # The next line is similar to, but distinct from, the previously sent command ":WAVeform:POINts:MODE MAX".  This next command is one of the most important parts of this script.
        self.write(":WAVeform:POINts MAX") # This command sets the points mode to MAX AND ensures that the maximum # of points to be transferred is set, though they must still be on screen

        # # Since the ":WAVeform:POINts MAX" command above also changes the :POINts:MODE to MAXimum, which may or may not be a good thing, so change it to what is needed next.
        self.write(":WAVeform:POINts:MODE " + str(POINTS_MODE))
        # # If measurements are also being made, they are made on the "measurement record."  This record can be accessed by using:
            # # :WAVeform:POINts:MODE NORMal instead of :WAVeform:POINts:MODE RAW
            # # Please refer to the progammer's guide for more details on :WAV:POIN:MODE RAW/NORMal/MAX

        # # Now find how many points are actually currently available for transfer in the given points mode (must still be on screen)
        MAX_CURRENTLY_AVAILABLE_POINTS = int(self.query("WAVeform:POINts?")) # This is the max number of points currently available - this is for on screen data only - Will not change channel to channel.
        # print(MAX_CURRENTLY_AVAILABLE_POINTS)
        # # NOTES:
            # # For getting ALL of the data off of the scope, as opposed to just what is on screen, see Addendum 1
            # # For getting ONLY CERTAIN data points, see Addendum 2
            # # The methods shown in these addenda are combinable
            # # The number of points can change with the number of channels that have acquired data, the Acq. Mode, Acq Type, time scale (they must be on screen to be retrieved),
                # # number of channels on, and the acquisition method (:RUNS/:STOP, :SINGle, :DIGitize), and :WAV:POINts:MODE

        # # The scope will return a -222,"Data out of range" error if fewer than 100 points are requested, even though it may actually return fewer than 100 points.
        USER_REQUESTED_POINTS = 555
        if USER_REQUESTED_POINTS < 100:
            USER_REQUESTED_POINTS = 100
        # # One may also wish to do other tests, such as: is it a whole number (integer)?, is it real? and so forth...

        if MAX_CURRENTLY_AVAILABLE_POINTS < 100:
            MAX_CURRENTLY_AVAILABLE_POINTS = 100

        if USER_REQUESTED_POINTS > MAX_CURRENTLY_AVAILABLE_POINTS or ACQ_TYPE == "PEAK":
            USER_REQUESTED_POINTS = MAX_CURRENTLY_AVAILABLE_POINTS
            ## Note: for Peak Detect, it is always suggested to transfer the max number of points available so that narrow spikes are not missed.
            ## If the scope is asked for more points than :ACQuire:POINts? (see below) yields, though, not necessarily MAX_CURRENTLY_AVAILABLE_POINTS, it will throw an error, specifically -222,"Data out of range"

        ## If one wants some other number of points...
        ## Tell it how many points you want
        ## self.write(":WAVeform:POINts " + str(USER_REQUESTED_POINTS))
        
        ## Then ask how many points it will actually give you, as it may not give you exactly what you want.
        NUMBER_OF_POINTS_TO_ACTUALLY_RETRIEVE = int(self.query(":WAVeform:POINts?"))
        ## Warn user if points will be less than requested, if desired...
        ## Note that if less than the max is set, it will stay at that value (or whatever is closest) until it is changed again, even if the time base is changed.
        ## What does the scope return if less than MAX_CURRENTLY_AVAILABLE_POINTS is returned?
            ## It depends on the :WAVeform:POINts:MODE
            ## If :WAVeform:POINts:MODE is RAW
                ## The scope decimates the data, only returning every Nth point.
                ## The points are NOT re-mapped; the values of the points, both vertical and horizontal, are preserved.
                ## Aliasing, lost pulses and transitions, are very possible when this is done.
            ## If :WAVeform:POINts:MODE is NORMal
                ## The scope re-maps this "measurement record" down to the number of points requested to give the best representation of the waveform for the requested number of points.
                ## This changes both the vertical and horizontal values.
                ## Aliasing, lost pulses and transitions, are definitely possible, though less likely for well displayed waveforms in many, but not all, cases.

        ## This above method always works w/o errors.  In summary, after an acquisition is complete:
                ## Set POINts to MAX
                ## Set :POINts:MODE as desired/needed
                ## Ask for the number of points available.  This is the MOST the scope can give for current settings/timescale/Acq. Type
                ## Set a different number of points if desired and if less than above
                ## Ask how many points it will actually return, use that

        ## What about :ACQUIRE:POINTS?
        ## The Programmers's Guide says:
            ## The :ACQuire:POINts? query returns the number of data points that the
            ## hardware will acquire from the input signal. The number of points
            ## acquired is not directly controllable. To set the number of points to be
            ## transferred from the oscilloscope, use the command :WAVeform:POINts. The
            ## :WAVeform:POINts? query will return the number of points available to be
            ## transferred from the oscilloscope.

        ## It is not a terribly useful query. It basically only gives the max amount of points available for transfer if:
                ## The scope is stopped AND has acquired data the way you want to use it and the waveform is entirely on screen
                    ## In other words, if you do a :SINGle, THEN turn on, say digital chs, this will give the wrong answer for digital chs on for the next acquisition.
                ## :POINts:MODE is RAW or MAX - thus it DOES NOT work for Average or High Res. Acq. Types, which need NORMal!
                ## and RUN/STOP vs SINGle vs :DIG makes a difference!
                ## and Acq. Type makes a difference! (it can be misleading for Average or High Res. Acq. Types)
                ## and all of the data is on screen!
                ## Thus it is not too useful here.
        ## What it is good for is:
            ## 1. determining if there is off screen data, for Normal or Peak Detect Acq. Types, after an acquisition is complete, for the current settings (compare this result with MAX_CURRENTLY_AVAILABLE_POINTS).
            ## 2. finding the max possible points that could possibly be available for Normal or Peak Detect Acq. Types, after an acquisition is complete, for the current settings, if all of the data is on-screen.

        #####################################################################################################################################
        #####################################################################################################################################
        ## Get timing pre-amble data and create time axis
        ## One could just save off the preamble factors and #points and post process this later...

        Pre = self.query(":WAVeform:PREamble?").split(',') # This does need to be set to a channel that is on, but that is already done... e.g. Pre = KsInfiniiVisionX.query(":WAVeform:SOURce CHANnel" + str(FIRST_CHANNEL_ON) + ";PREamble?").split(',')
        ## While these values can always be used for all analog channels, they need to be retrieved and used separately for math/other waveforms as they will likely be different.
        #ACQ_TYPE    = float(Pre[1]) # Gives the scope Acquisition Type; this is already done above in this particular script
        X_INCrement = float(Pre[4]) # Time difference between data points; Could also be found with :WAVeform:XINCrement? after setting :WAVeform:SOURce
        X_ORIGin    = float(Pre[5]) # Always the first data point in memory; Could also be found with :WAVeform:XORigin? after setting :WAVeform:SOURce
        X_REFerence = float(Pre[6]) # Specifies the data point associated with x-origin; The x-reference point is the first point displayed and XREFerence is always 0.; Could also be found with :WAVeform:XREFerence? after setting :WAVeform:SOURce
        ## This could have been pulled earlier...
        del Pre
            ## The programmer's guide has a very good description of this, under the info on :WAVeform:PREamble.
            ## This could also be reasonably be done when pulling the vertical pre-ambles for any channel that is on and acquired data.
            ## This is the same for all channels.
            ## For repetitive acquisitions, it only needs to be done once unless settings change.

        time = ((np.linspace(0,NUMBER_OF_POINTS_TO_ACTUALLY_RETRIEVE-1,NUMBER_OF_POINTS_TO_ACTUALLY_RETRIEVE)-X_REFerence)*X_INCrement)+X_ORIGin
        if ACQ_TYPE == "PEAK": # This means Peak Detect Acq. Type
            DataTime = np.repeat(DataTime,2)
            ##  The points come out as Low(time1),High(time1),Low(time2),High(time2)....
            ### SEE IMPORTANT NOTE ABOUT PEAK DETECT AT VERY END, specific to fast time scales
        ###################################################################################################
        ###################################################################################################
        ## Determine number of bytes that will actually be transferred and set the "chunk size" accordingly.

            ## When using PyVisa, this is in fact completely unnecessary, but may be needed in other leagues, MATLAB, for example.
            ## However, the benefit in Python is that the transfers can take less time, particularly longer ones.

        ## Get the waveform format
        WFORM = str(self.query(":WAVeform:FORMat?"))
        if WFORM == "BYTE":
            FORMAT_MULTIPLIER = 1
        else: #WFORM == "WORD"
            FORMAT_MULTIPLIER = 2

        if ACQ_TYPE == "PEAK":
            POINTS_MULTIPLIER = 2 # Recall that Peak Acq. Type basically doubles the number of points.
        else:
            POINTS_MULTIPLIER = 1

        TOTAL_BYTES_TO_XFER = POINTS_MULTIPLIER * NUMBER_OF_POINTS_TO_ACTUALLY_RETRIEVE * FORMAT_MULTIPLIER + 11
            ## Why + 11?  The IEEE488.2 waveform header for definite length binary blocks (what this will use) consists of 10 bytes.  The default termination character, \n, takes up another byte.
                ## If you are using mutliplr termination characters, adjust accordingly.
            ## Note that Python 2.7 uses ASCII, where all characters are 1 byte.  Python 3.5 uses Unicode, which does not have a set number of bytes per character.

        ## Set chunk size:
            ## More info @ http://pyvisa.readthedocs.io/en/stable/resources.html
        if TOTAL_BYTES_TO_XFER >= 400000:
            pass
            # KsInfiniiVisionX.chunk_size = TOTAL_BYTES_TO_XFER
        ## else:
            ## use default size, which is 20480

        ## Any given user may want to tweak this for best throughput, if desired.  The 400,000 was chosen after testing various chunk sizes over various transfer sizes, over USB,
            ## and determined to be the best, or at least simplest, cutoff.  When the transfers are smaller, the intrinsic "latencies" seem to dominate, and the default chunk size works fine.

        ## How does the default chuck size work?
            ## It just pulls the data repeatedly and sequentially (in series) until the termination character is found...

        ## Do I need to adjust the timeout for a larger chunk sizes, where it will pull up to an entire 8,000,000 sample record in a single IO transaction?
            ## If you use a 10s timeout (10,000 ms in PyVisa), that will be good enough for USB and LAN.
            ## If you are using GPIB, which is slower than LAN or USB, quite possibly, yes.
            ## If you don't want to deal with this, don't set the chunk size, and use a 10 second timeout, and everything will be fine in Python.
                ## When you use the default chunk size, there are repeated IO transactions to pull the total waveform.  It is each individual IO transaction that needs to complete within the timeout.

        #####################################################
        ## Setup data export - For repetitive acquisitions, this only needs to be done once unless settings are changed
        self.write(":WAVeform:FORMat WORD") # 16 bit word format... or BYTE for 8 bit format - WORD recommended, see more comments below when the data is actually retrieved
        ## WORD format especially  recommended  for Average and High Res. Acq. Types, which can produce more than 8 bits of resolution.
        self.write(":WAVeform:BYTeorder LSBFirst") # Explicitly set this to avoid confusion - only applies to WORD FORMat
        self.write(":WAVeform:UNSigned 0") # Explicitly set this to avoid confusion
        #####################################################
        ## Pull waveform data, scale it
        
        ## Gets the waveform in 16 bit WORD format
        ## The below method uses an IEEE488.2 compliant definite length binary block transfer invoked by :WAVeform:DATA?.
            ## ASCII transfers are also possible, but MUCH slower.
        data = self.query_binary_values(f':WAVeform:SOURce CHANnel{channel};DATA?', "h", False, container=np.array)
        # print(len(data))
        ## Here, WORD format, LSBF, and signed integers are used (these are the scope settings in this script).  The query_binary_values function must be setup the same (https://docs.python.org/2/library/struct.html#format-characters):
                ## For BYTE format and unsigned, use "b" instead of "h"; b is a signed char; see link from above line
                ## For BYTE format and signed,   use "B" instead of "h"; B is an unsigned char
                ## For WORD format and unsigned, use "h"; h is a short
                ## For WORD format and signed,   use "H" instead of "h"; H is an unsigned short
                ## For MSBFirst use True (Don't use MSBFirst unless that is the computer architecture - most common WinTel are LSBF - see sys.byteorder @ https://docs.python.org/2/library/sys.html)

            ## WORD is more accurate, but slower for long records, say over 100 kPts.
            ## WORD strongly suggested for Average and High Res. Acquisition Types.

            ## query_binary_values() is a PyVisa specific IEEE 488.2 binary block reader.  Most languages have a similar function.
                ## The InfiniiVision and InfiniiVision-X scopes always return a definite length binary block in response to the :WAVeform:DATA? querry
                ## query_binary_values() does also read the termination character, but this is not always the case in other languages (MATLAB, for example)
                    ## In that case, another read is needed to read the termination character (or a device clear).
                ## In the case of Keysight VISA (IO Libraries), the default termination character is '\n' but this can be changed, depending on the interface....
                    ## For more on termination characters: https://PyVisa.readthedocs.io/en/stable/resources.html#termination-characters

            ## Notice that the waveform source is specified, and the actual data query is concatenated into one line with a semi-colon (;) essentially like this:
                ## :WAVeform:SOURce CHANnel1;DATA?
                ## This makes it "go" a little faster.

            ## When the data is being exported w/ :WAVeform:DATA?, the oscilloscope front panel knobs don't work; they are blocked like :DIGitize, and the actions take effect AFTER the data transfer is complete.
            ## The :WAVeform:DATA? query can be interrupted without an error by doing a device clear: KsInfiniiVisionX.clear()

        ## Scales the waveform
        ## One could just save off the preamble factors and post process this later.
        
        # return time, (( data - Y_REFerence ) * Y_INCrement ) + Y_ORIGin
        return pd.DataFrame(
            np.column_stack(
                (time, (( data - Y_REFerence ) * Y_INCrement ) + Y_ORIGin)
                ), 
            columns=['Time (s)','Channel (V)']
            ).set_index('Time (s)')


        