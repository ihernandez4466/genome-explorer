def analyze_sequence(raw_sequence: str) -> dict:
    """
    Validate and analyze a DNA sequence.

    On valid input, return a dict with keys:
        is_valid, clean_sequence, length, gc_content_pct,
        reverse, complement, reverse_complement

    On invalid input, return a dict with keys:
        is_valid, error
    """

    analyzer = Analyzer(raw_sequence)
    return {
        "is_valid": True,
        "clean_sequence": analyzer.get_clean_sequence(),
        "length": len(analyzer.get_clean_sequence()),
        "gc_content_pct": analyzer.get_gc_content(),
        "reverse": analyzer.get_reverse(),
        "complement": analyzer.get_complement(),
        "reverse_complement": analyzer.get_complement_reverse(),
    } if analyzer.is_valid() else {
        "is_valid": False,
        "error": f"Invalid character found: {analyzer.get_invalid_characters()}",
    }


class Analyzer:

    NUCLEOTIDE_PAIRS = {"A": "T", "G": "C", "T": "A", "C": "G", "N": "N"}

    def __init__(self, sequence: str):
        self.original_sequence = sequence
        self.clean_sequence = self.clean_sequence()

    def get_clean_sequence(self):
        return self.clean_sequence

    def get_invalid_characters(self):
        characters = []
        for character in self.clean_sequence:
            if character not in self.NUCLEOTIDE_PAIRS and character not in characters:
                characters.append(character)
        return ", ".join(characters)
    
    def get_gc_content(self):
        return self.calculate_gc_content(self.clean_sequence)

    def get_reverse(self):
        return self.calculate_reverse(self.clean_sequence)

    def get_complement(self):
        return self.calculate_complement(self.clean_sequence)

    def get_complement_reverse(self):
        return self.calculate_complement_reverse(self.clean_sequence)

    def clean_sequence(self):
        # remove empty characters
        raw_sequence = self.original_sequence.replace(" ", "")
        # remove new lines characters
        sequence = raw_sequence.replace("\n", "")
        return sequence.upper()

    def is_valid(self):
        for character in self.clean_sequence:
            if character.upper() not in self.NUCLEOTIDE_PAIRS:
                return False
        return True

    def calculate_gc_content(self, sequence: str):
        '''
        ((count of G  + count of C) / Total Sequence Length) x 100
        '''
        count_g = 0
        count_c = 0
        for character in sequence:
            if character == "G":
                count_g+=1
            elif character == "C":
                count_c+=1

        return (count_g + count_c) / len(sequence) * 100

    def calculate_complement(self, sequence: str):
        '''
        The complement of a sequence is calculated by using the opposite of the base pair for each character
        A pairs with T
        G pairs with C

        Example: ATGCAAGCT becomes TACGTTCGA
        '''
        result = ""
        for character in sequence:
            pair = self.NUCLEOTIDE_PAIRS.get(character)
            result += pair

        return result

    def calculate_reverse(self, sequence: str):
        '''
        The reverse of a sequence keeps the bases but swaps the order to be in reverse

        Example: ATGCAAGCT becomes TCGAACGTA
        '''
        result = sequence[::-1]
        return result


    def calculate_complement_reverse(self, sequence: str):
        '''
        The complement reverse of a sequence is calculated by two steps

        1. find the complement
        2. find the reverse of the complement calculated in step 1
        '''
        complement = self.calculate_complement(sequence)
        answer = self.calculate_reverse(complement)
        return answer