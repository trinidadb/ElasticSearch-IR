import matplotlib.pyplot as plt
import pandas as pd
from evaluate import EvaluatorAll, EvaluatorByQuery
import mplcursors

resultsAll = EvaluatorAll()
resultsByQuery = EvaluatorByQuery(firstSortByQuery=True)
resultsByRunId = EvaluatorByQuery(firstSortByQuery=False)

class Plot():
 
    def __init__(self, metrics):
        self.metrics = metrics

    def showTable(self):
        otherMetrics = self.metrics.drop(columns=[col for col in self.metrics.columns if col.startswith(('P_', 'iprec_'))])
        print(otherMetrics)

    def plotByRunID(self):
        #self.metrics.reset_index(inplace=True)
        #self.metrics = self.metrics[self.metrics['runId'] == 'base']
        runIds = self.metrics.index.get_level_values('runId').unique()
        for runId in runIds:
            self.metrics = self.metrics.loc[self.metrics.index.get_level_values('runId') == runId]
            # Assuming df is your DataFrame with a multi-level index
            self.metrics.reset_index(level='runId', drop=True, inplace=True)
            self.plotIPrecAtRecall(runId=runId)

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

    def plotIPrecAtRecall(self, runId="all"):
        iPrecisionTable = self.metrics.filter(regex='^iprec_')
        colRename = {col:float(col[-4:]) for col in iPrecisionTable.columns}
        iPrecisionTable = iPrecisionTable.rename(columns=colRename)
        iPrecisionTable = iPrecisionTable.sort_index(axis=1)
        iPrecisionTable = iPrecisionTable.astype(float)

        custom_colors = ['blue', 'green', 'red', 'orange', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan',
                        'navy', 'lime', 'maroon', 'gold', 'indigo', 'sienna', 'magenta', 'dimgray', 'olivedrab', 'darkcyan',
                        'lightsteelblue', 'limegreen', 'tomato', 'khaki', 'violet']

        # Transpose and plot with custom color palette
        ax = iPrecisionTable.T.plot(figsize=(7, 6), color=custom_colors)
        ax.set_ylabel('IPrecision', fontsize=12)
        ax.set_xlabel('Recall', fontsize=12)
        ax.set_title(f"IPrecision VS Recall for {runId} index")
        plt.legend(title=self.metrics.index.names[0], fontsize=7)

        mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(sel.artist.get_label()))

        plt.show()     


#Plot(resultsAll.results).plotIPrecAtRecall()
        
Plot(resultsByRunId.results).plotByRunID()