"""."""
import functools

from pyvisa import VisaIOError


def rsetattr(obj, attr, val):
    # https://stackoverflow.com/a/31174427

    pre, _, post = attr.rpartition('.')
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)


def rgetattr(obj, attr, *args):
    # https://stackoverflow.com/a/31174427
    def _getattr(obj, attr):
        return getattr(obj, attr, *args)
    try:
        return functools.reduce(_getattr, [obj] + attr.split('.'))
    except AttributeError:
        return None


def drivers_list(labtoolkit):
    return [rgetattr(labtoolkit, f'{x}.REGISTER') for x in labtoolkit.__all__ if rgetattr(labtoolkit, f'{x}.REGISTER')]


def drivers_show(labtoolkit):
    for reg in sorted([x for x in labtoolkit.__all__ if rgetattr(labtoolkit, f'{x}.REGISTER')]):
        # print(f'{reg}:')
        di = rgetattr(labtoolkit, f'{reg}.REGISTER')
        for i in di:
            print(f'{i:34} {reg:24} {str(di[i]).split(".")[-1][:-2]}')
        print()


def enumerate_instruments(labtoolkit, rm, resources, *, ignores=None, static=None):

    class Instruments:

        def __repr__(self):
            # return str(self.__dict__)  # .items()
            buffer = []
            for x in self.__dict__:
                buffer.append(f'{x}:\n')
                for index, each in enumerate(instruments.__dict__[x]):
                    buffer.append(f'\t{index}: {each}\n')
            return ''.join(buffer)

    instruments = Instruments()

    # pprint(resources)
    for ignore in ignores:  # pd.read_excel(latest('Config pyVISA v*.xlsx'), sheet_name='Ignore').dropna(how='all')['Resource Prefix']:
        resources = [x for x in resources if not x.startswith(ignore)]

    for static in static.iterrows():

        # pd.read_excel(latest('Config pyVISA v*.xlsx'), sheet_name='Data').dropna(how='all')
        # print(static[1])
        # print(static[1].Resource)
        if static[1].Enable:
            if static[1].Resource in resources:
                resources.remove(static[1].Resource)
                fam = static[1].Family
                inst = rm.open_resource(static[1].Resource)
                try:
                    driver = rgetattr(labtoolkit, static[1].Driver)(inst)
                except TypeError:
                    raise TypeError(f'Check the driver name: {static[1].Driver}')

                try:
                    getattr(instruments, fam)
                except AttributeError:
                    setattr(instruments, fam, [])
                finally:
                    getattr(instruments, fam).append(driver)

    # pprint(resources)

    registers = {}
    for reg in [x for x in labtoolkit.__all__ if rgetattr(labtoolkit, f'{x}.REGISTER')]:
        di = rgetattr(labtoolkit, f'{reg}.REGISTER')
        for i in di:
            registers.update({i: {'Family': reg, 'Driver': di[i]}})
    # pprint(registers)

    for resource in resources:

        inst = rm.open_resource(
            resource,
            read_termination='\n',
            write_termination='\r\n' if resource.startswith('ASRL') else '\n'
        )
        try:
            response = inst.query('*IDN?')
            # print(response)
        except VisaIOError:
            print(resource)
        # pprint(response)
        if ',' in response:
            make, model, *_ = response.replace(', ', ',').split(',')
            response = f'{make},{model}'
            if response in registers.keys():
                # print(registers[response])
                # resources.remove(resource)
                driver = registers[response]['Driver'](inst)
                fam = registers[response]['Family']
                try:
                    getattr(instruments, fam)
                except AttributeError:
                    setattr(instruments, fam, [])
                finally:
                    getattr(instruments, fam).append(driver)
            else:
                print(f'{response} not a known instrument')
        else:
            inst.close()
            print(f'{response} response string not typical from {resource}')
    # pprint(instruments.__dict__)
    return instruments
