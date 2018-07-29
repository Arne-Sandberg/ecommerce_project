MAX_RESULTS_PER_RESPONSE = 5000
OBJECT_ID_PATTERN = r'([a-f\d]{24})'
ISO_DATETIME_REGEX = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])' \
                     r'-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):' \
                     r'([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?' \
                     r'(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'

STATUS_TYPES = [
    "LOCKED",
    "FREE",
    "AVAILABLE",
    "PENDING",
    "PROCESSING",
    "TO_BE_DISPATCHED",
    "DISPATCHED",
    "MISSING",
]

STATUS = {key: key for key in STATUS_TYPES}

TO_BE_DISPATCHED = (STATUS['TO_BE_DISPATCHED'])
FREE = (STATUS['FREE'], STATUS['AVAILABLE'])
LOCKED = (STATUS['LOCKED'], STATUS['PROCESSING'])
