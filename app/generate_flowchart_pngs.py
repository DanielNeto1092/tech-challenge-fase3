from __future__ import annotations

import struct
import zlib
from pathlib import Path


OUTPUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "flowcharts"


FONT_5X7: dict[str, list[str]] = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11100", "10010", "10001", "10001", "10001", "10010", "11100"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01110"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
    "J": ["00111", "00010", "00010", "00010", "10010", "10010", "01100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "0": ["01110", "10001", "10011", "10101", "11001", "10001", "01110"],
    "1": ["00100", "01100", "00100", "00100", "00100", "00100", "01110"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "3": ["11110", "00001", "00001", "00110", "00001", "00001", "11110"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "5": ["11111", "10000", "10000", "11110", "00001", "00001", "11110"],
    "6": ["01110", "10000", "10000", "11110", "10001", "10001", "01110"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "8": ["01110", "10001", "10001", "01110", "10001", "10001", "01110"],
    "9": ["01110", "10001", "10001", "01111", "00001", "00001", "01110"],
    " ": ["00000", "00000", "00000", "00000", "00000", "00000", "00000"],
    "-": ["00000", "00000", "00000", "11111", "00000", "00000", "00000"],
}


FLOWCHARTS = [
    {
        "name": "triagem_ginecologica",
        "title": "FLUXO DE TRIAGEM GINECOLOGICA",
        "bg": (253, 243, 231),
        "stroke": (184, 107, 75),
        "fill": (255, 247, 240),
        "text": (64, 34, 24),
        "boxes": [
            (30, 95, 160, 92, ["SINTOMAS", "RELATADOS"]),
            (220, 95, 160, 92, ["ANALISE", "DE RISCO"]),
            (410, 95, 170, 92, ["CLASSIFICACAO", "DE URGENCIA"]),
            (610, 95, 170, 92, ["SUGESTAO", "DE EXAMES"]),
            (810, 95, 170, 92, ["ORIENTACOES", "INICIAIS"]),
            (1010, 95, 160, 92, ["AGENDAMENTO", "OU", "ENCAMINHAMENTO"]),
        ],
    },
    {
        "name": "violencia_domestica",
        "title": "FLUXO DE VIOLENCIA DOMESTICA",
        "bg": (253, 236, 236),
        "stroke": (192, 86, 33),
        "fill": (255, 244, 244),
        "text": (74, 31, 31),
        "boxes": [
            (30, 95, 160, 92, ["SINAIS", "DE ALERTA"]),
            (220, 95, 160, 92, ["AVALIACAO", "DE RISCO"]),
            (410, 95, 170, 92, ["PROTOCOLO", "DE SEGURANCA"]),
            (610, 95, 170, 92, ["EQUIPE", "ESPECIALIZADA", "ACIONADA"]),
            (810, 95, 170, 92, ["DOCUMENTACAO", "SEGURA"]),
            (1010, 95, 160, 92, ["ACOMPANHAMENTO", "E", "SEGUIMENTO"]),
        ],
    },
    {
        "name": "obstetrico",
        "title": "FLUXO OBSTETRICO",
        "bg": (234, 244, 251),
        "stroke": (43, 108, 138),
        "fill": (243, 248, 252),
        "text": (39, 67, 93),
        "boxes": [
            (30, 95, 160, 92, ["DADOS", "DA GESTANTE"]),
            (220, 95, 170, 92, ["AVALIACAO DE", "RISCO", "GESTACIONAL"]),
            (420, 95, 160, 92, ["ORIENTACOES", "GERAIS"]),
            (610, 95, 170, 92, ["SUGESTAO", "DE EXAMES"]),
            (810, 95, 170, 92, ["ALERTAS", "DE URGENCIA"]),
            (1010, 95, 160, 92, ["ACOMPANHAMENTO", "CONTINUO"]),
        ],
    },
    {
        "name": "prevencao",
        "title": "FLUXO DE PREVENCAO",
        "bg": (237, 247, 236),
        "stroke": (58, 125, 68),
        "fill": (243, 251, 241),
        "text": (47, 90, 50),
        "boxes": [
            (30, 95, 170, 92, ["HISTORICO", "DA PACIENTE"]),
            (230, 95, 180, 92, ["IDENTIFICACAO", "DE EXAMES", "PENDENTES"]),
            (440, 95, 170, 92, ["ORIENTACOES", "PREVENTIVAS"]),
            (640, 95, 170, 92, ["AGENDAMENTO", "SUGERIDO"]),
            (840, 95, 170, 92, ["LEMBRETES", "PERSONALIZADOS"]),
        ],
    },
]


class Canvas:
    def __init__(self, width: int, height: int, bg: tuple[int, int, int]) -> None:
        self.width = width
        self.height = height
        self.pixels = bytearray(bg * width * height)

    def _set(self, x: int, y: int, color: tuple[int, int, int]) -> None:
        if 0 <= x < self.width and 0 <= y < self.height:
            idx = (y * self.width + x) * 3
            self.pixels[idx:idx + 3] = bytes(color)

    def fill_rect(self, x: int, y: int, w: int, h: int, color: tuple[int, int, int]) -> None:
        x0 = max(0, x)
        y0 = max(0, y)
        x1 = min(self.width, x + w)
        y1 = min(self.height, y + h)
        for yy in range(y0, y1):
            start = (yy * self.width + x0) * 3
            end = (yy * self.width + x1) * 3
            row = bytes(color) * (x1 - x0)
            self.pixels[start:end] = row

    def draw_rect_outline(self, x: int, y: int, w: int, h: int, color: tuple[int, int, int], thickness: int = 3) -> None:
        self.fill_rect(x, y, w, thickness, color)
        self.fill_rect(x, y + h - thickness, w, thickness, color)
        self.fill_rect(x, y, thickness, h, color)
        self.fill_rect(x + w - thickness, y, thickness, h, color)

    def draw_line(self, x1: int, y1: int, x2: int, y2: int, color: tuple[int, int, int], thickness: int = 3) -> None:
        dx = abs(x2 - x1)
        dy = -abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx + dy
        while True:
            self.fill_rect(x1 - thickness // 2, y1 - thickness // 2, thickness, thickness, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x1 += sx
            if e2 <= dx:
                err += dx
                y1 += sy

    def draw_arrow(self, x1: int, y1: int, x2: int, y2: int, color: tuple[int, int, int]) -> None:
        self.draw_line(x1, y1, x2, y2, color, thickness=4)
        self.draw_line(x2, y2, x2 - 12, y2 - 7, color, thickness=4)
        self.draw_line(x2, y2, x2 - 12, y2 + 7, color, thickness=4)

    def draw_char(self, x: int, y: int, char: str, color: tuple[int, int, int], scale: int = 4) -> int:
        pattern = FONT_5X7.get(char.upper(), FONT_5X7[" "])
        for row_idx, row in enumerate(pattern):
            for col_idx, bit in enumerate(row):
                if bit == "1":
                    self.fill_rect(x + col_idx * scale, y + row_idx * scale, scale, scale, color)
        return 6 * scale

    def draw_text(self, x: int, y: int, text: str, color: tuple[int, int, int], scale: int = 4) -> int:
        cursor = x
        for char in text:
            cursor += self.draw_char(cursor, y, char, color, scale)
        return cursor - x

    def text_width(self, text: str, scale: int = 4) -> int:
        return len(text) * 6 * scale

    def save_png(self, path: Path) -> None:
        raw = bytearray()
        stride = self.width * 3
        for y in range(self.height):
            raw.append(0)
            start = y * stride
            raw.extend(self.pixels[start:start + stride])

        def chunk(tag: bytes, data: bytes) -> bytes:
            return (
                struct.pack("!I", len(data))
                + tag
                + data
                + struct.pack("!I", zlib.crc32(tag + data) & 0xFFFFFFFF)
            )

        png = bytearray(b"\x89PNG\r\n\x1a\n")
        png.extend(chunk(b"IHDR", struct.pack("!IIBBBBB", self.width, self.height, 8, 2, 0, 0, 0)))
        png.extend(chunk(b"IDAT", zlib.compress(bytes(raw), level=9)))
        png.extend(chunk(b"IEND", b""))
        path.write_bytes(png)


def render_flowchart(spec: dict) -> None:
    canvas = Canvas(1200, 260, spec["bg"])
    canvas.draw_text(40, 24, spec["title"], spec["text"], scale=4)

    boxes = spec["boxes"]
    for x, y, w, h, lines in boxes:
        canvas.fill_rect(x, y, w, h, spec["fill"])
        canvas.draw_rect_outline(x, y, w, h, spec["stroke"], thickness=3)
        line_scale = 3
        line_height = 7 * line_scale + 8
        block_height = len(lines) * line_height - 8
        yy = y + (h - block_height) // 2
        for line in lines:
            line_width = canvas.text_width(line, scale=line_scale)
            xx = x + (w - line_width) // 2
            canvas.draw_text(xx, yy, line, spec["text"], scale=line_scale)
            yy += line_height

    for current, nxt in zip(boxes, boxes[1:]):
        x1 = current[0] + current[2]
        y1 = current[1] + current[3] // 2
        x2 = nxt[0]
        y2 = nxt[1] + nxt[3] // 2
        canvas.draw_arrow(x1, y1, x2, y2, spec["stroke"])

    canvas.save_png(OUTPUT_DIR / f"{spec['name']}.png")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for spec in FLOWCHARTS:
        render_flowchart(spec)
        print(f"Arquivo gerado: {OUTPUT_DIR / (spec['name'] + '.png')}")


if __name__ == "__main__":
    main()
