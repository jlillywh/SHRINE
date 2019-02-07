class Date:
    def __init__(self, date_string):
        #Aegis.__init__(self)
        self.__date = date_string
        date_array = date_string.split('/',2)
        self.month = int(date_array[0])
        self.day = int(date_array[1])
        self.year = int(date_array[2])

    def advance(self):
        """Add 1 day to the current date."""
        max_days = [31,28,31,30,31,30,31,31,30,31,30,31]
        if self.day < max_days[self.month - 1]:
            self.day += 1
        else:
            self.day = 1
            if self.month < 12:
                self.month += 1
            else:
                self.month = 1
                self.year += 1
        self.__date = str(self.month) + '/' + str(self.day) + '/' + str(self.year)
        return self.__date

    @property  # when you do Date.date, it will call this function
    def date(self):
        return self.__date

    @date.setter  # when you do Date.date = x, it will call this function
    def date(self, date_string):
        """Set the amount but limit it to the bounds immediately.
            Parameters
            ----------
            date_string : str
                user defined amount to replace the existing __date

            Returns
            -------
            self.__date : str
                The new __date
        """
        self.__date = date_string

    def __repr__(self):
        return self.date