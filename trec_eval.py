import subprocess
import pandas as pd
import matplotlib.pyplot as plt
from constants import INDEX_NAMES

class Evaluate():

    def __init__(self):
        self.metrics = self.evalAllIndexes()
        self.plotCharts()

    def evalAllIndexes(self):
        metrics=pd.DataFrame()
        for index_name in INDEX_NAMES:
            aux = self.run_trec_eval(index_name)
            metrics = pd.concat([metrics, aux], ignore_index=True)

        # Usamos pivot para transformar el DataFrame
        metrics = metrics.pivot(index='runId', columns='metric', values='value')
        return metrics
    
    def plotCharts(self):
        precision = self.metrics.filter(regex='^P_')
        iPrecision = self.metrics.filter(regex='^iprec_')

        print(precision)

        precision.rename(columns={'P_5': 5, 'P_10': 10, 'P_15': 15, 'P_20': 20, 'P_30': 30, 'P_100': 100, 'P_200': 200, 'P_500': 500, 'P_1000': 1000}, inplace=True)
        precision.sort_index(axis=1, inplace=True)

        precision = precision.astype(float)

        print(precision.T)

        # transpose and plot
        ax = precision.T.plot(figsize=(7, 6))
        ax.set_ylabel('Absolute Power (log)', fontsize=12)
        ax.set_xlabel('Frequencies', fontsize=12)
        plt.show()

        # plt.figure(figsize=(10, 6))
        # for runId, row in precision.iterrows():
        #     plt.plot(row.index, row.values, label=runId)

        # # Configura etiquetas y leyenda
        # plt.xlabel('Número de Documentos')
        # plt.ylabel('Precisión')
        # plt.title('Métricas de Precisión')
        # plt.legend()

        # # Muestra el gráfico
        # plt.show()
    
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

Evaluate().evalAllIndexes()

def process_trec_eval_results(output):
    # Separate P and iprec metrics for plotting
    p_metrics, iprec_metrics, other_metrics = parse_metrics(output)

    # Plot P metrics
    plot_precision_metrics(p_metrics)

    # Create a table for other metrics
    create_metrics_table(other_metrics)

def parse_metrics(output):
    lines = output.strip().split('\n')
    header = lines[0].split()
    data = [line.split() for line in lines[1:]]
    
    df = pd.DataFrame(data, columns=['metric', 'all', 'value'])
    df.drop(columns=['all'], inplace=True)

    print(df)
    
    # Separate P and iprec metrics
    p_metrics = df[df['metric'].str.startswith('P_')]
    iprec_metrics = df[df['metric'].str.startswith('iprec_at_recall')]
    
    # Other metrics
    other_metrics = df[~df['metric'].isin(p_metrics['metric']) & ~df['metric'].isin(iprec_metrics['metric'])]
    
    return p_metrics, iprec_metrics, other_metrics

def plot_precision_metrics(p_metrics):
    plt.figure(figsize=(10, 6))
    for group in p_metrics:
        plt.plot(group['metric'], group['value'])
    plt.title('Precision Metrics (P@K)')
    plt.xlabel('K (Number of Documents)')
    plt.ylabel('Precision')
    plt.legend()
    plt.show()

def create_metrics_table(other_metrics):
    print("Metrics Table:")
    print(other_metrics)
