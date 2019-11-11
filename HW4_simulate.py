import sys
import random

def parseFile(filename):
    """
    Parses a FASTA file and returns it as a string

    Parameters
    ---------
    filename : file
        FASTA file that will be parsed

    Returns
    -------
    file_lines : str
        a string version of filename
    """

    file_lines = ""
    file = open(filename, "r")
    file.readline()

    for line in file:
        nextline = line.strip()
        file_lines = file_lines + nextline

    file_lines.lower()
    file.close()
    return file_lines

def get_GL(file_line):
    """
    Using the string version of the FASTA file from parseFile(filename), find
    the character length of the genome

    Parameters
    ---------
    file_lines : str
        string version of the FASTA file from parseFile(filename)

    Returns
    -------
    len_Genome : int
        an integer representation of the character length of the genome
    """

    len_Genome = 0

    for word in file_line:
        len_Genome += len(word)

    return len_Genome

def simulate(genome, len_Genome, len_Read, rate_Error):
    """
    Using the string version of the FASTA file from parseFile(filename), 
    simulate the genome including mutations

    Parameters
    ---------
    genome : str
        string version of the FASTA file from parseFile(filename)
    len_Genome : int
        an integer representation of the character length of the genome
    len_Read : int
        the length of the read as given by the user
    rate_Error : float
        the error rate represented by a float as given by the user

    Returns
    -------
    read : str
        a simulated possible read from the sequence of DNA
    """

    pos_nucleotides = ["A","G","T","C"]
    read = ""

    randStart = random.randint(0,(len_Genome-(len_Read + 1)))
    for i in range(len_Read):
        if random.randint(0,100) < (rate_Error * 100):
            pos_nucleotides.remove(genome[randStart+i])
            read = read + random.choice(pos_nucleotides)
            pos_nucleotides.append(genome[randStart+i])
        else:
            read = read + genome[randStart+i]

    return read

def main():
    Coverage = int(sys.argv[2])
    len_Read = int(sys.argv[3])
    rate_Error = float(sys.argv[4])

    genome = parseFile(FASTA_file)
    len_Genome = get_GL(genome)

    N = int((Coverage + len_Genome)/len_Read)

    readFile = open("reads.txt","w+")

    for i in range(N):
        readFile.write(simulate(genome, len_Genome, len_Read, rate_Error))
        readFile.write("\n")

    readFile.close()

if __name__ == "__main__":
    main()
