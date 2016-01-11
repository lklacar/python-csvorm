import os

import settings


class CSVModel(object):
    @classmethod
    def file_path(cls):
        filename = "%s%s" % (cls.__name__, settings.FILE_EXTENTION)
        file_path = os.path.join(settings.MODEL_DIR, filename)
        return file_path

    @classmethod
    def init_file(cls):
        correct_header = cls._get_header()
        try:
            file = open(cls.file_path(), "r")
            lines = file.readlines()
            file_header = lines[0].strip()
            if file_header != correct_header:
                lines.pop()
                lines.insert(0, correct_header + "\n")
            file.close()
            file = open(cls.file_path(), "w")
            file.writelines(lines)

            file.close()

        except IOError:
            file = open(cls.file_path(), "w")
            file.write(cls._get_header() + "\n")
            file.close()
        except IndexError:
            file = open(cls.file_path, "w")
            file.write(cls._get_header() + "\n")
            file.close()

    @classmethod
    def _get_header(cls):
        attributes = cls._get_attributes()
        return settings.SEPARATOR.join(attributes)

    @classmethod
    def _get_attributes(cls):
        return [attr for attr in cls.__dict__ if not attr.startswith("__")]

    @classmethod
    def _get_lines(cls):
        lines = open(cls.file_path(), "r").readlines()
        del lines[0]  # remove header
        return lines

    @classmethod
    def all(cls):
        cls.init_file()
        lines = cls._get_lines()
        attributes = cls._get_attributes()
        objects = []
        for line in lines:
            temp = cls()
            tokens = line.split(settings.SEPARATOR)
            for i in range(len(tokens)):
                setattr(temp, attributes[i].strip(), tokens[i].strip())
            objects.append(temp)
        return objects

    @classmethod
    def get(cls, **kwarg):
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
        cls.init_file()
        key = kwarg['order_by']
        all_objects = cls.all()
        for i in range(len(all_objects)):
            for j in range(len(all_objects)):
                if getattr(all_objects[i], key) < getattr(all_objects[j], key):
                    all_objects[i], all_objects[j] = all_objects[j], all_objects[i]
        return all_objects

    @classmethod
    def delete(cls, **kwarg):
        cls.init_file()
        all = cls.all()

        # cita header iz fajla kako bi ga kasnije ponovo sacuvao
        file = open(cls.file_path(), 'r')
        header = file.readlines()[0]
        file.close()
        file = open(cls.file_path(), 'w')
        file.write(header)
        file.close()

        field_names = kwarg.keys()
        for item in all:
            for field_name in field_names:
                if not getattr(item, field_name.strip()) == kwarg[field_name.strip()].strip():
                    item.save()
