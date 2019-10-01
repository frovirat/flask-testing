from .models import ProcessStats


class TextProcessingController:
    """
    Class that contains counters and stats
    """
    @staticmethod
    def get_stats() -> dict:
        """This method return the stats of files processed

        Returns:
            dict: dictionary with the stats
                'text_processed_stat': Text that have been processed
                'characters_found': Characters found on the text processed
                'words_found': words found on the text processed
        """
        stats = ProcessStats()
        response = {
            'text_processed_stat': stats.n_text_processed,
            'characters_found': stats.n_letters_found,
            'words_found': stats.n_words_found
        }

        return response

    @staticmethod
    def reset_stats() -> str:
        """Reset all the stats to initial value

        Returns:
            str: success message
        """
        stats = ProcessStats()
        stats.n_text_processed = 0
        stats.n_letters_found = 0
        stats.n_words_found = 0

        return 'OK'

    @staticmethod
    def count_elements(text: str) -> dict:
        """Count the elements(words and characters) that contain a text

        Args:
            text (str): text to process

        Returns:
            dict: response with the counts
                'words': words found on the text
                'characters': characters found on the text
        """
        response = {
            'words': 0,
            'characters': 0
        }
        try:
            response['words'] = len(text.split(' '))
            response['characters'] = len(text)
            stats = ProcessStats()
            stats.n_text_processed += 1
            stats.n_words_found += response['words']
            stats.n_letters_found = response['characters']

        except AttributeError:
            pass

        return response

    @staticmethod
    def count_words(text: str, words: list = None) -> dict:
        """function that count the words that exist on a given text

        Args:
            text (str): text to process
            words (list, optional): list of words to filter the results, only counts the words in
            this list. Defaults to None means all are counted.

        Returns:
            dict: count response
                'words_found': number of words found
        """
        try:
            response = {'words_found': 0}
            count_words = [word for word in text.split(' ') if word]

            if words:
                count_words = [word for word in count_words if word in words]

            response['words_found'] = len(count_words)
            stats = ProcessStats()
            stats.n_text_processed += 1
            stats.n_words_found += response['words_found']

        except AttributeError:
            pass

        return response
