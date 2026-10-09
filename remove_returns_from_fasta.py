from Bio import SeqIO
SeqIO.write(
    (r for r in SeqIO.parse(r"input.fasta", "fasta")),
    r"output.fasta",
    "fasta-2line"
)