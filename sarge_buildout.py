import subprocess


SARGE_BUILDOUT_CFG = """\
[buildout]
extends = buildout.cfg
eggs-directory = {cache}/eggs
download-cache = {cache}/download
extends-cache = {cache}/extends
"""


def set_up_buildout(bucket, **extra):
    if not (bucket.folder / 'buildout.cfg').isfile():
        return

    sarge = bucket.sarge
    dist = sarge.home_path / 'dist'
    cache = sarge.home_path / 'var' / 'buildout'
    for name in ['eggs', 'download', 'extends']:
        (cache / name).makedirs_p()

    sarge_buildout_cfg = SARGE_BUILDOUT_CFG.format(cache=str(cache))
    (bucket.folder / '_sarge_buildout.cfg').write_text(sarge_buildout_cfg)

    python = sarge.config.get('virtualenv_python_bin', 'python')
    subprocess.check_call([
        python, dist / 'bootstrap.py',
        '-c', '_sarge_buildout.cfg',
        '-d', '--setup-source=' + dist / 'distribute_setup.py',
        '--download-base=file://' + dist,
        ], cwd=bucket.folder)
    subprocess.check_call(['bin/buildout', '-c', '_sarge_buildout.cfg', '-v'],
                          cwd=bucket.folder)


def initialize():
    from sarge.deployer import bucket_setup
    bucket_setup.connect(set_up_buildout)
