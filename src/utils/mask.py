import re

# Sequências de 11+ dígitos: CPF (11) e CNS (15), com ou sem pontuação.
_DIGIT_RUN = re.compile(r"\d[\d.\-\s]{9,}\d")


def mask_documents(text: str) -> str:
    """Mascara CPF/CNS em textos que vão para o log, mantendo os 3 últimos dígitos."""
    def _mask(match: re.Match) -> str:
        digits = ''.join(filter(str.isdigit, match.group()))
        if len(digits) < 11:
            return match.group()
        return f"{'*' * (len(digits) - 3)}{digits[-3:]}"

    return _DIGIT_RUN.sub(_mask, text)
