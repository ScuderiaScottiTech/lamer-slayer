#!/bin/bash

# Verifica che siano stati passati due argomenti
if [ "$#" -ne 2 ]; then
    echo "Uso: $0 <origine> <destinazione>"
    exit 1
fi

# Directory di origine e destinazione
origine="$1"
destinazione="$2"

# Verifica che la directory di origine esista
if [ ! -d "$origine" ]; then
    echo "La directory di origine non esiste."
    exit 1
fi

# Verifica che la directory di destinazione esista, altrimenti creala
if [ ! -d "$destinazione" ]; then
    mkdir -p "$destinazione"
fi

# Conta il numero di file nella directory di origine
num_files=$(ls -1q "$origine"/* | wc -l)

# Calcola il 20% del numero di file
num_to_move=$((num_files * 20 / 100))

# Seleziona casualmente il 20% dei file e spostali nella directory di destinazione
ls -1 "$origine"/* | shuf -n "$num_to_move" | xargs -I {} mv {} "$destinazione"

echo "$num_to_move file spostati da $origine a $destinazione."
