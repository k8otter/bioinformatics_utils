from Bio import SeqIO
SeqIO.write(
    (r for r in SeqIO.parse(r"G:\My Drive\Sondhi_Lab_Otter_Data\Projects\IEG\bioinformatics\reference_genes\alpha_TUB\primer_making\Galleria_mellonella_XM_026906502.2.fasta", "fasta")),
    r"G:\My Drive\Sondhi_Lab_Otter_Data\Projects\IEG\bioinformatics\reference_genes\alpha_TUB\primer_making\Galleria_mellonella_XM_026906502.2_nospaces.fasta",
    "fasta-2line"
)