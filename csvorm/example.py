from csvorm.fields import StringField
from model import CSVModel
from relations import HasOne, HasMany


class City(CSVModel):
    city_name = StringField()
    id = StringField()




if __name__ == "__main__":
    # Create a person

    c = City()

    print c.id

    c.city_name = "Novi Sad"
    c.id = "1"
    c.save()

    print City.all()[0].city_name