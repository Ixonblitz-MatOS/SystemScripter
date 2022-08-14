import datetime
from colorama import Fore

month = datetime.datetime.now().month
day = datetime.datetime.now().day
year = datetime.datetime.now().year
hour = datetime.datetime.now().hour
minute = datetime.datetime.now().minute
second = datetime.datetime.now().second
ampm = datetime.datetime.today().strftime("%p")
RED = Fore.RED


class DateException(Exception):
    def _ErrorPrint(self, message) -> int:
        print(RED, message)
        return 0

    def SeparatorError(DateException):
        """
        :raise: When Separator raises string errors
        """
        DateException._ErrorPrint("Separator has caused an issue make sure it is not an escape character and is in the ASCII table")

    def DateNotAvailable(DataException):
        """
        :raise: When Date cannot be gotten from System
        """
        DataException._ErrorPrint("Cannot Get The Date From System")

    def TimeNotAvailable(DataException):
        """
        :raise:When Time cannot be taken from System
        """
        DataException._ErrorPrint("Cannot Get The Time From System")

    def TimeAndDateNotAvailable(DataException):
        """
        :raise: When Time and Date not Available
        """
        DataException._ErrorPrint("Cannot Get The Time Or Date From System")

class Date:
    def GetFullDate(self,CustomSeparator: str, CustomTimeSeparator: str) -> str:
        """
        :return: Month/day/year : hour minute second am/pm
        """
        return f'{month}{CustomSeparator}{day}{CustomSeparator}{year} {hour}{CustomTimeSeparator}{minute}{CustomTimeSeparator}{second}{CustomTimeSeparator}{ampm} '


    def mdy(self,CustomSeparator: str) -> str:
        """
        :return: Month/Day/Year
        """
        return f'{month}{CustomSeparator}{day}{CustomSeparator}{year}'


    def hms(self,CustomeTimeSeparator: str) -> str:
        """
        :return: hour minute second
        """
        return f'{hour}{CustomeTimeSeparator}{minute}{CustomeTimeSeparator}{second}'


    def StandardTime(self,CustomeTimeSeparator: str) -> str:
        """
        :return: hour minute second AM/PM
        """
        return f'{hour}{CustomeTimeSeparator}{minute}{CustomeTimeSeparator}{second}{CustomeTimeSeparator}{ampm}'


    def DateTime(self,CustomSeparator: str, CustomMidSeparator: str, CustomeTimeSeparator: str) -> str:
        """
        :return: Date|CustomSeparator|Time
        """
        return f'{month}{CustomSeparator}{day}{CustomSeparator}{year}{CustomMidSeparator}{hour}{CustomeTimeSeparator}{minute}{CustomeTimeSeparator}{second}'