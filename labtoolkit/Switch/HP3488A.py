from ..GenericInstrument import GenericInstrument
from ..IEEE488 import IEEE488
from ..SCPI import SCPI

import pandas as pd


class Switch:

    def load_switchpath(self, switchpaths):
        df = pd.read_excel(switchpaths, sheet_name='Data').dropna(how='all')
        df = df.astype({'Path': 'category', 'Requires': 'category', 'Switch': 'int', 'State': 'bool'})

        # rearrange requires as extras steps for paths that call for it
        for switch_path in set(df[df['Requires'].notna()]['Path']):
            frame = df[df['Path'] == switch_path]
            req = df[df['Path'] == list(set(frame.Requires))[0]]
            for values in req.iterrows():
                res = {'Path': str(switch_path), 'Switch': int(values[1].Switch), 'State': bool(values[1].State)}
                # print(res)
                df = df.append(res, ignore_index=True)

        df = df.drop(columns=['Requires'])
        self._switchpaths = df

    @property
    def switchpath(self):
        return list(set(self._switchpaths.Path))

    @switchpath.setter
    def switchpath(self, path):
        for route in self._switchpaths[self._switchpaths['Path'] == path].iterrows():
            self.switch(route[1].Switch, route[1].State)


class HP3488A(GenericInstrument, Switch):

    def __post__(self):
        self.inst.read_termination = '\r\n'
        self.inst.write_termination = '\n'
    # switcher.switch(502, True)
    # switcher.read(502), switcher.readtext(502)
    # buffer = {}
    # for sw in 100, 101, 102:
    #    buffer[sw] = switcher.read(sw)
    #    print(f"{sw} {switcher.read(sw)}, {switcher.readtext(sw)}")
    # buffer

    # query(f'CTYPE {1}'), query(f'CTYPE {2}'), query(f'CTYPE {3}'), query(f'CTYPE {4}'), query(f'CTYPE {5}')
    # CRESET 1
    # query(f'CMON {4}')

    def switch(self, switch, state):
        if state in ['OPEN', False]:
            self.write(f'OPEN {switch}')

        if state in ['CLOSE', True]:
            self.write(f'CLOSE {switch}')

    def viewtext(self, switch):
        return self.query(f'VIEW {switch}').split(' ')[0]  # 'CLOSED 0', 'OPEN 1'

    def view(self, switch):
        # 'CLOSED 0', 'OPEN 1'
        if int(self.query(f'VIEW {switch}').split(' ')[-1]) == 1:
            return bool(False)
        else:
            return bool(True)

    def cards(self):
        return self.query(f'CTYPE {1}'), self.query(f'CTYPE {2}'), self.query(f'CTYPE {3}'), self.query(f'CTYPE {4}'), self.query(f'CTYPE {5}')

    def switches(self):
        switches = []
        for index, card in enumerate(self.cards(), 1):
            card = card.split(' ')[-1]
            # print(f'{index}, {card}')
            # print(cards[card])
            if card == '44471':
                for dex in [0, 1, 2]:
                    switches.append(f'{index}0{dex}')
                    # print(f'{index}0{dex}')
            if card == '44472':
                for segment in [0, 1]:
                    for dex in [0, 1, 2, 3]:
                        switches.append(f'{index}{segment}{dex}')
                        # print(f'{index}{segment}{dex}')
        return switches

    def state(self):
        buffer = {}
        for sw in self.switches():
            buffer[sw] = self.view(sw)
            # print(f"{sw} {buffer[sw]}")
        return buffer
