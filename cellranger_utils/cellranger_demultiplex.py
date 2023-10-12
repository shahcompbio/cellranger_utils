import os
import yaml
import cellranger_utils.utils as utils


def create_multiconfig(
        metadata,
        reference,
        config_dir,
        multiconfig_path,
        fastq_data
):
    # this cellranger mode requires hto
    assert 'hashtag' in metadata['meta']

    lines = [
        f'[gene-expression]',
        f'reference,{reference}',
    ]

    cmo_path = os.path.join(config_dir, 'cmo.txt')
    cmo_path = os.path.abspath(cmo_path)
    utils.create_cmo(metadata, cmo_path)
    lines.extend([f'cmo-set,{cmo_path}'])

    if 'citeseq' in metadata['meta']:
        antibodies_path = os.path.join(config_dir, 'antibodies.txt')
        antibodies_path = os.path.abspath(antibodies_path)
        utils.create_antibodies(metadata, antibodies_path)
        lines.extend([f'[feature]', f'reference,{antibodies_path}'])

    lines.extend([f'[libraries]', f'fastq_id,fastqs,feature_types'])

    for fastq_info in fastq_data:
        lines.append(f"{fastq_info['id']},{fastq_info['fastq']},{fastq_info['type']}")

    lines.append('[samples]'),
    lines.append('sample_id,cmo_ids')
    for hashtag in metadata['meta']['hashtag'].keys():
        sampleid = metadata['meta']['hashtag'][hashtag]['sample_id']
        sampleid = sampleid.replace('#', '_')
        lines.append(f"{sampleid},{hashtag}")

    with open(multiconfig_path, 'w') as f:
        f.writelines('\n'.join(lines))


def run_cellranger_demultiplex(
        reference,
        meta_yaml,
        gex_fastq,
        gex_identifier,
        cite_hto_fastq,
        cite_hto_identifier,
        sample_id,
        outdir,
        tempdir,
        numcores=16,
        mempercore=10,
):
    metadata = yaml.safe_load(open(meta_yaml, 'rt'))

    tempdir = os.path.abspath(tempdir)
    reference = os.path.abspath(reference)
    gex_fastq = os.path.abspath(gex_fastq)
    cite_hto_fastq = os.path.abspath(cite_hto_fastq)

    config_dir = os.path.join(tempdir, 'configs')
    multiconfig_path = os.path.join(config_dir, 'multiconfig.txt')
    utils.makedirs(config_dir)

    fastq_data = [
        {'type': 'Gene Expression', 'id': gex_identifier, 'fastq': gex_fastq},
        {'type': 'Multiplexing Capture', 'id': cite_hto_identifier, 'fastq': cite_hto_fastq}
    ]

    create_multiconfig(
        metadata, reference, config_dir, multiconfig_path, fastq_data
    )

    cmd = [
        'cellranger',
        'multi',
        '--csv=' + multiconfig_path,
        '--id=' + sample_id,
        f'--localcores={numcores}',
        f'--localmem={mempercore}',
        '--jobmode=local',
        '--disable-ui'
    ]

    cwd = os.getcwd()
    os.chdir(tempdir)
    utils.run_cmd(cmd)
    os.chdir(cwd)

    os.rename(os.path.join(tempdir, sample_id), outdir)
