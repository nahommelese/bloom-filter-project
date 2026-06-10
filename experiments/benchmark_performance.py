import argparse,csv,statistics,time
from pathlib import Path
from bloom_filter import BloomFilter
from experiments.common import RESULTS_DATA, generate_words

def timed(fn):
    start=time.perf_counter(); fn(); return time.perf_counter()-start

def parse_sizes(raw): return [int(x) for x in raw.split(',') if x.strip()]
def run_benchmark(sizes,fpr,repeats,output):
    rows=[]
    for size in sizes:
        inserted=generate_words(size,100+size); absent=generate_words(size,200+size)
        ins=[]; present=[]; missing=[]
        for _ in range(repeats):
            bloom=BloomFilter(size,fpr)
            ins.append(timed(lambda: bloom.update(inserted)))
            present.append(timed(lambda: [x in bloom for x in inserted]))
            missing.append(timed(lambda: [x in bloom for x in absent]))
        rows.append({'sample_size':size,'target_false_positive_rate':fpr,'repeats':repeats,
                     'insert_seconds_mean':statistics.mean(ins),'insert_seconds_stdev':statistics.stdev(ins) if repeats>1 else 0.0,
                     'present_query_seconds_mean':statistics.mean(present),'absent_query_seconds_mean':statistics.mean(missing),
                     'bit_count':bloom.bit_count,'hash_count':bloom.hash_count,'memory_bytes':bloom.memory_bytes})
    with output.open('w',newline='',encoding='utf-8') as h:
        w=csv.DictWriter(h,fieldnames=rows[0]); w.writeheader(); w.writerows(rows)
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--sizes',default='1000,5000,10000,50000,100000,250000'); p.add_argument('--false-positive-rate',type=float,default=0.01); p.add_argument('--repeats',type=int,default=5); p.add_argument('--output',type=Path,default=RESULTS_DATA/'hpc_performance.csv'); a=p.parse_args(); run_benchmark(parse_sizes(a.sizes),a.false_positive_rate,a.repeats,a.output); print('Wrote',a.output)
