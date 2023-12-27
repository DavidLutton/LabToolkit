from .HPGreenScreen import HPGreenScreen
import numpy as np


class AnritsuMS266nC(HPGreenScreen):
    ...

    def trace(self):
        self.write('BIN 0')  # ASCII
        match self.frequency_span:

            case 0.0:
                y = self.query_ascii_values(f'XMT? {0},{500}', container=np.array) / 100

                x = np.linspace(0, self.sweep_time, len(y))
                columns = ['Time (s)', 'dBm']  # TODO Unit Power

            case _:
                y = self.query_ascii_values(f'XMA? {0},{500}', container=np.array) / 100

                x = np.linspace(self.frequency_start, self.frequency_stop, len(y))
                columns = ['Frequency (Hz)', 'dBm']  # TODO Unit Power

        return pd.DataFrame(
            np.column_stack((x, y)),
            columns=columns,
        ).set_index(columns[0])