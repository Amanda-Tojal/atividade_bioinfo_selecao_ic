with open("m160801_104636_42242_c101006162550000001823230309161600_s1_p0.fastq","r")as file:
    conteúdo = file.read()
    print (conteúdo[0:1000])
import subprocess
import os
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

def run_fastqc(input_file, output_dir):
    """Executa o FastQC para verificar a qualidade das leituras"""
    command = f"fastqc {input_file} -o {output_dir}"
    subprocess.run(command, shell=True)

def remove_adapters(input_file, output_file):
    """Remover adaptadores usando Fastp (ou outra ferramenta)"""
    command = f"fastp -i {input_file} -o {output_file} --detect_adapter_for_pe"
    subprocess.run(command, shell=True)

def remove_contamination(input_file, output_file):
    """Remover contaminação usando BBMap"""
    command = f"bbduk.sh in={input_file} out={output_file} ref=contaminant_db.fasta k=31"
    subprocess.run(command, shell=True)

def assemble_genome(input_file, output_dir):
    """Montar o genoma usando SPAdes"""
    command = f"spades.py -s {input_file} -o {output_dir}"
    subprocess.run(command, shell=True)

def analyze_assembly(assembly_dir):
    """Analisar o resultado da montagem usando QUAST"""
    command = f"quast.py {assembly_dir}/contigs.fasta"
    subprocess.run(command, shell=True)

def calculate_n50(contig_file):
    """Calcular o N50 e outras métricas do genoma montado"""
    if not os.path.exists(contig_file):
        print(f"Erro: o arquivo {contig_file} não foi encontrado.")
        return None
    
    contigs = []
    for record in SeqIO.parse(contig_file, "fasta"):
        contigs.append(len(record.seq))
    
    contigs.sort(reverse=True)
    total_length = sum(contigs)
    half_total_length = total_length / 2

    length_sum = 0
    n50 = None
    for length in contigs:
        length_sum += length
        if length_sum >= half_total_length:
            n50 = length
            break
    
    return n50
def main():
    # Caminho dos arquivos
    input_file = "m160801_104636_42242_c101006162550000001823230309161600_s1_p0.fastq"
    output_dir = "resultado_fastqc"
    cleaned_file = "sequencias_limpas.fastq"
    assembled_dir = "genoma_montado"
    contig_file = f"{assembled_dir}/spades_output/contigs.fasta"
    # 1. Qualidade das Leituras
    print("Realizando controle de qualidade com FastQC...")
    run_fastqc(input_file, output_dir)
    
    # 2. Remoção de adaptadores
    print("Removendo adaptadores...")
    remove_adapters(input_file, cleaned_file)
    
    # 3. Remoção de contaminação
    print("Removendo contaminação...")
    remove_contamination(cleaned_file, "sequencias_sem_contaminacao.fastq")
    
    # 4. Montagem do Genoma
    print("Realizando montagem do genoma...")
    assemble_genome("sequencias_sem_contaminacao.fastq", assembled_dir)
    
    # 5. Análise da montagem
    print("Analisando os resultados da montagem...")
    analyze_assembly(assembled_dir)
    
    # 6. Calculando N50
    print("Calculando N50...")
    n50 = calculate_n50(f"{assembled_dir}/spades_output/scaffolds.fasta")

    n50 = calculate_n50(contig_file)
    
    if n50 is not None:
        print(f"N50: {n50}")
    else:
        print("Falha ao calcular o N50.")
    
if __name__ == "__main__":
    main()

