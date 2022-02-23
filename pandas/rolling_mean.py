import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from numpy import NaN

is_ipython = 'inline' in matplotlib.get_backend()
if is_ipython:
    from IPython import display


def plot_single_with_mean(config):
    '''
    config: {
        'id': unique identifier,
        'title': '',
        'xlabel': '',
        'ylabel': '',
        'x_data': [],
        'y_data': [],
        'm': int
    }
    '''
    fig = plt.figure(config['id'])
    axes = fig.get_axes()
    _data = config['y_data']
    m = config['m']
    if m > 0 and len(_data) > m:
        means = pd.Series(_data).rolling(m).mean()
        print(len(_data), len(means))
    else:
        means = [NaN] * len(_data)
    if len(axes) == 0:
        plt.title(config['title'])
        plt.xlabel(config['xlabel'])
        plt.plot(config['x_data'], config['y_data'], label=config['ylabel'])
        plt.plot(config['x_data'], means, label=config['ylabel'] + '_mean')
    else:
        ax = axes[0]
        line, meanline = ax.get_lines()
        line.set_xdata(config['x_data'])
        line.set_ydata(config['y_data'])
        meanline.set_xdata(config['x_data'])
        meanline.set_ydata(means)
        ax.relim()
        ax.autoscale_view(True, True, True)
    if is_ipython:
        display.clear_output(wait=True)
        display.display(fig)
    else:
        plt.pause(0.2)  # pause a bit so that plots are updated
    return axes


config = {
    'id': 2,
    'title': 'single_with_mean',
    'xlabel': 't',
    'ylabel': 'l1',
    'x_data': range(5),
    'y_data': [1, 3, 6, 7, 9],
    "m": 3
}
plot_single_with_mean(config)
plt.show(block=True)
