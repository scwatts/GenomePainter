#!/usr/bin/env python3
"""
This script summarises the species composition of Genome Painter results, per contig.

It outputs a tab-delimited table with these columns:
  1) Contig name
  2) Contig length
  3) Species 1: the best matching species (across all contigs)
  4) Species 2: the second-best matching species
  etc.

Example usage:
    summarise_contigs.py genome_painter_results.tsv
"""

import argparse
import os


def get_arguments():
    parser = argparse.ArgumentParser(description='Summarise contigs from genome painter results',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('input', type=str,
                        help='A tsv file from paint_genome')
    parser.add_argument('--threshold', type=float, required=False, default=0.9,
                        help='Minimum probability threshold - positions with a max probability '
                             'lower than this will be ignored')
    parser.add_argument('--top_num', type=int, required=False, default=4,
                        help='This many of the top species matches will be displayed')

    args = parser.parse_args()
    return args


def main():
    args = get_arguments()

    summarise_contigs(args.input, args.threshold, args.top_num)


def summarise_contigs(result_file, threshold, top_num):
    assembly_name = os.path.basename(result_file).replace('_painted.tsv', '')
    species_names = get_species_names(result_file)
    species_tallies = {x: 0 for x in species_names}
    contig_tallies = {}
    contig_names = []
    contig_lengths = {}
    with open(result_file, 'rt') as result:
        for line in result:
            if line.startswith('#'):
                continue
            parts = line.strip().split('\t')
            contig = parts[0]
            if contig not in contig_tallies:
                contig_names.append(contig)
                contig_tallies[contig] = {x: 0 for x in species_names}
            position = int(parts[1])
            contig_lengths[contig] = position
            probabilities = [float(x) for x in parts[2:]]
            assert len(probabilities) == len(species_names)
            max_prob = max(probabilities)
            if max_prob >= threshold:
                best_species = species_names[probabilities.index(max_prob)]
                species_tallies[best_species] += 1
                contig_tallies[contig][best_species] += 1

    total = sum(species_tallies.values())
    if total == 0:
        return '\t'.join([assembly_name, 'Error: no assembly positions meet threshold'])
    percentages = [(x, 100.0 * species_tallies[x] / total) for x in species_names]
    percentages = sorted(percentages, reverse=True, key=lambda x: x[1])

    top_species = [p[0] for p in percentages[:top_num]]
    print_header(top_species)

    for contig in contig_names:
        contig_total = sum(contig_tallies[contig].values())
        if contig_total == 0:
            continue
        output = [contig, str(contig_lengths[contig])]
        for s in top_species:
            contig_percentage = 100.0 * contig_tallies[contig][s] / contig_total
            output.append('%.4f' % contig_percentage)
        print('\t'.join(output))


def get_species_names(result_file):
    species_names = []
    with open(result_file, 'rt') as result:
        for line in result:
            if line.startswith('#'):
                species_names.append(line.strip()[1:])
            else:
                break
    return species_names


def print_header(top_species):
    header = ['Contig', 'Length'] + top_species
    print('\t'.join(header))


if __name__ == '__main__':
    main()