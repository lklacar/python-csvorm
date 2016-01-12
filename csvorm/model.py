import os
import helpers
import settings
from relations import HasOne, HasMany, Relation


class CSVModel(object):
    """
    Base class of all csv models
    """
    @classmethod
    def file_path(cls):
        """
        :return: Path of the csv file for this class
        """
        filename = "%s%s" % (cls.__name__, settings.FILE_EXTENTION)
        file_path = os.path.join(settings.MODEL_DIR, filename)
        return file_path

    @classmethod
    def init_file(cls):
        """
        Creates the file if it does not exist and writes the correct header to it
        :return:
        """
        correct_header = cls._get_header()
        try:
            # If the file exists, check if the header is correct and add it if it is not
            lines = helpers.file_lines(cls.file_path())
            file_header = lines[0].strip()
            if file_header != correct_header:
                lines.pop()
                lines.insert(0, correct_header + "\n")

            file = open(cls.file_path(), "w")
            file.writelines(lines)
            file.close()

        except IOError:
            # If the file does not exist, create it and write the header
            file = open(cls.file_path(), "w")
            file.write(cls._get_header() + "\n")
            file.close()
        except IndexError:
            # If the file exists, but the file is empty, write the header
            file = open(cls.file_path, "w")
            file.write(cls._get_header() + "\n")
            file.close()

    @classmethod
    def _get_header(cls):
        """

        :return: Header of the csv file
        """
        attributes = cls._get_attributes()
        return settings.SEPARATOR.join(attributes)

    @classmethod
    def _get_attributes(cls):
        """

        :return:  Inspects the class and returns the list of all attributes that need to be persisted
        """
        return [attr for attr in cls.__dict__ if not attr.startswith("__")]


    @classmethod
    def all(cls):
        """
        Reads the correct csv file, parses it, makes objects and returns the list of objects
        :return: List of all objects
        """
        cls.init_file()
        lines = helpers.file_lines_without_header(cls.file_path())
        attributes = cls._get_attributes()
        objects = []
        for line in lines:
            temp = cls()
            tokens = line.split(settings.SEPARATOR)
            for i in range(len(tokens)):
                attr = getattr(temp, attributes[i].strip())

                if isinstance(attr, Relation):
                    val = attr.get(id=tokens[i].strip())
                    setattr(temp, attributes[i].strip(), val)

                else:
                    attr.set(tokens[i].strip())
                    print attr
                    setattr(temp, attributes[i].strip(), attr)
            objects.append(temp)
        return objects

    @classmethod
    def get(cls, **kwarg):
        """
        Returns the list of all objects that match the given condition
        :param kwarg: condition key=value
        :return: List of objects
        """
        cls.init_file()
        all = cls.all()
        found = []
        field_names = kwarg.keys()
        for item in all:
            for field_name in field_names:
                if getattr(item, field_name.strip()) == kwarg[field_name.strip()].strip():
                    found.append(item)
        return found

    def save(self):
        """
        Persists the object to correct csv file
        :return:
        """
        self.init_file()
        fields = self._get_attributes()
        values = []
        for field in fields:
            if isinstance(getattr(self, field), CSVModel):
                value = str(getattr(self, field).id)
            elif isinstance(getattr(self, field), list):
                value = []
                for i in getattr(self, field):
                    value.append(i.id)
                value = ",".join(value)
            else:
                value = getattr(self, field)
            values.append(value)

        open(self.file_path(), "a").write("|".join(values) + "\n")

    @classmethod
    def order_by(cls, **kwarg):
        """
        Returns the list of all objects sorted by the given field
        Example:
            Person.order_by(order_by='name')
        :return: list of sorted objects
        """
        cls.init_file()
        key = kwarg['order_by']
        all_objects = cls.all()
        for i in range(len(all_objects)):
            for j in range(len(all_objects)):
                if getattr(all_objects[i], key) < getattr(all_objects[j], key):
                    all_objects[i], all_objects[j] = all_objects[j], all_objects[i]
        return all_objects


    @classmethod
    def _write_header(cls):
        header = cls._get_header()
        file = open(cls.file_path(), 'w')
        file.write(header)
        file.close()

    @classmethod
    def delete(cls, **kwarg):
        """
        Deletes the object with given condition
        :param kwarg:
        :return:
        """
        cls.init_file()
        all = cls.all()

        cls._write_header()

        field_names = kwarg.keys()
        for item in all:
            for field_name in field_names:
                if not getattr(item, field_name.strip()) == kwarg[field_name.strip()].strip():
                    item.save()
