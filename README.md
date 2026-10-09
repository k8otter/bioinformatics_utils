# bioinformatics\_utils

Note: these have all been tested and used on Windows devices only



### Bash:

If you have a bunch of accession numbers for nucleotide sequences but want the corresponding protein accession numbers:



**bulk\_get\_protein\_accession\_numbers\_from\_nucleotide\_accessions.sh**



To run:

* edit input.txt
* edit protein\_ids.txt
* navigate to the folder containing your input
* `bash bulk\_get\_protein\_accession\_numbers\_from\_nucleotide\_accessions.sh`



The output file can then be used on NCBI Batch Entrez<https://www.ncbi.nlm.nih.gov/sites/batchentrez> to make a fasta file containing all of those sequences. I suggest you run bulk\_replace\_nucleotide\_accessions\_with\_protein\_accessions.ps1  first to get a list of the accession numbers only because the output format will not work in Batch Entrez.





### Cmd:

If you are making a spreadsheet of the accession numbers (e.g. with species info or source dois) and want to replace the nucleotide sequences with the protein sequences:



**bulk\_replace\_nucleotide\_accessions\_with\_protein\_accessions.ps1**



To run:

* edit protein\_ids.txt
* edit input.csv
* edit output\_csv.csv
* navigate to folder containing your inputs
* `powershell -File "C:\\path\\to\\bulk\_replace\_nucleotide\_accessions\_with\_protein\_accessions.ps1"`



### Python:

You will need a python (Python 3.14.8) environment with the following installed:

* biopython 1.88
* ipykernel
* jupyterlab
* blast
* pandas



To create a conda env: `conda create -n env\_name python=3.14.8 biopython=1.88`

You can install other packages as needed with pip or conda forge

#### 

#### To prepare sequences for alignment and create metadata:



**fasta\_cleaning\_pipeline\_updated.ipynb**



To use:

* Note: The notebook itself contains detailed information about parameters and output files
* You will need to be in the correct python environment and setting up the kernel depends on the IDE you are using
* Update the Imports \& Global Configuration block and run

  * pay special attention to: 

    * Entrez.email
    * INPUT\_FASTA
    * HEADER\_TAXON\_RANK - useful if you want to have the order or family appended to the end of the header
    * DATASET\_ID - will label all of the files
    * PAPER\_ACCESSIONS\_CSV - expects a csv file with two columns "paper\_accession" and "source\_doi" 
    * BASE\_OUTPUT\_DIR
  * Run the helper-definition cells down through \*\*SignalP 6 trimming\*\*. These define the functions used below.
  * Run \*\*Preparation\*\* to create the metadata review CSV. Open it, fill unresolved entries, and save it before continuing.
  * Run \*\*Pipeline Execution (main)\*\*. It rereads the saved review sheet and may ask you to choose duplicate records or supply missing species.
  * Run optional analysis sections only when needed, after checking their paths and switches.

    * InterPro Scan
    * Dibasic cleavage site identification
    * Additional filtering by motifs, domains from InterPro, taxonomy 





#### To design in-situ probes for HCR:

If you have a nucleotide sequence that you just want the open reading frame for (this will also remove returns which you need for the HCR\_probe\_maker.ipynb):



**crop\_fasta\_orfs.py**



To run:

* open anaconda prompt
* activate your conda environment `conda activate env\_name`
* navigate to folder containing the script
* `python crop\_fasta\_orfs.py input.fasta`

  * make sure you have the path to the input fasta if you do not
  * you could run: `python crop\_fasta\_orfs.py input.fasta -o cropped.fasta --complete-only` to only take orfs that have a start and stop codon or `python crop\_fasta\_orfs.py input.fasta --stop-codons TAA,TAG` to specify the stop codons



If you just want to remove the returns in preparation for the HCR\_probe\_maker.ipynb:



**remove\_returns\_from\_fasta.py**



To run:

* open in your favorite IDE (e.g. VSCode)
* edit the input.fasta
* edit the output.fasta
* click run



To create probes for HCR:



**HCR\_probe\_maker.ipynb**



To run:

* You will need to be in the correct python environment and setting up the kernel depends on the IDE you are using
* Edit the configuration block (descriptions of the parameters are in the notebook) - you may run all if the configuration block is updated or run them one at a time

  * Run the helper function blocks
  * Run the design block
  * Run the export block













