=====
Usage
=====

To use LabToolkit in a project::

    import LabToolkit as labtk

** Manual opening of instruments and assignment of drivers **

.. literalinclude:: ../examples/basic_invoke_manual_instrument_list_and_driver_assignment.py

**Basic invocation of LabToolkit with a fixed list of instruments and driver discovery**

.. literalinclude:: ../examples/basic_invoke_fixedinstrumentlist.py

**This will discover instruments and skip invoking those in the ignore list**

.. literalinclude:: ../examples/basic_invoke_discoverinstrumentlist.py

**Example of setting up for a test where a generator and a reciever are used to measure the frequency response between 1e9 and 18e9 Hz (1-18GHz) in 100e6 steps**
Where the results are saved to a spreadsheet, estimated time to completion is shown.


.. literalinclude:: ../examples/sweep.py
