from collections import OrderedDict

def dict_to_OreredDict(basedic, fields):
    new_dic = OrderedDict()
    if (not isinstance(fields, list)):
        raise ValueError('type of field must list current field type -> {0}'.format(type(fields)))
    for field in fields:
        #print(field)
        new_dic[field] = basedic[field];

    return new_dic
