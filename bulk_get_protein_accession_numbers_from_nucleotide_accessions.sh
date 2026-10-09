export PATH=${HOME}/edirect:${PATH}
cat input.txt | efetch -db nucleotide -format gb | grep -E "ACCESSION|protein_id" | sed -E 's/.*protein_id="([^"]+)".*/\1/' > protein_ids.txt