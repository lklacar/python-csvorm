from model import CSVModel


class Person(CSVModel):
    first_name = ""
    last_name = ""
    id = "0"


if __name__ == "__main__":
    # Create a person
    p = Person()
    p.first_name = "First Name"
    p.last_name = "Last Name"
    p.id = "123"
    p.save()

    # List all people
    print Person.all()

    # Find that person
    print p.get(id="123")

    # Delete it
    p.delete(id="123")
    print p.get(id="123")
