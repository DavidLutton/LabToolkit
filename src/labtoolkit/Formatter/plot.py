import matplotlib.pyplot as plt
from matplotlib.ticker import EngFormatter
import numpy as np


def plot_add_minor_min_max_labels(ax):
    lo = np.inf
    hi = -np.inf 
    for xl in ax.get_lines():  # https://stackoverflow.com/a/20131383
        xtrace = xl.get_xdata()
        elo, ehi = np.amin(xtrace), np.amax(xtrace)
        if elo < lo:
            lo = elo
        if ehi > hi:
            hi = ehi
    xticks = np.unique(np.clip(ax.get_xticks(minor=True), lo, hi))
    key_xticks = np.array([lo, hi])
    ax.set_xticks(xticks, minor=True)
    
    for label in ax.get_xticklabels(which='minor'):
        if label._x not in key_xticks:
            label.set_visible(False)

    if 9e3 in key_xticks:
        for label in ax.get_xticklabels(which='major'):
            if label._x == 10e3:
                label.set_visible(False)
        
    return label

if __name__ == '__main__':
    plt.rcdefaults()  # Restore the rcParams from Matplotlib's internal default style.
    
    # plt.rcParams['figure.figsize'] = (15, 10)
    # plt.rcParams['figure.figsize'] = (24, 8)
    # plt.rcParams['figure.dpi'] = 200
    plt.rcParams['figure.autolayout'] = True
    plt.rcParams['axes.xmargin'] = 0.005
    plt.rcParams['axes.ymargin'] = 0.025
    plt.rcParams['axes.linewidth'] = 1
    plt.rcParams['figure.figsize'] = (16, 5)
    plt.rcParams['figure.dpi'] = 300
    plt.rcParams['axes.grid'] = True
    fig, ax = plt.subplots()
    
    ax.margins(x=1/200, y=1/20)
    # plt.ylim(-extremes, extremes)
    ax.grid()
    ax.set_xscale('log')
    # plt.plot([150e3, 230e6], [7.1, 7.1], label='Limit', color='green')
    ax.plot([9e3, 30e6], [3.1, 3.1], label='Limit', color='green')
    la = plot_add_minor_min_max_labels(ax)
    ax.legend()
    
    
    ax.xaxis.set_major_formatter(EngFormatter(unit='Hz', sep=" "))
    ax.xaxis.set_minor_formatter(EngFormatter(unit='Hz', sep=" "))
    ax.tick_params(axis='x', labelrotation=0, which='both')
    # plt.grid(True, which="both")
    ax.grid('x', which='major', linestyle='-', linewidth=plt.rcParams['axes.linewidth'] * 1.75)
    ax.grid('x', which='minor', linestyle='--')
    # ax.set_title(f'{c.stem}')
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('dB')
    # dest = c.parent / f'{c.stem}.png'
    #if not dest.exists():
    #    plt.savefig(dest)
    #    co.to_excel(c.parent / f'{c.stem}.xlsx', 'Data')
    
    plt.show()
    plt.close()
