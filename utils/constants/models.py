from django.db import models


class Gender(models.IntegerChoices):
    female = 1
    male = 2
    other = 3


class Difficulty(models.IntegerChoices):
    Easy = 1
    Mid = 2
    High = 3


class InOutType(models.IntegerChoices):
    input = 1
    output = 2


class DataType(models.IntegerChoices):
    Integer = 1
    Long = 2
    Float = 3
    Double = 4
    Char = 5
    String = 6
    Boolean = 7
    ArrayOfIntegers = 8
    ArrayOfLongs = 9
    ArrayOfFloats = 10
    ArrayOfDoubles = 11
    ArrayOfChars = 12
    ArrayOfStrings = 13
    ArrayOfBooleans = 14
    MatrixOfIntegers = 15
    MatrixOfLongs = 16
    MatrixOfFloats = 17
    MatrixOfDoubles = 18
    MatrixOfChars = 19
    MatrixOfStrings = 20
    MatrixOfBooleans = 21


class ProfileContent():
    Accout = 1
    Profile = 2
    All = 3
    Custom = 4


class RankingType():
    User = 1
    OrganizationRanking = 2


class ChallengeTypeContent():
    Public = 1
    Group = 2
    Owner = 3
    Completed = 4
