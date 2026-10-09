#!/usr/bin/env python3

# Usage:
#   python crop_fasta_orfs.py input.fasta
#   python crop_fasta_orfs.py input.fasta -o cropped.fasta --complete-only
#   python crop_fasta_orfs.py input.fasta --stop-codons TAA,TAG

  
import argparse
import csv
import re
from pathlib import Path

IUPAC = set('ACGTURYSWKMBDHVN')
COMP = str.maketrans('ACGTRYSWKMBDHVN', 'TGCAYRSWMKVHDBN')


def read_fasta(path):
    header, parts = None, []
    with path.open(encoding='utf-8-sig') as handle:
        for number, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if header is not None:
                    yield header, ''.join(parts)
                header, parts = line[1:], []
                if not header.strip():
                    raise ValueError(f'Empty FASTA header on line {number}')
            else:
                if header is None:
                    raise ValueError(f'Sequence before first header on line {number}')
                parts.append(''.join(line.split()))
    if header is not None:
        yield header, ''.join(parts)


def sequence_type(header, sequence):
    words = set(re.findall(r'[a-z]+', header.lower()))
    if words & {'pep', 'peptide', 'protein', 'aa'}:
        return 'protein'
    if words & {'dna', 'rna', 'nt', 'nucleotide', 'cds'}:
        return 'nucleotide'
    letters = set(sequence.upper())
    if sequence and letters <= IUPAC:
        fraction = sum(c in 'ACGTUN' for c in sequence.upper()) / len(sequence)
        if letters <= set('ACGTU') or fraction >= 0.9:
            return 'nucleotide'
    return 'protein_or_uncertain'


def longest_orf(sequence, stops, complete_only=False, forward_only=False):
    """Return (oriented DNA, strand, frame, original start, end, complete).

    Coordinates are 1-based inclusive on the original sequence. Ties favor
    forward strand, then lower frame, then earlier oriented start.
    """
    dna = sequence.upper().replace('U', 'T')
    if set(dna) - IUPAC:
        raise ValueError('Nucleotide record contains non-IUPAC symbols (including gaps)')
    best = None
    strands = [('+', dna)]
    if not forward_only:
        strands.append(('-', dna.translate(COMP)[::-1]))
    for strand, oriented in strands:
        for frame in range(3):
            start = None
            end = frame
            for pos in range(frame, len(oriented) - 2, 3):
                codon = oriented[pos:pos+3]
                end = pos + 3
                if set(codon) - set('ACGT'):
                    if start is not None and not complete_only:
                        best = choose(best, oriented, strand, frame, start, pos, False)
                    start = None
                elif codon in stops:
                    if start is not None:
                        best = choose(best, oriented, strand, frame, start, end, True)
                    start = None
                elif codon == 'ATG' and start is None:
                    start = pos
            if start is not None and not complete_only:
                best = choose(best, oriented, strand, frame, start, end, False)
    return best


def choose(best, oriented, strand, frame, start, end, complete):
    fragment = oriented[start:end]
    if best is not None and len(fragment) <= len(best[0]):
        return best
    if strand == '+':
        lo, hi = start + 1, end
    else:
        lo, hi = len(oriented) - end + 1, len(oriented) - start
    return fragment, strand, frame + 1, lo, hi, complete


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('input', nargs='?', type=Path, help='Input FASTA; prompts if omitted')
    parser.add_argument('-o', '--output', type=Path)
    parser.add_argument('--complete-only', action='store_true', help='Require both ATG and a stop codon')
    parser.add_argument('--forward-only', action='store_true', help='Search only the three forward frames')
    parser.add_argument('--sequence-type', choices=['auto', 'nucleotide', 'protein'], default='auto')
    parser.add_argument('--stop-codons', default='TAA,TAG,TGA', help='Comma-separated stops for your genetic code')
    args = parser.parse_args()
    source = args.input or Path(input('Input FASTA path: ').strip().strip('\"'))
    output = args.output or source.with_name(source.stem + '_longest_orf.fasta')
    report = output.with_suffix('.report.tsv')
    if source.resolve() in {output.resolve(), report.resolve()}:
        parser.error('Output/report must not overwrite input')
    if output.exists() or report.exists():
        parser.error('Output or report already exists; choose another output name')
    stops = {c.strip().upper().replace('U', 'T') for c in args.stop_codons.split(',')}
    if not stops or any(len(c) != 3 or set(c) - set('ACGT') for c in stops) or 'ATG' in stops:
        parser.error('Stop codons must be three A/C/G/T bases and cannot include ATG')
    # Validate every record before creating output files.
    records, rows = [], []
    try:
        for header, sequence in read_fasta(source):
            kind = sequence_type(header, sequence) if args.sequence_type == 'auto' else args.sequence_type
            result = longest_orf(sequence, stops, args.complete_only, args.forward_only) if kind == 'nucleotide' else None
            strand = frame = start = end = complete = ''
            if result:
                cropped, strand, frame, start, end, complete = result
                status = 'cropped'
            else:
                cropped = sequence
                status = 'no_orf_kept' if kind == 'nucleotide' else 'protein_or_uncertain_kept'
            if not sequence:
                status = 'empty_kept'
            records.append((header, cropped))
            rows.append([header, kind, status, len(sequence), len(cropped), strand, frame, start, end, complete])
        if not records:
            raise ValueError('No FASTA records found')
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    with output.open('x', encoding='utf-8', newline='\n') as handle:
        for header, sequence in records:
            handle.write(f'>{header}\n{sequence}\n')
    with report.open('x', encoding='utf-8', newline='') as handle:
        writer = csv.writer(handle, delimiter='\t')
        writer.writerow(['header', 'detected_type', 'status', 'input_length', 'output_length', 'strand', 'frame_on_oriented_strand', 'original_start_1based', 'original_end_1based', 'has_terminal_stop'])
        writer.writerows(rows)
    print(f'FASTA: {output.resolve()}\nReport: {report.resolve()}')
    print(f'{len(rows)} records; {sum(r[2] == "cropped" for r in rows)} cropped.')
    print('Review report type assignments, especially for ambiguous nucleotide/protein alphabets.')


if __name__ == '__main__':
    main()
