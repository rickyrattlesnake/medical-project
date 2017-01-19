def mergeFields(delimiter, validator, *fields):
    # convert to string and concatenate
    if not validator(fields):
        raise ValueError('Merge Failed with invalid Fields - {}'
                         .format(fields))
    return delimiter.join([str(field) for field in fields])


def unmergeField(delimiter, merged_field):
    return merged_field.split(delimiter)


if __name__ == '__main__':
    x = ['a', 'A', 'a']

    def validator(fields):
        return all(str(x).casefold() == str(y).casefold()
                   for (x, y) in zip(fields, fields[1:]))

    print(unmergeField('|', mergeFields('|', validator, *x)))
