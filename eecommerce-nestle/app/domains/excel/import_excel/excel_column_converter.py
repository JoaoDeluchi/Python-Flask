from string import ascii_uppercase
characters = ascii_uppercase

def convert_column(arg:int) -> str:
    count_times = 0
    position = ''
    while(arg>0):
        if(is_bigger_than_26(arg)):
            position = characters[count_times]
            count_times += 1
            arg = arg-26
        else:
            position += characters[arg-1]
            arg = 0
    return position

def is_bigger_than_26(value:int) -> bool:
    if value > 26:
        return True
    return False