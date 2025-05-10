class StringUtil:
    """
    A utility class for performing operations on strings.
    """

    @staticmethod
    def shorten_string(s: str, max_length: int) -> str:
        """
        Shortens a string to a specified maximum length by preserving the beginning and end of the string
        and inserting ".." in the middle. If the string is shorter than or equal to the maximum length,
        it is returned unchanged.
        If max_length is odd, one additional character is added to the first part of the shortened string to
        return a string with the length of max_length.
        """

        if len(s) <= max_length:
            return s
        if max_length < 3:
            raise ValueError("max_length must be at least 3")

        part_length: int = (max_length - 2) // 2
        first_part: str = s[:part_length + (max_length % 2)]
        last_part: str = s[-part_length:]
        return f"{first_part}..{last_part}"
