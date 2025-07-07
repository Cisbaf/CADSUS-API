def is_valid_cns(cns: str) -> bool:
    cns = ''.join(filter(str.isdigit, cns))
    
    if len(cns) != 15:
        return False

    if cns[0] in '12':
        # Validação baseada no CPF
        soma = sum(int(cns[i]) * (15 - i) for i in range(15))
        return soma % 11 == 0
    elif cns[0] in '789':
        # Validação direta
        soma = sum(int(cns[i]) * (15 - i) for i in range(15))
        return soma % 11 == 0
    return False