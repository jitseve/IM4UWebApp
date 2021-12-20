import base64
from matplotlib.figure import Figure
from io import BytesIO

class DataPlot(object):

    def __init__(self):
        super().__init__()

        self.colors = ( (0.61176, 0.04314, 0.95686),                    # Purple
                        (0.00000, 0.00000, 0.00000),                    # Black
                        (0.48235, 0.82745, 0.53725),                    # Emerald
                        (0.37255, 0.65882, 0.82745),                    # Carolina Blue
                        (0.05098, 0.12941, 0.63137),                    # Blue Pantone
                        (0.24706, 0.05098, 0.07059))                    # Dark Sienna

        self.marker = ('o' , 'v', 'x', '+', 'd')                        # Some markers

        return

    def img1by1(self, x, y, lab='', fig=None, line=True,
                color=0, marker=0, ylab='', xlab='', title='', 
                xlim=None, ylim=None, bgr=('#808080') ):
            
        fig = Figure()
        ax = fig.subplots()

        if line is True:
            ax.plot(x, y, color=self.colors[color % 6],
                    linestyle='-', label=lab)
        else:
            ax.plot(x, y, marker=self.marker[marker % 5],
                    linestyle='None', markersize=8, markerfacecolor=('#ffffff'),
                    markeredgecolor=self.colors[color % 6], markeredgewidth=3)

        #FORMAT
        ax.set_title(title,fontsize=20)
        ax.set_ylabel(ylab)
        ax.set_xlabel(xlab)
        ax.grid()

        if xlim is not None:
            ax.set_xlim(xlim)
        if ylim is not None:
            ax.set_ylim(ylim)

        ax.set_facecolor(bgr)

        buf = BytesIO()
        fig.savefig(buf, format="png")
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return f'data:image/png;base64,{data}'