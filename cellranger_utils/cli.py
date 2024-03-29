"""Console script for cellranger utils"""
import yaml
import click
from cellranger_utils.cellranger_demultiplex import run_cellranger_demultiplex
from cellranger_utils.cellranger_non_multiplexed import run_cellranger_non_multiplexed
from cellranger_utils.cellranger_persample import run_cellranger_persample

from cellranger_utils.bamtofastq import run_bam_to_fastq


@click.group()
def cli():
    pass


@cli.command()
@click.option('--reference', required=True, help='CSV file path')
@click.option('--vdj_reference', help='CSV file path')
@click.option('--gex_fastq', required=True, help='cores for cellranger multi')
@click.option('--gex_id', required=True, help='cores for cellranger multi')
@click.option('--outdir', required=True, help='cores for cellranger multi')
@click.option('--meta_yaml', required=True, help='memory for cellranger multi')
@click.option('--tempdir', required=True, help='cores for cellranger multi')
@click.option('--sample_id', required=True, help='cores for cellranger multi')
@click.option('--tcr_fastq', help='cores for cellranger multi')
@click.option('--tcr_id', help='cores for cellranger multi')
@click.option('--cite_fastq', help='cores for cellranger multi')
@click.option('--cite_id', help='cores for cellranger multi')
@click.option('--bcr_fastq', help='cores for cellranger multi')
@click.option('--bcr_id', help='cores for cellranger multi')
@click.option('--numcores', default=16, help='cores for cellranger multi')
@click.option('--mempercore', default=10, help='cores for cellranger multi')
def cellranger_nonmultiplexed(
        reference,
        vdj_reference,
        gex_fastq,
        gex_id,
        outdir,
        meta_yaml,
        tempdir,
        sample_id,
        tcr_fastq=None,
        tcr_id=None,
        cite_fastq=None,
        cite_id=None,
        bcr_fastq=None,
        bcr_id=None,
        numcores=16,
        mempercore=10
):
    run_cellranger_non_multiplexed(
        reference,
        vdj_reference,
        gex_fastq,
        gex_id,
        outdir,
        meta_yaml,
        tempdir,
        sample_id,
        tcr_fastq=tcr_fastq,
        tcr_identifier=tcr_id,
        cite_fastq=cite_fastq,
        cite_identifier=cite_id,
        bcr_fastq=bcr_fastq,
        bcr_identifier=bcr_id,
        numcores=numcores,
        mempercore=mempercore
    )


@cli.command()
@click.option('--reference', required=True, help='CSV file path')
@click.option('--gex_fastq', required=True, help='cores for cellranger multi')
@click.option('--gex_id', required=True, help='cores for cellranger multi')
@click.option('--outdir', required=True, help='cores for cellranger multi')
@click.option('--meta_yaml', required=True, help='memory for cellranger multi')
@click.option('--tempdir', required=True, help='cores for cellranger multi')
@click.option('--sample_id', required=True, help='cores for cellranger multi')
@click.option('--cite_hto_fastq', help='cores for cellranger multi')
@click.option('--cite_hto_id', help='cores for cellranger multi')
@click.option('--numcores', default=16, help='cores for cellranger multi')
@click.option('--mempercore', default=10, help='cores for cellranger multi')
def cellranger_demultiplex(
        reference,
        gex_fastq,
        gex_id,
        outdir,
        meta_yaml,
        tempdir,
        sample_id,
        cite_hto_fastq=None,
        cite_hto_id=None,
        numcores=16,
        mempercore=10
):
    run_cellranger_demultiplex(
        reference,
        meta_yaml,
        gex_fastq,
        gex_id,
        cite_hto_fastq,
        cite_hto_id,
        sample_id,
        outdir,
        tempdir,
        numcores=numcores,
        mempercore=mempercore
    )


@cli.command()
@click.option('--reference', required=True, help='CSV file path')
@click.option('--vdj_reference', required=True, help='CSV file path')
@click.option('--gex_fastq', required=True, help='cores for cellranger multi')
@click.option('--gex_id', required=True, help='cores for cellranger multi')
@click.option('--gex_metrics', required=True, help='cores for cellranger multi')
@click.option('--output', required=True, help='cores for cellranger multi')
@click.option('--meta_yaml', required=True, help='CSV file path')
@click.option('--tempdir', required=True, help='cores for cellranger multi')
@click.option('--sample_id', required=True, help='cores for cellranger multi')
@click.option('--tcr_fastq', help='cores for cellranger multi')
@click.option('--tcr_id', help='cores for cellranger multi')
@click.option('--cite_hto_fastq', help='cores for cellranger multi')
@click.option('--cite_hto_id', help='cores for cellranger multi')
@click.option('--bcr_fastq', help='cores for cellranger multi')
@click.option('--bcr_id', help='cores for cellranger multi')
@click.option('--numcores', default=16, help='cores for cellranger multi')
@click.option('--mempercore', default=10, help='cores for cellranger multi')
def cellranger_persample(
        reference,
        vdj_reference,
        gex_fastq,
        gex_id,
        gex_metrics,
        output,
        meta_yaml,
        tempdir,
        sample_id,
        tcr_fastq=None,
        tcr_id=None,
        cite_hto_fastq=None,
        cite_hto_id=None,
        bcr_fastq=None,
        bcr_id=None,
        numcores=16,
        mempercore=10,
):
    run_cellranger_persample(
        reference,
        vdj_reference,
        gex_fastq,
        gex_id,
        gex_metrics,
        output,
        meta_yaml,
        tempdir,
        sample_id,
        tcr_fastq=tcr_fastq,
        tcr_identifier=tcr_id,
        cite_hto_fastq=cite_hto_fastq,
        cite_hto_identifier=cite_hto_id,
        bcr_fastq=bcr_fastq,
        bcr_identifier=bcr_id,
        numcores=numcores,
        mempercore=mempercore,
    )


@cli.command()
@click.option('--cellranger_demultiplex_dir', required=True, help='CSV file path')
@click.option('--outdir', required=True, help='CSV file path')
@click.option('--tempdir', required=True, help='CSV file path')
def bam_to_fastq(cellranger_demultiplex_dir, outdir, tempdir):
    run_bam_to_fastq(cellranger_demultiplex_dir, outdir, tempdir)


@cli.command()
@click.option('--meta_yaml', required=True, help='CSV file path')
@click.option('--cite_hto_id', help='CSV file path')
@click.option('--tcr_id', help='CSV file path')
@click.option('--bcr_id', help='CSV file path')
def check_multiplex_status(
        meta_yaml,
        cite_hto_id=None,
        tcr_id=None,
        bcr_id=None,
):
    metadata = yaml.safe_load(open(meta_yaml, 'rt'))

    if 'meta' not in metadata:
        print("non-multiplexed")
        return

    if metadata['meta'] is None:
        print("non-multiplexed")
        return

    if 'hashtag' not in metadata['meta']:
        print("non-multiplexed")
        return

    # either TCR or BCR must exist  to run all 3 steps
    # if tcr_id is None and bcr_id is None:
    #     print("non-multiplexed")
    #     return

    # cite and hto comes in a single dir and must exist to run all 3 steps
    if cite_hto_id is None:
        print("non-multiplexed")
        return

    print("multiplexed")


if __name__ == "__main__":
    cli()
