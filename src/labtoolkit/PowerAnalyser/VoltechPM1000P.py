from ..IEEE488 import IEEE488


class VoltechPM1000P(IEEE488):
    """Voltech PM1000+.

    .. figure::  images/PowerAnalyser/VoltechPM1000P.jpg
    """
    pass

    '''
    “*CLS” Clears Standard Event Status Enable
    Register (ESE) and Data Status Register
    (DSR).
    “*ESE <value>” Sets the Standard Event Status Enable
    Register (ESE). The <value> sent is a
    decimal value.
    “*ESE?” Returns the value stored in the Standard
    Event Status Enable Register (ESE) as
    decimal value.
    “*ESR?” Returns the Standard Event Status
    Register (ESR) as decimal value.
    "*IDN?” Returns the product ID string.
    “*RST” Resets the unit to default settings. This
    command leaves communication settings
    unchanged.
    “*STB?” Returns the Status Byte Register (STB) as
    a decimal value.
    “:AVG <value>” Enable or disable averaging of results
    (averaging depth of 4).
    <value> = 0 → Disable (default)
    <value> = 1 → Enable
    “:AVG?” Returns status of averaging of results.
    0 → Disabled (default)
    1 → Enabled

    ":BLK:ENB” Enables blanking
    ":BLK:DIS” Disables blanking
    ":BLK?” Returns current blanking setting.
    0 → Disabled
    1 → Enabled (default)
    ":CAL:DATE?” Returns the date of last calibration.
    ":CFG:LOAD <value>” Loads requested configuration <value>= 0
    to 5, 0 = default.
    ":CFG:SAVE <value>” Saves the specified configuration
    <value>= 1 through 5.
    ":CFG:PRINT <value>" Prints the specified configuration
    <value>= 1 through 5.
    ":COM:RS2:BAUD <value>” Sets the RS232 baud rate <value> =
    9600, 19200 or 38400
    ":COM:RS2:BAUD?” Returns the current baud rate setting
    ":COM:IEE:ADDR <value>” Sets the IEEE488 (GPIB) address
    <value> = 1 - 30
    ":COM:IEE:ADDR?” Returns the current IEEE488 (GPIB)
    address setting
    “:COM:ETH:GATE?” Returns Default Gateway currently in use.
    “:COM:ETH:IP?” Returns the IP address currently in use.
    “:COM:ETH:SUB?” Returns Subnet Mask currently in use.
    “:COM:ETH:MAC <value>” Will set the MAC address. Accepts the
    lower 24 bits as ASCII hex string. Ex.
    <value> = 5AB2F1.
    “:COM:ETH:MAC?” Returns Ethernet MAC address to the
    user in hex string format.
    “:COM:ETH:STAT <value>” Sets way in which IP address is obtained.
    <value> = 0 → DHCP
    <value> = 1 → Static IP settings
    “:COM:ETH:STAT:GATE xxx.xxx.xxx.xxx” Sets the static default gateway.
    “:COM:ETH:STAT:GATE?” Returns the stored static Default Gateway.
    “:COM:ETH:STAT:IP xxx.xxx.xxx.xxx” Sets the static IP address.
    “:COM:ETH:STAT:IP?” Returns the stored static IP address.
    “:COM:ETH:STAT:SUB xxx.xxx.xxx.xxx” Sets the static subnet mask.
    “:COM:ETH:STAT:SUB?” Returns the stored static Subnet Mask.
    “:COM:ETH:STAT?” Returns the status of Static IP enabled
    flag to the user. 0 -> DHCP, 1 -> Static.
    “:DSE <value>” Sets the Data Status Enable Register
    (DSE). The <value> sent is a decimal
    value.
    “:DSE?” Returns the Data Status Enable Register
    (DSE) as decimal value.
    “:DSR?” Returns the Data Status Register (DSR)
    as decimal value.
    “:DVC” Device clear. Sets device to default
    settings. This command leaves
    communication settings unchanged.
    ":FRD?” Returns the selected values
    ":FRF?” Returns the current selection list
    ":FSR:VLT” Sets the frequency source for voltage
    ":FSR:AMP” Sets the frequency source for current
    ":FSR?” Returns the freq source 0 = volts 1 =
    amps
    ":GRA:HRM:VLT:SCL <value>” Set scaling in harmonic bar chart for Volts
    <value> = 0 - 1000
    ":GRA:HRM:AMP:SCL<value>” Set scaling in harmonic bar chart for Amps
    <value> = 0 - 100
    ":GRA:HRM:AMP:SHW” Show current bar chart
    ":GRA:HRM:VLT:SHW” Show voltage bar chart
    ":GRA:HRM:HLT” Highlights required harmonic "value" = 1
    through 50
    ":GRA:WAV:WAT <value>” <value> = 0 → Watts graph disabled
    <value> = 1 → Watts graph enabled
    ":GRA:WAV:SHW” Show waveform graph
    ":HMX:VLT:SEQ <value>” Sets odd or odd/even harmonics:
    <value> = 0 → odd/even
    <value> = 1 → odd only
    ":HMX:VLT:RNG <value>” Sets harmonic range <value> = 1 - 50
    ":HMX:VLT:FOR <value>” Sets voltage harmonic format:
    <value> = 0 → Absolute values
    <value> = 1 → Percentage of fundamental
    ":HMX:AMP:SEQ <value>” Sets odd or odd/even harmonics:
    <value> = 0 → odd/even
    <value> = 1 → odd only
    ":HMX:AMP:RNG <value>” Sets harmonic range <value> = 1 - 50
    ":HMX:AMP:FOR <value>” Sets current harmonic format:
    <value> = 0 → Absolute values
    <value> = 1 → Percentage of fundamental
    ":HMX:THD:FML <value>" Select the THD formula :
    <value> = 0 → series
    <value> = 1 → difference
    ":HMX:THD:SEQ <value>" Select the THD sequence:
    <value> = 0 → All
    <value> = 1 → odd only
    ":HMX:THD:RNG <value>" Set the THD range <value> = 2 to 50.
    ":HMX:THD:HZ <value>" Choose to include or exclude THD
    Harmonic zero:
    <value> = 0 → exclude
    <value> = 1 → include
    ":HMX:THD:DC <value>" Select the THD reference:
    <value> = 0 → fundamental
    <value> = 1 → rms
    “:INP:FILT:LPAS <value>” Sets the low pass frequency filter state:
    <value> = 0 -> Low Pass Filter Disabled
    <value> = 1 -> Low Pass Filter Enabled
    ":INP:FILT:LPAS?" Returns the state of the low pass filter.
    ":INT:START <value>" Selects either Manual Start Method or
    Clock Start Method.
    <value> = 0 → Manual Start Method
    <value> = 1 → Clock Start Method
    ":INT:MAN:RUN" Starts integration when in Manual Start
    Method. Requires integration mode
    active, manual start selected and
    integration not running.
    ":INT:MAN:STOP" Stops integration when in Manual Start
    Method. Requires integration mode active,
    manual start selected and integration
    running.
    ":INT:RESET" Resets integration values. Requires
    integration mode active and integration
    not running.
    ":INT:CLK:TIME xx-xx-xxX" Sets the start time for the integrator when
    configured for Clock Start Method. Start time sent in current PM1000+ time format.
    xx-xx-xxX stands for hh-mm-ss
    (uppercase ‘X’ is not used) for 24hr time
    format or hh-mm-ss(A or P) for AM/PM
    time format.
    ":INT:CLK:DATE xxxxxxxx" Sets the start date for the integrator when
    configured for Clock Start Method. Start
    date sent in current PM1000+ date format;
    xxxxxxxx means dd-mm-yyyy or mm-ddyyyy
    or yyyy-mm-dd according to the Date
    Format settings in the Main Menu ->
    System Configuration -> Clock -> Date
    Format.
    ":INT:CLK:DUR <value>" Sets the duration of the integrator, in
    minutes, when configured for Clock Start
    Method. (1.0 ≤ <value> ≤ 1,000,000)

    ":GRA:INT:WFM <value>" Configure integrator graph to display a
    waveform.
    <value> = 0 → Whrs
    <value> = 1 → Ahrs
    <value> = 2 → Vahrs
    <value> = 3 → VArhrs
    <value> = 4 → Watts
    <value> = 5 → VA
    <value> = 6 → Var
    <value> = 7 → Amps
    <value> = 8 → Volts
    ":GRA:INT:SHW" Change display to show integrator graph.
    Return to results screen with the
    :DSP:Z04 command.
    ":GRA:INT:SCL <value>" Configure vertical scale for the selected
    result in the integrator graph. (0.0999 ≤
    <value> ≤ 100,000)
    ":GRA:INT:DUR <value>" Configure the horizontal scale (duration),
    in minutes, when configured for Manual
    Start Method. (1.0 ≤ <value> ≤ 1,000,000)
    ":MOD:NOR” Sets normal mode.
    ":MOD:INR” Sets inrush mode.
    “:MOD:INT” Sets integrator mode.
    ":MOD:SBY” Sets standby power mode.
    ":MOD:BAL” Sets ballast mode.
    ":MOD?” Returns the current mode. 0 = Normal
    1 = Ballast
    2 = Inrush
    3 = Standby
    4 = Integrator
    ":MOD:INR:RNG <value>” Set Inrush current range <value> = 1
    through 6.
    ":MOD:INR:VRNG <value>” Set Inrush voltage range <value> = 1
    through 4.
    ":MOD:INR:CLR" Clears the Apk value when in Inrush
    mode.
    ":MOD:SBY:PER <value>" Sets the user defined period of averaging
    in Low Power Standby mode. <value>= 1
    to 300 seconds.
    ":DSP:Z04” Displays 4 results screen.
    ":DSP:Z14” Displays 14 results screen.
    ":REM:OFF” Returns PM1000+ from remote control.
    ":RNG:VLT:FIX <value>" Fixes voltage range <value> = 1 (10V) to
    4 (1000V)
    ":RNG:AMP:FIX <value>" Fixes current range <value> = 1 (0.1A) to
    6 (100A)
    ":RNG:VLT:AUT” Sets voltage on auto range.
    ":RNG:AMP:AUT” Sets current on auto range.
    ":RNG:VLT?” Returns the current voltage range.
    ":RNG:AMP?” Returns the current amps range.
    ":RNG:VLT:AUT?” Returns : 0 → Range fixed.
    1 → AutoRange engaged.
    ":RNG:AMP:AUT?” Returns : 0 → Range fixed.
    1 → AutoRange engaged.
    "*RST” Resets the PM1000+ to default settings.
    ":SCL:VLT <value>” Sets voltage scaling <value> = scaling
    factor 0.0001 to 100000.
    ":SCL:AMP <value>” Sets current scaling <value> = scaling
    factor 0.0001 to 100000.
    ":SCL:VLT?” Returns the current voltage scaling factor.

    ":SCL:AMP?” Returns the current amps scaling factor.
    ":SEL:CLR” Clears the results selection list.
    ":SEL:WAT” Selects watts.
    ":SEL:VAS” Selects VA.
    ":SEL:VAR” Selects Var.
    ":SEL:VLT” Selects Vrms.
    ":SEL:AMP” Selects Arms.
    ":SEL:PWF” Selects PF.
    ":SEL:VPK+” Selects Vpk+ (most positive peak).
    ":SEL:VPK-” Selects Vpk- (most negative peak).
    ":SEL:APK+” Selects Apk (most positive peak).
    ":SEL:APK-” Selects Apk (most negative peak).
    ":SCL:VCF” Selects Vcf.
    ":SCL:ACF” Selects Acf.
    ":SEL:WHR” Selects watt hrs.
    ":SEL:VAH” Selects VA hrs.
    ":SEL:VRH” Selects VAr hrs.
    ":SEL:AHR” Selects A hrs.
    ":SEL:VDF” Selects Vdf.
    ":SEL:ADF” Selects Adf.
    ":SEL:FRQ” Selects frequency.
    ":SEL:RES” Selects resistance R.
    ":SEL:IMP” Selects impedance Z.
    ":SEL:REA” Selects reactance X.
    ":SEL:VHM” Selects voltage harmonic series.
    ":SEL:AHM” Selects current harmonic series.
    ":SEL:HRS” Selects integration elapsed time.
    ":SEL:VDC” Selects Volts DC.
    ":SEL:ADC” Selects Amps DC.
    ":SEL:VRNG” Add the active voltage range to the
    screen.
    ":SEL:ARNG" Add the active current range to the
    screen.
    ":SHU:INT” Selects internal shunt.
    ":SHU:EXT” Selects external shunt.
    ":SHU?” Returns the current shunt setting 0 =
    internal 1 = external.
    ":SYST:TIME?” Returns the current time setting.
    ":SYST:DATE?” Returns the current date setting.
    ":SYST:SET:TIME <value>” Sets the RTC time <value> = Example 10-
    10-00.
    ":SYST:SET:DATE <value>” Sets the RTC date <value> = Example 12-
    12-2006.
    ":SYST:FOR:TIME <value>” Sets the time format <value> where 0 =
    12 Hour and 1 = 24 Hour.
    ":SYST:FOR:DATE <value>” Sets the RTC date format <value> = 0
    mmddyyyy; 1 = ddmmyyyy; 2 = yyyymmdd
    ":SYST:ZERO <value>” Set auto zero:
    <value> = 0 → disabled
    <value> = 1 → enabled
    ":SYST:ZERO?” Read auto zero state.

    As states before, there are many ways in which to send commands to the PM1000+,
    but there are some common rules for all methods.
    · All instructions should be terminated with a line feed (ASCII 10) character
    · All returned information will be terminated by a line feed (ASCII 10) character
    · Only one instruction can be sent at a time. ":SEL:VLT;:SEL:AMP" is not a valid
    command.
    · For all commands that configure the unit, allow 0.5 seconds between each
    command or use flow control to wait until the next command is sent.
    · Results are updated approximately every 0.5 seconds.
    · A range change will result in the results not being updated for the 0.5 second
    interval. Also, the running of auto-zero, which happens every 1 minute, will
    result in no new results for approximately 1 second. To avoid both of these
    scenarios, ranges can be fixed, and auto-zero can be disabled.
    Note: When utilizing communications via the Ethernet interface on the PM1000+,
    all communications will be responded to with a carriage return character, i.e.
    ASCII CR (0x0D). In the examples below the carriage return character is
    represented by “[CR]”.
    Example 1: User queries the PM1000+ to determine the status of the blanking
    setting and the PM1000+ responds with a CR added to the end of the string;
    USER: “BLK?”
    PM1000+: “1[CR]”
    The PM1000+ responds as normal with a CR character added to the end of the
    string.
    Example 2: User sends a command to the PM1000+ to disable blanking and the
    PM1000+ responds with a CR character;
    USER: “BLK:DIS”
    PM1000+: “[CR]”
    The PM1000+ responds with a CR character.
    Utilizing all other

    Basic selection and returning of result.
    The results are returned using the FRD command. This returns the results that are
    shown on the screen, in the order in which they appear on the screen. As results are
    selected using comms, the results are added to the bottom of the list, with the
    exception of harmonics, which always appear at the end of the list.
    :SEL:CLR clears all results
    :SEL:VLT
    :SEL:AMP
    :SEL:FRQ
    :SEL:WAT
    :SEL:VAS
    :SEL:VAR
    :SEL:PWF
    :SEL:VPK+
    :SEL:APK+
    :FRD? Returns Vrms, Arms, Frequency, Watts, VA, Var, power
    factor, Vpeak + and Vpeak- in floating point format.

    :FRF? Returns the results selected for confirmation using the
    label that appears on the display. In this case will return,
    “Vrms, Arms, Freq, Watt, VA, Var, PF, Vpk+, Apk+

    Returning Results Repeatedly
    The PM1000+ updates the results every 500ms. To return results as soon as they are
    available, set up the DSE register to enable bit 1, the New Data Available (NDV) bit.
    Then read the DSR register using the ":DSR?" command until it tells indicates that
    there is new data available, and then then send a ":FRD?" command to get selected
    results.
    ":DSE 2" // This enables the NDV bit.
    While strDSR <> "2"
    ":DSR?"
    strDSR = received data
    WEND
    ":FRD?"
    Receive results
    Harmonics
    To return harmonics, first the number of harmonic and the scope need to be selected
    and then they need to be added to the list of results on the display.
    :HMX:VLT:SEQ 0 Select odd and even harmonics (use 1 to select odd
    harmonics only)
    :HMX:VLT:RNG 9 Return all harmonic from 1 to 9.
    :SEL:VHM Add Voltage harmonics to the list.
    Now, assuming :SEL:CLR has not been issued after example 1, then the following
    results would be returned by :FRD?

    Vrms, Arms, Freq, Watt, VA, Var, PF, Vpk+, Apk+, Vh1 Mag, Vh1 phase, Vh2 Mag,
    Vh2 phase, …. Vh9 Mag, Vh9 phase.
    Standby power
    First, select standby power mode
    :MOD:SBY:PER 60 Set the standby power mode period to 60 seconds.
    :MOD:SBY
    :SEL:CLR Clears selection of results
    :SEL:VLT Selects Vrms
    :SEL:WAT Selects Watts
    :SEL:FRQ Selects Frequency
    :SEL:VCF Selects Volts crest factor
    :SEL:VDF Selects Volts distortion factor
    :RNG:VLT:FIX 4 Fix the voltage range to 1000Vpk
    :RNG:AMP:FIX 3 Fix the current range to 1.6Apk
    Wait 60 seconds
    :FRD? Read back values including average power over 60 seconds
    Wait 60 seconds
    :FRD? Read back value including average power over 60 seconds.
    Check against previous power.
    Inrush
    :MOD:INR Select in rush mode


    :MOD:INR:RNG 4 Fixes the current range for in rush mode to range 4 (6.25Apk)
    :MOD:INR:VRNG 4 Fixes the voltage range for in rush mode to range 4 (900Vpk)
    :MOD:INR:CLR
    :SEL:CLR Clear measurements
    :SEL:APK+ Selects peak positive current
    :SEL:APK- Selects peak negative current
    Ensure equipment under test is off
    :MOD:INR:CLR Clear the Apk+ and Apk-
    Switch on equipment under test
    :FRD? Returns Apk+ and Apk-.
    '''
