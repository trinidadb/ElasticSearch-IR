import matplotlib.pyplot as plt
import pandas as pd
from evaluate import EvaluatorAll, EvaluatorByQuery
import mplcursors
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


resultsAll = EvaluatorAll()
resultsByQuery = EvaluatorByQuery(firstSortByQuery=True)
resultsByRunId = EvaluatorByQuery(firstSortByQuery=False)

class Plot():
 
    def __init__(self, metrics):
        self.metrics = metrics

    def showTable(self):
        otherMetrics = self.metrics.drop(columns=[col for col in self.metrics.columns if col.startswith(('P_', 'iprec_'))])
        print(otherMetrics)

    def plotExtended(self, byRunId=False, iprecCurve=True):
        key = "runId" if byRunId else "queryId"
        ids = self.metrics.index.get_level_values(key).unique()

        nRows = 2 if byRunId else 5
        nCols = 2 if byRunId else 5

        fig, axs = plt.subplots(nRows, nCols, figsize=(50, 50), constrained_layout=True)
        axs = axs.flatten()

        for i, id in enumerate(ids):
            metricsToPlot = self.metrics.loc[self.metrics.index.get_level_values(key) == id]
            metricsToPlot.reset_index(level=key, drop=True, inplace=True)
            if iprecCurve:
                self.plotIPrecAtRecall(metrics=metricsToPlot, id=id, customAx=axs[i])
            else:
                self.plotRPrecision(metrics=metricsToPlot, id=id, customAx=axs[i])
            handles, labels = axs[i].get_legend_handles_labels()
            axs[i].get_legend().remove()

        fig.legend(handles, labels, loc='center right', title="QueryId" if byRunId else "RunId", fontsize=9)
        fig.supxlabel("Recall")
        fig.supylabel("IPrecision")
        fig.suptitle(f"Interpolated Precison VS Recall Curve {'By Index' if byRunId else 'By Query'}")

        plt.show()

    def plotRPrecision(self):
        precisionTable = self.metrics.filter(regex='^P_')
        precisionTable = precisionTable.rename(columns={'P_5': 5, 'P_10': 10, 'P_15': 15, 'P_20': 20, 'P_30': 30, 'P_100': 100, 'P_200': 200, 'P_500': 500, 'P_1000': 1000})
        precisionTable.sort_index(axis=1, inplace=True)
        precisionTable = precisionTable.astype(float)

        # transpose and plot
        ax = precisionTable.T.plot(figsize=(7, 6))
        ax.set_ylabel('Precision', fontsize=12)
        ax.set_xlabel('Number of Documents', fontsize=12)
        ax.set_title("Precision at different cut-off points")
        plt.show()

    def plotIPrecAtRecall(self, metrics=None, id="all", customAx=None):
        if metrics is None:
            metrics = self.metrics
        iPrecisionTable = metrics.filter(regex='^iprec_')
        colRename = {col:float(col[-4:]) for col in iPrecisionTable.columns}
        iPrecisionTable = iPrecisionTable.rename(columns=colRename)
        iPrecisionTable = iPrecisionTable.sort_index(axis=1)
        iPrecisionTable = iPrecisionTable.astype(float)

        custom_colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan',
                        'navy', 'lime', 'maroon', 'gold', 'indigo', 'sienna', 'magenta', 'dimgray', 'olivedrab', 'darkcyan',
                        'lightsteelblue', 'limegreen', 'tomato', 'khaki', 'violet']

        # Transpose and plot with custom color palette
        ax = customAx if customAx else plt.gca()
        iPrecisionTable.T.plot(ax=ax, figsize=(7, 6), color=custom_colors)

        mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(sel.artist.get_label()))

        if customAx:
            ax.set_xlabel('')
            ax.set_title(f"{id}", fontsize=10)

        else:
            ax.set_ylabel('IPrecision', fontsize=12)
            ax.set_xlabel('Recall', fontsize=12)
            ax.set_title(f"Interpolated Precison VS Recall Curve By Index")
            plt.legend(title=metrics.index.names[0], fontsize=7)
            plt.show() 


#Plot(resultsAll.results).plotIPrecAtRecall()
        
Plot(resultsByRunId.results).plotExtended()