import re

def is_valid_cpf(cpf: str) -> bool:
    # Remove pontos e traços
    cpf = ''.join(filter(str.isdigit, cpf))
    
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False

    def calculate_digit(digits, factor):
        total = sum(int(d) * f for d, f in zip(digits, range(factor, 1, -1)))
        remainder = (total * 10) % 11
        return remainder if remainder < 10 else 0

    first_digit = calculate_digit(cpf[:9], 10)
    second_digit = calculate_digit(cpf[:10], 11)

    return cpf[-2:] == f"{first_digit}{second_digit}"


def normalize_cpf_format(value: str) -> str:
    # Verifica se está no formato xxx.xxx.xxx-xx
    if re.fullmatch(r"\d{3}\.\d{3}\.\d{3}-\d{2}", value):
        return re.sub(r"[.-]", "", value)
    return value
