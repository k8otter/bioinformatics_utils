library(dplyr)
library(stringr)

data <- read.csv("H:\\My Drive\\Katz-Lab_Otter-Data\\Projects\\Molecular_Neuroanatomy\\doc\\insulins\\bioinf\\OTHER-SPP\\ILPs_alignment_ready.csv")

data1 <- data %>%
  filter(!is.na(motif)) %>%
  mutate(ILP_type = case_when(
    str_detect(motif, "C8XC13XC") ~ "ILP7",
    str_detect(motif, "C1XCC") ~ "MILP",
    str_detect(motif, "CC3XC8XC") ~ "aILP",
    .default = "Unknown")) %>%
  mutate(node = paste(species, accession, sep = " "))

write.csv(data1, "H:\\My Drive\\Katz-Lab_Otter-Data\\Projects\\Molecular_Neuroanatomy\\doc\\insulins\\bioinf\\OTHER-SPP\\ILPs_alignment_ready_motifclass.csv")
    
