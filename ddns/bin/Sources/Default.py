
from abc import abstractmethod

class Default_Source():
    def __init__(self,
                 start_end_marks:
                 tuple[str, str]) -> None:
        self.start_end_marks = start_end_marks

    def _fmt_start_end_marks(self, start_or_end_mark : str) -> int:
        """
        self.start_end_marks looks like
        "/home/jacobc/docker/ddns/sites.yaml", line 10, column 3
        """
        return int(start_or_end_mark.split(',')[1].strip().split(' ')[1])
    def _fmt_start_mark(self) -> int:
        return self._fmt_start_end_marks(self.start_end_marks[0])
    def _fmt_end_mark(self) -> int:
        return self._fmt_start_end_marks(self.start_end_marks[1])
    def _fmt_file_from_start_end_marks(self) -> str:
        return self.start_end_marks[0].split(',')[0].split('"')[1]
    
    @abstractmethod
    def obtain_state(self) -> None:
        pass

    def _create_dotenv_KeyError(self):
        error = KeyError(f"The .env is missing a defined key in pushes/!{self.__class__.__name__} "
                 f"- you should fix this in {self._fmt_file_from_start_end_marks()} between lines {self._fmt_start_mark()} and {self._fmt_end_mark()}")
        return error