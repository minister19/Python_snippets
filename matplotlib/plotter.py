import matplotlib
import matplotlib.pyplot as plt


class Plotter():
    def __init__(self):
        plt.ion()  # set up matplotlib

    def plot_single(self, config):
        '''
        config: {
            id: unique identifier,
            title: '',
            xlabel: '',
            ylabel: '',
            x_data: [],
            y_data: []
        }
        '''
        fig = plt.figure(config['id'])
        axes = fig.get_axes()
        if len(axes) == 0:
            plt.title(config['title'])
            plt.xlabel(config['xlabel'])
            plt.plot(config['x_data'], config['y_data'], label=config['ylabel'])
        else:
            ax = axes[0]
            line, = ax.get_lines()
            line.set_xdata(config['x_data'])
            line.set_ydata(config['y_data'])
            ax.relim()
            ax.autoscale_view(True, True, True)
        plt.pause(0.1)  # pause a bit so that plots are updated

    def plot_multiple(self, config):
        '''
        configs: {
            id: unique identifier,
            title: '',
            xlabel: '',
            ylabel: [''],
            x_data: [[]],
            y_data: [[]]
        }
        '''
        fig = plt.figure(config['id'])
        axes = fig.get_axes()
        if len(axes) == 0:
            plt.title(config['title'])
            plt.xlabel(config['xlabel'])
            for i in range(len(config['ylabel'])):
                if i == 0:
                    plt.plot(config['x_data'][i], config['y_data'][i], label=config['ylabel'][i])
                    axes = fig.get_axes()
                    ax = axes[0]
                else:
                    twin = ax.twinx()
                    if i >= 2:
                        fig.subplots_adjust(right=1.0 - 0.25*(i-1))
                        twin.spines.right.set_position(("axes", 1.0 + 0.2*(i-1)))
                    twin.plot(config['x_data'][i], config['y_data'][i], label=config['ylabel'][i])
        else:
            for i in range(len(config['ylabel'])):
                ax = axes[i]
                line, = ax.get_lines()
                line.set_xdata(config['x_data'][i])
                line.set_ydata(config['y_data'][i])
                ax.relim()
                ax.autoscale_view(True, True, True)
        plt.pause(0.1)  # pause a bit so that plots are updated


p = Plotter()
line = p.plot_single({
    'id': 1,
    'title': 'single_line',
    'xlabel': 't',
    'ylabel': 'l1',
    'x_data': range(4),
    'y_data': [1, 2, 3, 4]
})
plt.pause(1)
p.plot_single({
    'id': 1,
    'title': 'single_line',
    'xlabel': 't',
    'ylabel': 'l1',
    'x_data': range(5),
    'y_data': [1, 2, 3, 5, 8],
})

p.plot_multiple({
    'id': 2,
    'title': 'multiple_lines',
    'xlabel': 't',
    'ylabel': ['l1', 'l2'],
    'x_data': [range(4), range(5)],
    'y_data': [[1, 2, 3, 4], [1, 2, 3, 5, 8]],
})
plt.pause(1)
p.plot_multiple({
    'id': 2,
    'title': 'multiple_lines',
    'xlabel': 't',
    'ylabel': ['l1', 'l2'],
    'x_data': [range(5), range(6)],
    'y_data': [[1, 2, 3, 4, 5], [1, 2, 3, 5, 8, 13]],
})
plt.show(block=True)
