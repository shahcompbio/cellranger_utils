import os
import errno
import pandas as pd
from subprocess import Popen, PIPE


def makedirs(directory, isfile=False):
    if isfile:
        directory = os.path.dirname(directory)
        if not directory:
            return

    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def run_cmd(cmd, output=None):
    cmd = [str(v) for v in cmd]

    print(' '.join(cmd))

    stdout = PIPE
    if output:
        stdout = open(output, "w")

    p = Popen(cmd, stdout=stdout, stderr=PIPE)

    cmdout, cmderr = p.communicate()
    retc = p.returncode

    if retc:
        raise Exception(
            "command failed. stderr:{}, stdout:{}".format(
                cmdout,
                cmderr))

    if output:
        stdout.close()


def create_cmo(metadata, cmo_path):
    data = []

    for cmo in metadata['meta']['hashtag']:
        print(cmo)
        data.append({
            'id': cmo,
            'name': cmo,
            'read': 'R2',
            'pattern': '^NNNNNNNNNN(BC)NNNNNNNNN',
            'sequence': metadata['meta']['hashtag'][cmo]['sequence'],
            'feature_type': 'Multiplexing Capture',
        })

    pd.DataFrame(data).to_csv(cmo_path, index=False)


def create_antibodies(metadata, antibodies_path):
    data = []
    for cmo in metadata['meta']['citeseq']:
        data.append({
            'id': cmo,
            'name': metadata['meta']['citeseq'][cmo]['protein'].replace(',', '_').replace(' ', '_').replace('(',
                                                                                                            '').replace(
                ')', ''),
            'read': 'R2',
            'pattern': '^NNNNNNNNNN(BC)NNNNNNNNN',
            'sequence': metadata['meta']['citeseq'][cmo]['sequence'],
            'feature_type': 'Antibody Capture',
        })

    pd.DataFrame(data).to_csv(antibodies_path, index=False)


def read_metrics(metrics):
    df = pd.read_csv(metrics)

    numcells = df[df['Category'] == 'Cells']
    numcells = numcells[numcells['Library Type'] == 'Gene Expression']
    numcells = numcells[numcells['Metric Name'] == 'Cells']
    numcells = str(numcells['Metric Value'].iloc[0])
    numcells = int(numcells.replace(',', '').strip())

    numreads = df[df['Category'] == 'Library']
    numreads = numreads[numreads['Library Type'] == 'Gene Expression']
    numreads = numreads[numreads['Grouped By'] == 'Physical library ID']
    numreads = numreads[numreads['Group Name'] == 'GEX_1']
    numreads = numreads[numreads['Metric Name'] == 'Number of reads']
    numreads = str(numreads['Metric Value'].iloc[0])
    numreads = int(numreads.replace(',', '').strip())

    return numreads, numcells
