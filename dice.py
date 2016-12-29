# -*- coding: utf-8 -*-
import re
import random
import os
from wox import Wox

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

        diceBonus, noLimit = None, False
        diceParam = list(filter(lambda x: len(x) > 0, re.split('\s|d|D|,|\.', query)))
        diceParam[0] = list(filter(lambda x: len(x) > 0, re.split('\+|\-|\*|\/', diceParam[0])))
        diceParam[1] = list(filter(lambda x: len(x) > 0, re.split('\+|\-|\*|\/', diceParam[1])))
        if len(diceParam) == 3 and diceParam[2] == "-nolimit":
            noLimit = True
        elif len(diceParam) == 3 and diceParam[2] != "-nolimit":
            result.append({
                "Title": "Unknown options",
                "SubTitle":"Please use -nolimit to disable limit.",
                "IcoPath":"icon/dice.png",
            })
            return result
        elif len(diceParam) != 2 or len(diceParam[0]) > 1:
            result.append({
                "Title": "Bad parameters",
                "SubTitle":"Please make sure you enter two values,and use correct symbol.",
                "IcoPath":"icon/dice.png",
            })
            return result

        try:
            freq,surf = int(diceParam[0][0]),int(diceParam[1][0])
        except ValueError:
            result.append({
                "Title": "Value invalid",
                "SubTitle":"Please use integer.",
                "IcoPath":"icon/dice.png",
            })
            return result

        if freq <= 0 or surf <= 0:
            result.append({
                "Title": "Value can't be less than 0",
                "SubTitle":"Please use positive integer, excluding 0.",
                "IcoPath":"icon/dice.png",
            })
            return result

        if noLimit is not True:
            if freq > 30 or surf not in [2, 3, 4, 6, 8, 10, 12, 14, 16, 20, 30, 48, 60, 100, 120]:
                result.append({
                    "Title": "You can't rolling dice more than 30, or use irregular dice.",
                    "SubTitle":"You can use commonly used dice in TRPG with d14,d16,d24,d30,d48,d60,d120. Use options -nolimit to disable limit.",
                    "IcoPath":"icon/dice.png",
                })
                result.append({
                    "Title":"Use options -nolimit to disable limit.",
                    "SubTitle":"If you want rolling dice more than 30, or use irregular dice.",
                    "IcoPath":"icon/dice.png",
                    "JsonRPCAction": {
                        "method": "Wox.ChangeQueryText",
                        "parameters": [query + ' -nolimit',  ],
                        "dontHideAfterAction": True
                    }
                })
                return result

        diceResult = []
        for num in range(0,freq):
            rollDice = random.randint(1,surf)
            diceResult.append(rollDice)
        diceResultTotal = sum(diceResult)

        if len(diceParam[1]) == 2:
            bonusPattern = re.search('\+|\-|\*|\/', query)
            diceBonus = bonusPattern.group(0)
            if diceBonus is "+":
                diceResultTotal = diceResultTotal + int(diceParam[1][1])
            elif diceBonus is "-":
                diceResultTotal = diceResultTotal - int(diceParam[1][1])
            elif diceBonus is "*":
                diceResultTotal = diceResultTotal * int(diceParam[1][1])
            elif diceBonus is "/":
                diceResultTotal = diceResultTotal / int(diceParam[1][1])
            diceResultTotal = str(diceResultTotal)
            diceResult = str(diceResult) +'(' + '+' + diceParam[1][1] + ')'
            result.append({
                "Title": "Result: " + diceResultTotal,
                "SubTitle":"Detail: " + diceResult,
                "IcoPath":"icon/dice.png",
            })
            return result
        else:
            diceResultTotal = str(diceResultTotal)
            diceResult = str(diceResult)
            result.append({
                "Title": "Result: " + diceResultTotal,
                "SubTitle":"Detail: " + diceResult,
                "IcoPath":"icon/dice.png",
            })
            return result


if __name__ == "__main__":
    OmnipotentScepter()
