import argparse
import matplotlib.pyplot as plt
import pandas as pd
from experiments.common import RESULTS_DATA, RESULTS_FIGURES

def performance(prefix):
 d=pd.read_csv(RESULTS_DATA/f'{prefix}_performance.csv'); plt.figure(); plt.plot(d.sample_size,d.insert_seconds_mean,marker='o',label='Insert'); plt.plot(d.sample_size,d.present_query_seconds_mean,marker='o',label='Query inserted'); plt.plot(d.sample_size,d.absent_query_seconds_mean,marker='o',label='Query absent'); plt.xlabel('Number of items'); plt.ylabel('Mean runtime (seconds)'); plt.title('Bloom filter runtime'); plt.legend(); plt.tight_layout(); plt.savefig(RESULTS_FIGURES/f'{prefix}_performance.png',dpi=200); plt.close()
def false_positive(prefix):
 d=pd.read_csv(RESULTS_DATA/f'{prefix}_false_positive_rate.csv'); plt.figure(); plt.plot(d.load_factor,d.observed_false_positive_rate,marker='o',label='Observed'); plt.plot(d.load_factor,d.estimated_false_positive_rate,marker='o',label='Estimated'); plt.xlabel('Inserted items / expected items'); plt.ylabel('False-positive rate'); plt.title('False-positive rate as filter fills'); plt.legend(); plt.tight_layout(); plt.savefig(RESULTS_FIGURES/f'{prefix}_false_positive_rate.png',dpi=200); plt.close()
def compression(prefix):
 d=pd.read_csv(RESULTS_DATA/f'{prefix}_compression_rate.csv'); plt.figure();
 for n,g in d.groupby('expected_items'):
  g=g.sort_values('target_false_positive_rate'); plt.plot(g.target_false_positive_rate,g.compression_ratio_raw_divided_by_bloom,marker='o',label=f'n={n}')
 plt.xscale('log'); plt.xlabel('Target false-positive rate'); plt.ylabel('Raw bytes / Bloom bytes'); plt.title('Compression ratio'); plt.legend(); plt.tight_layout(); plt.savefig(RESULTS_FIGURES/f'{prefix}_compression_rate.png',dpi=200); plt.close()
def hash_distribution(prefix):
 d=pd.read_csv(RESULTS_DATA/f'{prefix}_hash_distribution.csv'); plt.figure();
 for typ,g in d.groupby('data_type'): plt.plot(g.bucket,g['count'],marker='o',label=typ)
 plt.xlabel('Bucket'); plt.ylabel('Count'); plt.title('Hash-position bucket distribution'); plt.legend(); plt.tight_layout(); plt.savefig(RESULTS_FIGURES/f'{prefix}_hash_distribution.png',dpi=200); plt.close()
if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('--prefix',default='hpc'); a=p.parse_args(); performance(a.prefix); false_positive(a.prefix); compression(a.prefix); hash_distribution(a.prefix); print('Wrote plots')
