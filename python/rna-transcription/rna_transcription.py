"""
rna_transcription.py --
"""


def to_rna(dna_strand: str):
    """Convert to adverse rna strand"""
    rna_trans = {"G": "C", "C": "G", "T": "A", "A": "U"}
    return dna_strand.translate(str.maketrans(rna_trans))
