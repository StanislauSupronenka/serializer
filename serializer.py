import re


fl = "test.txt"
PRIMITIVE_TYPES = [
    'int',
    'loat',
    'complex',
    'str',
    'bool'
]
CONTAINER_TYPES = [
    'list',
    'tuple',
    'set',
    'frozenset'
    ]
DICT_TYPE = ['dict']
REG_TYPE = re.compile(r"^<class '(\w+)'>$")


def serialize(obj):
    tmp_type = REG_TYPE.match(str(type(obj))).group(1)
    if tmp_type in PRIMITIVE_TYPES:
        return "{} = {}".format(tmp_type, obj)
    if tmp_type in CONTAINER_TYPES:
        return "{} ({})".format(tmp_type,';⠀'.join([serialize(el) for el in obj]))
    if tmp_type in DICT_TYPE:
        return "{} ({}⠀:⠀{})".format(tmp_type,
                                   ' ;'.join([serialize(key) for key in obj.keys()]),
                                   ' ;'.join([serialize(val) for val in obj.values()]))

def dump(obj, fl=fl):
    with open(fl, "a") as f:
        f.write("{};\n".format(serialize(obj)))


def deserialize_prim(obj):
    for i in range(0, len(obj.split()) - 1):
        return (parse_type(a[i])(re.sub(r";",'', a[i+2])))


def deserialize_cont(obj):
    tmp_obj = obj.split()
    tmp_list = []
    for i in range(0,len(tmp_obj) - 1):
        b = re.sub(r"\(",'', tmp_obj[i])
        if b in PRIMITIVE_TYPES:
            tmp_list.append(parse_type(b)(re.sub(r";?\)?",'', tmp_obj[i+2])))
    return parse_type(tmp_obj[0])(tmp_list)


def deserialize_dict(obj):
    a = 'dict (int = 5⠀:⠀int = 6);'
    tmp_obj = obj.split()
    tmp_dict = {}
    for i in range(0, len(tmp_obj) - 1):
        b = re.sub(r"\d*?\(?:?;?", '', tmp_obj[i])
        print(b)
        if b in PRIMITIVE_TYPES:
           tmp_dict[parse_type(b)(re.sub(r":?\w*?;?\)??",'', tmp_obj[i+2]))] = (re.sub(r"\w+?;?\)?:?",'', tmp_obj[i+4]))
        if i+4 > len(tmp_obj) - 1:
            break
    return tmp_dict


def load(fl=fl):
    with open(fl) as f:
        lines = f.readlines()

    return [deserialize(line) for line in lines]


def parse_type(str_type: str):
    if str_type == "int":
        return int
    elif str_type == "float":
        return float
    elif str_type == "complex":
        return complex
    elif str_type == "str":
        return str
    elif str_type == "list":
        return list
    elif str_type == "tuple":
        return tuple
    elif str_type == "set":
        return set
    elif str_type == "dict":
        return dict
