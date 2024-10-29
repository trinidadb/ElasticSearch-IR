import subprocess
import os
import pandas as pd

from constants import INDEX_NAMES, SEARCH_RESULTS_DIR

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

    def _run_trec_eval(self, index_name, trec_rel_file="files/qrels.txt"):
        trec_top_file = SEARCH_RESULTS_DIR+index_name + ".txt"
        command = f"{os.path.join(os.getcwd(), 'evaluation-tool', 'trec_eval.exe')} {'-q ' if self.byQuery else ''}{trec_rel_file} {trec_top_file}"

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
        self.results = self.evalIndexesSortByQueryId() if firstSortByQuery else self.evalIndexesSortByRunId()
