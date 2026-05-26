from global_attributes.aegis import Aegis
from global_attributes.clock import Clock
from global_attributes.set_label import SetLabel
from data.fileman import FileManager


class Model(Aegis):
    """Legacy model shell; prefer :class:`aegis.simulation.Model` for new work."""

    def __init__(self):
        Aegis.__init__(self)
        self.clock = Clock()
        self.listSet = SetLabel()

        dir_path = "..\\data_external"
        file_name = "data.xlsx"

        fileman = FileManager(dir_path)
        fileman.add_file(file_name)

        self._data_file = fileman.get_file(file_name)
