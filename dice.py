# -*- coding: utf-8 -*-
import re
import random
import os
from wox import Wox, WoxAPI

class OmnipotentScepter(Wox):

    def query(self, query):
        result = []
        if not query:
            result.append({
                "Title": "Let's roll some dice!",
                "SubTitle":"You can use '1d20','1D20','1 20','1,20','1.20' to rolling dice.",
                "IcoPath":"icon/dice.png",
            })
            return result

        diceParam = list(filter(lambda x: len(x) > 0, re.split('\s|d|D|,|\.', query)))

        if len(diceParam) != 2:
            result.append({
                "Title": "Missing parameters",
                "SubTitle":"Please make sure you enter two values,and use correct symbol.",
                "IcoPath":"icon/dice.png",
            })
            return result

        try:
            freq,surf = int(diceParam[0]),int(diceParam[1])
        except ValueError:
            result.append({
                "Title": "Value invalid",
                "SubTitle":"Please use integer.",
                "IcoPath":"icon/dice.png",
            })
            return result
        if freq <= 0 or surf <= 0:
            result.append({
                "Title": "Value invalid",
                "SubTitle":"Please use positive integer, excluding 0.",
                "IcoPath":"icon/dice.png",
            })
            return result
        else:
            diceResult = []
            for num in range(0,freq):
                rollDice = random.randint(1,surf)
                diceResult.append(rollDice)
            diceResultTotal = sum(diceResult)

            diceResult = str(diceResult)
            diceResultTotal = str(diceResultTotal)
            result.append({
                "Title": "Result: " + diceResultTotal,
                "SubTitle":"Detail: " + diceResult,
                "IcoPath":"icon/dice.png",
            })
            return result



if __name__ == "__main__":
    OmnipotentScepter()
