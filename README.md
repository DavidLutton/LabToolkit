
# Labtoolkit

Python package for instrument control, data acquisition and automation. 

## Demo

``` python
# Communicate with Hardware with PyVISA
import pyvisa
import labtoolkit
import labtoolkit.SpectrumAnalyser.AgilentE44nn

rm = pyvisa.ResourceManager()
sa = labtookit.SpectrumAnalyser.AgilentE44nn(
    rm.open_resource('GPIB0::18::INSTR')
    )

sa.frequency_center = 145e6
sa.frequency_span = 50e3
sa.sweep_points = 8192
sa.opc
df = sa.trace  
# returns a DataFrame of the trace data
# df.attrs are used to store metadata (sweep_time, resolution_bandwidth, etc)
```

## Badges
![PyPI - License](https://img.shields.io/pypi/l/Labtoolkit?color=green&style=for-the-badge)
![GitHub top language](https://img.shields.io/github/languages/top/DavidLutton/LabToolkit?style=for-the-badge)
![Read the Docs](https://img.shields.io/readthedocs/labtoolkit?style=for-the-badge)
![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/labtoolkit?style=for-the-badge)
![PyPI - Downloads](https://img.shields.io/pypi/dm/labtoolkit?style=for-the-badge)
![GitHub issues](https://img.shields.io/github/issues/davidlutton/labtoolkit?style=for-the-badge)
![GitHub pull requests](https://img.shields.io/github/issues-pr/davidlutton/labtoolkit?style=for-the-badge)
![GitHub contributors](https://img.shields.io/github/contributors/davidlutton/labtoolkit?style=for-the-badge)
![PyPI](https://img.shields.io/pypi/v/labtoolkit?style=for-the-badge)


## Authors

- [@DavidLutton](https://github.com/DavidLutton)


## Acknowledgements


 - [Awesome Readme Templates](https://awesomeopensource.com/project/elangosundar/awesome-README-templates)
 - [Awesome README](https://github.com/matiassingers/awesome-readme)
 - [How to write a Good readme](https://bulldogjob.com/news/449-how-to-write-a-good-readme-for-your-github-project)
 - [readme.so](https://readme.so/editor)
 - [Sans I/O documentation](https://sans-io.readthedocs.io/index.html) 

## Makes use of 
- [NumPy](https://numpy.org/doc/stable/user/whatisnumpy.html)
- [pandas - Python Data Analysis Library](https://pandas.pydata.org/)
- [PyVISA - Control your instruments with Python](https://pyvisa.readthedocs.io/en/latest/)
- [PyVISA-py - Pure Python backend for PyVISA](https://pyvisa.readthedocs.io/projects/pyvisa-py/en/latest/)
- [pytest - helps you write better programs](https://doc.pytest.org/en/latest/)


# Notes
Lots of the libaries that exist around PyVISA start their own ResourceManager. 

Some intentionally operate differently when using a different interface (GPIB, LAN, USB, serial)

Absolutely no changes needed to run on Linux or Windows (I don't have a Mac to test with)

To rescan the avalable instruments if needed (between tests) 

To assign drivers that simplify setting and retreaving data from instruments. Which provide a fairly common interface to instruments of the same kind (spectrum analyser, oscilloscope, VNA)

Do most of the instrument response conversion out of view (see `query_bool` or `query_float`)

Make sure I could explain how this driver layer behaves to test enginners or auditors

I know I am at least number 15 in this situation [xkcd: Standards](https://xkcd.com/927/)

I will be processing reasonably sized arrays (8k min or 40k to 100k on spectrum analyser) more from an oscilloscope so Numpy and Pandas are essential

## Units
Wherever practicible units returned are in the basic unit 

Wherever practicible inputs units are in the basic unit

For example 5e-12 rather than 5 ps

Use ... for formatting when passing to users as needed

## GUI
I have used [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/getting_started/overview.html) for myself

And for a couple of single flow applications I have used [Voilà to turn Jupyter notebooks into standalone web applications](https://github.com/voila-dashboards/voila) 

As it stands I'm planning on using [Dear PyGui: A fast and powerful Graphical User Interface Toolkit for Python with minimal dependencies](https://github.com/hoffstadt/DearPyGui)




## Existing [xkcd: Standards](https://xkcd.com/927/)
- [KE5FX GPIB Toolkit](http://www.ke5fx.com/gpib/readme.htm)
- [Galvant/InstrumentKit](https://github.com/Galvant/InstrumentKit) has stripped [numpy](https://github.com/Galvant/InstrumentKit/issues/91) out
- [LabPy/lantz](https://github.com/LabPy/lantz) has gone quiet
- [p3trus/slave](https://github.com/p3trus/slave) has gone quiet, ([breakdown of IEEE 488.2](https://slave.readthedocs.io/en/develop/basic_concepts.html#module-slave.iec60488) is tidy
- [python-ivi/python-iv](https://github.com/python-ivi/python-ivi) has gone quiet, more RF focused.
- [QCoDeS/Qcodes](https://github.com/QCoDeS/Qcodes/blob/master/qcodes/instrument_drivers/Keysight/N9030B.py)
- [scikit-rf/scikit-rf: RF and Microwave Engineering](https://github.com/scikit-rf/scikit-rf)
- ...
- [relationship between pyvisa, lantz, slave, etc · Issue #23 · python-ivi/python-ivi](https://github.com/python-ivi/python-ivi/issues/23)
- [Catalog the python lab automation landscape · Issue #23 · LabPy/labpy-discussion](https://github.com/LabPy/labpy-discussion/issues/23)
- [REVIEW: Hardware-Control: Instrument Control and Automation Package · Issue #2688 · openjournals/joss-reviews](https://github.com/openjournals/joss-reviews/issues/2688)
- [berkeleylab / hardware-control — Bitbucket](https://bitbucket.org/berkeleylab/hardware-control/src/main/)
- [python-data-acquisition/meta](https://github.com/python-data-acquisition/meta/issues/1) 
- [pycro-manager](https://pycro-manager.readthedocs.io/en/latest/) focues on microscope optical tasks, has Java controller.
- [yaq](https://yaq.fyi) seems to run daemons for everything 
- [Adding Additional RF Instrument Support · Galvant/InstrumentKit](https://github.com/Galvant/InstrumentKit/issues/212)
- [QCoDeS/Qcodes](https://github.com/QCoDeS/Qcodes) Modular data acquisition framework [15 minutes to QCoDeS](http://qcodes.github.io/Qcodes/examples/15_minutes_to_QCoDeS.html)
- [pymeasure: Scientific measurement library for instruments, experiments, and live-plotting](https://github.com/pymeasure/pymeasure)
- ...
- VISA GPIB [HP-Agilent-Keysight-equipment@groups.io | GPIB toolkit on Linux ?](https://groups.io/g/HP-Agilent-Keysight-equipment/topic/85273486#118451)
- [HP-Agilent-Keysight-equipment@groups.io | HP8695E HPIB Commands](https://groups.io/g/HP-Agilent-Keysight-equipment/topic/85912607#118981)
- [Creating and Editing Waveforms with Keysight PathWave BenchVue Software | Keysight Blogs](https://blogs.keysight.com/blogs/tech/bench.entry.html/2021/09/19/creating_and_editingwaveformswithkeysightpathw-KJgF.html)
- [Exopy’s documentation](https://exopy.readthedocs.io/en/latest/)
- [Instrbuilder: Easy Instrument Control with Python ](https://lucask07.github.io/instrbuilder/build/html/)

