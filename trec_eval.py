import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from constants import INDEX_NAMES

class Evaluate():

    def __init__(self, byQuery):
        self.byQuery = byQuery

    def evalAllIndexes(self):
        return self._evalIndexes('runId')
    
    def evalIndexesSortByQueryId(self):
        return self._evalIndexes(['queryId', 'runId'])
    
    def evalIndexesSortByRunId(self):
        return self._evalIndexes(['runId', 'queryId'])
    
    def _evalIndexes(self, indexBy):
        metrics=pd.DataFrame()
        for index_name in INDEX_NAMES:
            aux = self._run_trec_eval(index_name)
            metrics = pd.concat([metrics, aux], ignore_index=True)

        metrics = metrics[metrics['queryId'] != 'all'] if self.byQuery else metrics
        metrics = metrics.pivot(index=indexBy, columns='metric', values='value')
        return metrics

    def _run_trec_eval(self, index_name, trec_rel_file="qrels.txt"):
        trec_top_file = index_name + ".txt"
        command = f"trec_eval.exe {'-q ' if self.byQuery else ''}{trec_rel_file} {trec_top_file}"

        try:
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=True)
            output = result.stdout
            return self._parseOutput(output, index_name)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error running trec_eval: {e}")
        
    def _parseOutput(self, output, index_name):
        metrics = output.strip().split('\n')
        data = [metric.split() for metric in (metrics if self.byQuery else metrics[2::])]
        
        df = pd.DataFrame(data, columns=['metric', 'queryId', 'value'])
        df['runId'] = index_name
        return df

class EvaluatorAll(Evaluate):
    def __init__(self):
        super().__init__(False)
        self.results = self.evalAllIndexes()

class EvaluatorByQuery(Evaluate):
    def __init__(self, firstSortByQuery=True):
        super().__init__(True)
        self.results = self.evalIndexesSortByQueryId if firstSortByQuery else self.evalIndexesSortByRunId

class Plot():
 
    def __init__(self, metrics):
        self.metrics = metrics

    def showTable(self):
        otherMetrics = self.metrics.drop(columns=[col for col in self.metrics.columns if col.startswith(('P_', 'iprec_'))])
        print(otherMetrics)

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

    def plotIPrecAtRecall(self):
        iPrecisionTable = self.metrics.filter(regex='^iprec_')
        colRename = {col:float(col[-4:]) for col in iPrecisionTable.columns}
        iPrecisionTable = iPrecisionTable.rename(columns=colRename)
        iPrecisionTable = iPrecisionTable.sort_index(axis=1)
        iPrecisionTable = iPrecisionTable.astype(float)

        # transpose and plot
        ax = iPrecisionTable.T.plot(figsize=(7, 6))
        ax.set_ylabel('IPrecision', fontsize=12)
        ax.set_xlabel('Recall', fontsize=12)
        ax.set_title("IPrecision VS Recall")
        plt.show()        

resultsAll = EvaluatorAll()
resultsByQuery = EvaluatorByQuery(firstSortByQuery=True)
resultsByQuery = EvaluatorByQuery(firstSortByQuery=False)

Plot(resultsAll.results).plotIPrecAtRecall()