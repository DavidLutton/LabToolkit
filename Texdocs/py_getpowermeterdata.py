import visa
# visa.log_to_screen()

rm = visa.ResourceManager()

resource_name = "GPIB0::11::INSTR"
inst = rm.open_resource(resource_name)

IDN = inst.query('*IDN?')  # HEWLETT-PACKARD,437B,,2.0

print(inst.query("?"))  # float(0.0)
