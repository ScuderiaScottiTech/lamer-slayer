#!/bin/bash

# Percentuali passate come argomenti
perc_scam=${1}
perc_tossico=${2}
perc_lamer=${3}

# Verifica che le directory esistano
if [ ! -d "scam" ]; then
  echo "Directory 'scam' DOES NOT exist. Aborting."
  exit 1
fi

if [ ! -d "tossico" ]; then
  echo "Directory 'tossico' DOES NOT exist. Aborting."
  exit 1
fi

if [ ! -d "lamer" ]; then
  echo "Directory 'lamer' DOES NOT exist. Aborting."
  exit 1
fi

# Creazione della directory di destinazione
output_dir="mixed"
mkdir -p $output_dir

# Funzione per selezionare una percentuale di file da una directory e spostarli nella directory di destinazione
move_files() {
  src_dir=$1
  perc=$2
  total_files=$(ls -1 "$src_dir" | wc -l)
  files_to_move=$((total_files * perc / 100))
  
  echo "Moving $files_to_move files from $src_dir to $output_dir"

  ls "$src_dir" | shuf -n $files_to_move | xargs -I{} mv "$src_dir/{}" "$output_dir/"
}

# Sposta i file in base alle percentuali
move_files "scam" $perc_scam
move_files "tossico" $perc_tossico
move_files "lamer" $perc_lamer

echo "Files have been mixed into '$output_dir'."
