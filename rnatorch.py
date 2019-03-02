import click
from os import mkdir, path, symlink, chdir
import json
from shutil import copy2
from subprocess import call, Popen

def create_config(r1, r2, gmap, star, nt, outdir, m, t):
    data = {}
    data['r1'] = r1
    data['r2'] = r2
    data['sample'] = r1[:r1.find('_')]
    data['star_index'] = star
    data['gmap_index'] = gmap
    data['blast_db'] = nt + "/nt" if nt != "" else "None"
    data['root'] = path.dirname(path.realpath(__file__))
    data['outdir'] = outdir
    data['threads'] = int(t)
    data['memory'] = int(m)
    with open(outdir + "/config.json", 'w') as configfile:
        json.dump(data, configfile, sort_keys=True, indent=4)


@click.group()
def main():
    pass

@main.command()
@click.option('--outdir', nargs = 1, required = True)
def restart(outdir):
    """Restart unfinished RNA SV pipeline."""
    chdir(outdir)
    process = Popen(['snakemake', '--unlock'])
    process.wait()
    process = Popen(['snakemake'])
    process.wait()


@main.command()
@click.option('--r1', help = "Left Reads", required = True)
@click.option('--r2', help = "Right Reads", required = True)
@click.option('--gmap', help = "Path to GMAP index", required = True)
@click.option('--star', help = "Path to STAR index", required = True)
@click.option('--nt', default = "", nargs = 1, help = 'Folder containing NT database. '
                                      'If not provided filtering of non-human sequences is not performed')
@click.option('--outdir', nargs = 1, required = True)
@click.option('-m', default = 100, nargs = 1, help = 'Available memory specified in gygabytes')
@click.option('-t', default = 8, nargs = 1, help = 'Number of threads')
def run(r1, r2, gmap, star, nt, outdir, m, t):
    """Run RNA SV pipeline."""
    try:
        mkdir(outdir)
    except:
        print("Output folder can't be created")
        return -1
    create_config(r1, r2, gmap, star, nt, outdir, m, t)
    copy2(path.dirname(path.realpath(__file__)) + "/path_to_executables_config.json", outdir)
    copy2(path.dirname(path.realpath(__file__)) + "/Snakefile", outdir)
    mkdir(outdir + "/sample")
    symlink(path.abspath(r1), outdir + "/sample/" + path.basename(r1))
    symlink(path.abspath(r2), outdir + "/sample/" + path.basename(r2))
    chdir(outdir)
    process = Popen(['snakemake'])
    process.wait()

if __name__ == '__main__':
    main()