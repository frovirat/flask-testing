"""
Data Model used in text processing
"""
class ProcessStats:
    """
    Class that stores the process stats. Singleton
    """
    class _ProcessStats:
        """
        Internal instance of stats. Singleton implementation
        Attributes:
            n_text_processed: Number of text processed
            n_words_found: Number of words found
            n_letters_found: Number of characters found
        """
        n_text_processed = 0
        n_words_found = 0
        n_letters_found = 0
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance:
            return cls.__instance
        cls.__instance = cls._ProcessStats(*args, **kwargs)
        return cls.__instance
