import os
import json
import shutil

import pysam
from glob import glob
import cellranger_utils.utils as utils


def find_gex_id(bam_file):
    with pysam.AlignmentFile(bam_file, 'rb') as reader:
        header = reader.header

    for comment in header['CO']:
        if not comment.startswith('library_info'):
            continue

        comment = comment[len('library_info:'):]
        comment = json.loads(comment)

        print(comment)

        if comment['library_type'] == 'Gene Expression':
            return comment['library_id'], comment['gem_group']

    raise Exception()


def find_fastqs_to_use(tempdir, library_id, gem_group):
    files = glob(f'{tempdir}/*_{library_id}_{gem_group}*')

    assert len(set([os.path.basename(v) for v in files])) == len(files)

    return files


def find_metrics_cellranger(cellranger_dir):
    metrics = f'{cellranger_dir}/metrics_summary.csv'
    assert os.path.exists(metrics), metrics
    return metrics


def find_bam_cellranger(cellranger_dir):
    bam_file = f'{cellranger_dir}/count/sample_alignments.bam'
    assert os.path.exists(bam_file), bam_file
    return bam_file


def run_bam_to_fastq(cellranger_dir, outdir, tempdir):
    utils.makedirs(outdir)
    utils.makedirs(os.path.join(outdir, 'fastqs'))

    metrics = find_metrics_cellranger(cellranger_dir)
    bam_file = find_bam_cellranger(cellranger_dir)

    num_reads, num_cells = utils.read_metrics(metrics)

    library_id, gem_group = find_gex_id(bam_file)

    cmd = ['bamtofastq', f'--reads-per-fastq={num_reads + 1000000}', bam_file, tempdir]

    utils.run_cmd(cmd)

    fastqs = find_fastqs_to_use(tempdir, library_id, gem_group)

    for fastq in fastqs:
        os.rename(fastq, os.path.join(outdir, 'fastqs', os.path.basename(fastq)))

    shutil.copyfile(metrics, os.path.join(outdir, 'metrics.csv'))
