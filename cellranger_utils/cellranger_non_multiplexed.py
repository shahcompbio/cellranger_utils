import os
import yaml
import cellranger_utils.utils as utils


def create_multiconfig(
        metadata,
        reference,
        vdj_reference,
        config_dir,
        multiconfig_path,
        fastq_data
):
    lines = [
        f'[gene-expression]',
        f'reference,{reference}'
    ]
    if 'hashtag' in metadata['meta']:
        cmo_path = os.path.join(config_dir, 'cmo.txt')
        cmo_path = os.path.abspath(cmo_path)
        utils.create_cmo(metadata, cmo_path)
        lines.extend([f'cmo-set,{cmo_path}'])

    lines += [
        f'[vdj]',
        f'reference,{vdj_reference}',
    ]

    lines.extend([f'[libraries]', f'fastq_id,fastqs,feature_types'])

    for fastq_info in fastq_data:
        lines.append(f"{fastq_info['id']},{fastq_info['fastq']},{fastq_info['type']}")

    if 'hashtag' in metadata['meta']:
        lines.append('[samples]'),
        lines.append('sample_id,cmo_ids')
        for hashtag in metadata['meta']['hashtag'].keys():
            sampleid = metadata['meta']['hashtag'][hashtag]['sample_id']
            sampleid = sampleid.replace('#', '_')
            lines.append(f"{sampleid},{hashtag}")

    with open(multiconfig_path, 'w') as f:
        f.writelines('\n'.join(lines))


def run_cellranger_non_multiplexed(
        reference,
        vdj_reference,
        gex_fastq,
        gex_identifier,
        output,
        meta_yaml,
        tempdir,
        sample_id,
        tcr_fastq=None,
        tcr_identifier=None,
        cite_fastq=None,
        cite_identifier=None,
        bcr_fastq=None,
        bcr_identifier=None,
        numcores=16,
        mempercore=10,
):
    config_dir = os.path.join(tempdir, 'configs')
    utils.makedirs(config_dir)

    metadata = yaml.safe_load(open(meta_yaml, 'rt'))

    reference = os.path.abspath(reference)
    vdj_reference = os.path.abspath(vdj_reference)
    gex_fastq = os.path.abspath(gex_fastq)
    bcr_fastq = os.path.abspath(bcr_fastq) if bcr_fastq is not None else bcr_fastq
    tcr_fastq = os.path.abspath(tcr_fastq) if tcr_fastq is not None else tcr_fastq
    cite_fastq = os.path.abspath(cite_fastq) if cite_fastq is not None else cite_fastq

    fastq_data = [{'type': 'Gene Expression', 'id': gex_identifier, 'fastq': gex_fastq}]
    if cite_fastq is not None:
        cite_type = 'Multiplexing Capture' if 'hashtag' in metadata['meta'] else 'Antibody Capture'
        fastq_data.append({'type': cite_type, 'id': cite_identifier, 'fastq': cite_fastq})
    if bcr_fastq is not None:
        fastq_data.append({'type': 'VDJ-B', 'id': bcr_identifier, 'fastq': bcr_fastq})
    if tcr_fastq is not None:
        fastq_data.append({'type': 'VDJ-T', 'id': tcr_identifier, 'fastq': tcr_fastq})

    metadata = yaml.safe_load(open(meta_yaml, 'rt'))

    multiconfig_path = os.path.abspath(os.path.join(config_dir, 'multiconfig.txt'))
    create_multiconfig(
        metadata, reference, vdj_reference, config_dir, multiconfig_path, fastq_data
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

    os.rename(os.path.join(tempdir, sample_id), output)
