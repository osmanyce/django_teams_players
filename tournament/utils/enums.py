#
# Created by Osmany Castro.
# Copyright © 2021. All rights reserved.
#
from enum import Enum


class ResponseStatus(str, Enum):
    SUCCESS = 'success'
    FAILED = 'failed'
