#!/usr/bin/env python3
# -*-encoding: utf-8-*-

import bcrypt


def encrypt(password, encoding='utf-8'):
    return bcrypt.hashpw(bytes(password, encoding=encoding), bcrypt.gensalt(14))


def check_pass(password, hashed):
    return bcrypt.checkpw(password, hashed)
