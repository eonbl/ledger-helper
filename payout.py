import re
import sys
import operator

# Computes payout transactions to settle a ledger
# Accepts input from console: "Name: (buy-in) -> buy-out" (with some room for error) and empty new line at the end

# Example input:
# Aaron (200) -> 313.5
# Brad (100) -> 21.60
# Charlie (200) -> 164.9
#

# parse_input can be modified to accept other formats


def parse_lines(lines):
    names = []
    buy_ins = []
    buy_outs = []

    for line in lines:
        # Find all numbers in the line
        res = [float(s) for s in list(zip(*re.findall(r'[+-]?((\d+(\.\d*)?)|(\.\d+))', line)))[0]]
        if len(res) >= 2:
            # Name is the first word in the line
            name = re.findall('\w+', line)[0]
            names.append(name)
            buy_ins.append(res[0])
            buy_outs.append(res[-1])
        elif line == '\n':
            continue
        else:
            print('Error in formatting: needs at least 2 numbers in each line')
            sys.exit()

    if sum(buy_ins) != sum(buy_outs):
        print('WARNING: sum of buy-ins do not match sum of buy-outs')

    return names, buy_ins, buy_outs


def parse_input():
    lines = []

    while True:
        line = input()
        if line:
            lines.append(line)
        else:
            break

    return parse_lines(lines)


def compute_payout(names, buy_ins, buy_outs):
    assert(len(names) == len(buy_ins) == len(buy_outs))

    positive = []
    negative = []
    payouts = []

    # Distribute any unaccounted for money evenly among all players
    balanced_buy_ins = list(buy_ins)
    balanced_buy_outs = list(buy_outs)
    extra = (sum(buy_ins) - sum(buy_outs)) / len(names)
    for i in range(len(balanced_buy_outs)):
        balanced_buy_outs[i] += extra

    if abs(extra * len(names)) > 0.004:
        print("NOTE: Missing profits/losses distributed evenly among players")

    # Line up all positive profits and negative profits and match them from largest to smallest
    for i in range(len(names)):
        profit = balanced_buy_outs[i] - balanced_buy_ins[i]
        if profit > 0:
            positive.append([names[i], profit])
        elif profit < 0:
            negative.append([names[i], abs(profit)])

    positive.sort(key=operator.itemgetter(1), reverse=True)
    negative.sort(key=operator.itemgetter(1), reverse=True)

    pos_idx = 0
    neg_idx = 0
    while pos_idx < len(positive) and neg_idx < len(negative):
        if positive[pos_idx][1] > negative[neg_idx][1]:
            positive[pos_idx][1] -= negative[neg_idx][1]
            payouts.append([negative[neg_idx][0], positive[pos_idx][0], negative[neg_idx][1]])
            neg_idx += 1
        elif positive[pos_idx][1] < negative[neg_idx][1]:
            negative[neg_idx][1] -= positive[pos_idx][1]
            payouts.append([negative[neg_idx][0], positive[pos_idx][0], positive[pos_idx][1]])
            pos_idx += 1
        else:
            payouts.append([negative[neg_idx][0], positive[pos_idx][0], negative[pos_idx][1]])
            pos_idx += 1
            neg_idx += 1

    return payouts


def string_in_out(names, buy_ins, buy_outs):
    if len(names) == len(buy_ins) == len(buy_outs):
        str = f'\tIn\t{"Out":>6}\t{"Profit":>8}\n'
        for i in range(len(names)):
            str += f'{names[i]}\t{int(buy_ins[i])}\t{buy_outs[i]:>6.2f}\t{buy_outs[i]-buy_ins[i]:>+8.2f}\n'
        str += f'Total\t{sum([int(b) for b in buy_ins])}\t{sum(buy_outs):>6.2f}' + \
               f'\t{sum([buy_outs[i]-buy_ins[i] for i in range(len(buy_outs))]):>+8.2f}\n'
    else:
        str = 'Buy-ins and buy-outs do not match number of players\n'

    return str


def string_payout(payouts):
    str = f'\nFrom\t\tTo\t\t{"Amount":>6}\n'
    for f, t, amt in payouts:
        str += f'{f}\t\t{t}\t\t{amt:>6.2f}\n'
    return str


if __name__ == '__main__':
    names, buy_ins, buy_outs = parse_input()

    print(string_in_out(names, buy_ins, buy_outs))

    print(string_payout(compute_payout(names, buy_ins, buy_outs)))
