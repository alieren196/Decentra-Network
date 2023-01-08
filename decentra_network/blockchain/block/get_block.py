#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
import os

from decentra_network.blockchain.block.block_main import Block
from decentra_network.config import TEMP_BLOCK_PATH
from decentra_network.lib.config_system import get_config
from decentra_network.lib.log import get_logger

logger = get_logger("BLOCKCHAIN")


def GetBlock(custom_TEMP_BLOCK_PATH=None):
    """
    Returns the block.
    """
    the_TEMP_BLOCK_PATH = (TEMP_BLOCK_PATH if custom_TEMP_BLOCK_PATH is None
                           else custom_TEMP_BLOCK_PATH)

    os.chdir(get_config()["main_folder"])

    # Files are looking like this:
    # db/temp_block.decentra_network.json2
    # db/temp_block.decentra_network.json3
    # db/temp_block.decentra_network.json4

    # So we need to get the highest number and delete others
    # We need to get the highest number
    highest_number = 0
    for file in os.listdir(get_config()["main_folder"] + "/db"):
        if file.startswith(the_TEMP_BLOCK_PATH):
            number = int(file.replace(the_TEMP_BLOCK_PATH, ""))
            if number > highest_number:
                highest_number = number
    
    # We need to delete all other files
    for file in os.listdir(get_config()["main_folder"] + "/db"):
        if file.startswith(the_TEMP_BLOCK_PATH):
            number = int(file.replace(the_TEMP_BLOCK_PATH, ""))
            if number != highest_number:
                os.remove(file)

    # We need to load the highest number
    the_TEMP_BLOCK_PATH += str(highest_number)


    with open(the_TEMP_BLOCK_PATH, "r") as block_file:
        the_block_json = json.load(block_file)
    result = Block.load_json(the_block_json)

    return result
