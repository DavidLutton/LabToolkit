
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

## Makes use of 
- [NumPy](https://numpy.org/doc/stable/user/whatisnumpy.html)
- [pandas - Python Data Analysis Library](https://pandas.pydata.org/)
- [PyVISA - Control your instruments with Python](https://pyvisa.readthedocs.io/en/latest/)
- [PyVISA-py - Pure Python backend for PyVISA](https://pyvisa.readthedocs.io/projects/pyvisa-py/en/latest/)
- [pytest - helps you write better programs](https://doc.pytest.org/en/latest/)
