from model import CSVModel
from relations import HasOne, HasMany


class City(CSVModel):
    city_name = ""
    id = ""

class Person(CSVModel):
    first_name = ""
    last_name = ""
    id = "0"
    city = HasMany(City)



if __name__ == "__main__":
    # Create a person

    """
    c = City()
    c.city_name = "Novi Sad"
    c.id = "1"
    c.save()
    """

    print Person.all()[0].city
