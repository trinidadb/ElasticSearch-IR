import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from constants import INDEX_NAMES

class Evaluate():

    def evalAllIndexes(self):
        metrics=pd.DataFrame()
        for index_name in INDEX_NAMES:
            aux = self.run_trec_eval(index_name)
            metrics = pd.concat([metrics, aux], ignore_index=True)

        # Usamos pivot para transformar el DataFrame
        metrics = metrics.pivot(index='runId', columns='metric', values='value')
        return metrics

    def run_trec_eval(self, index_name, trec_rel_file="qrels.txt"):
        # Build the command
        trec_top_file = index_name + ".txt"
        command = f"trec_eval.exe {trec_rel_file} {trec_top_file}"

        try:
            # Run the command and capture the output
            result = subprocess.run(command, stdout=subprocess.PIPE, text=True, check=True)
            output = result.stdout
            return self._parseOutput(output, index_name)
        except subprocess.CalledProcessError as e:
            raise Exception(f"Error running trec_eval: {e}")
        
    def _parseOutput(self, output, index_name):
        metrics = output.strip().split('\n')
        data = [metric.split() for metric in metrics[2::]]
        
        df = pd.DataFrame(data, columns=['metric', 'toBeRemoved', 'value'])
        df.drop(columns=['toBeRemoved'], inplace=True)
        df['runId'] = index_name
        return df
    

class Plot():
 
    def __init__(self, metrics):
        self.metrics = metrics

    def showTable(self):
        otherMetrics = self.metrics.drop(columns=[col for col in self.metrics.columns if col.startswith(('P_', 'iprec_'))])
        print(otherMetrics)

    def plotRPrecision(self):
        precisionTable = self.metrics.filter(regex='^P_')

        precisionTable.rename(columns={'P_5': 5, 'P_10': 10, 'P_15': 15, 'P_20': 20, 'P_30': 30, 'P_100': 100, 'P_200': 200, 'P_500': 500, 'P_1000': 1000}, inplace=True)
        precisionTable.sort_index(axis=1, inplace=True)
        precisionTable = precisionTable.astype(float)


        # transpose and plot
        ax = precisionTable.T.plot(figsize=(7, 6))
        ax.set_ylabel('Precision', fontsize=12)
        ax.set_xlabel('Number of Documents', fontsize=12)
        #ax.title("Precision at different cut-off points")
        #plt.show()

    def plotIPrecAtRecall(self):
        iPrecisionTable = self.metrics.filter(regex='^iprec_')

        colRename = {col:float(col[-4:]) for col in iPrecisionTable.columns}
        iPrecisionTable.rename(columns=colRename, inplace=True)
        iPrecisionTable.sort_index(axis=1, inplace=True)
        iPrecisionTable = iPrecisionTable.astype(float)

        # transpose and plot
        ax = iPrecisionTable.T.plot(figsize=(7, 6))
        ax.set_ylabel('IPrecision', fontsize=12)
        ax.set_xlabel('Recall', fontsize=12)
        #ax.title("Precision VS Recall")
        plt.show()        


metrics = Evaluate().evalAllIndexes()
Plot(metrics).showTable()