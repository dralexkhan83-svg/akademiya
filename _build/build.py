#!/usr/bin/env python3
"""Собирает сайт Академии ортопедов Dental Profi из папки «Академия».

Запуск: python3 _build/build.py /mnt/project-files/Академия
Результат пишется в корень репозитория (index.html, blok-*/, assets/).
Папки «02 Ученики» и всё с данными пациентов сюда не попадают намеренно.
"""
import html
import io
import re
import shutil
import subprocess
import sys
from pathlib import Path

import openpyxl
from PIL import Image

SRC = Path(sys.argv[1] if len(sys.argv) > 1 else "/mnt/project-files/Академия")
OUT = Path(__file__).resolve().parent.parent
UB = SRC / "01 Учебные блоки"
LOGO = SRC / "00 Контекст собственника" / "Логотип Денталь Профи"

B1 = UB / "Блок 1. Второй ассистент"
B2 = UB / "Блок 2. Диагностика и план лечения"
B3 = UB / "Блок 3. Методология дизайна улыбки (VSD)"
B4 = UB / "Блок 4. Философия и мышление Денталь Профи"
B5 = UB / "Блок 5. Препарирование под различные виды констуркций"
B6 = UB / "Блок 6. Стандарты и протоколы Dental Profi"
B4W = B4 / "Исходники Word"
B6P = B6 / "05 Протоколы ортопедических приёмов Dental Profi"

# kind: docx | pdftext | pdfpages | image | html | xlsx
BLOCKS = [
    {
        "n": 1, "title": "Второй ассистент",
        "lead": "Первый этап: работа вторым ассистентом, фотопротокол и оформление первичного пациента.",
        "items": [
            ("pravila-raboty", "Правила работы", "Прочитать в первую очередь", "docx", B1 / "1. ПРАВИЛА РАБОТЫ - ПРОЧИТАТЬ В ПЕРВУЮ ОЧЕРЕДЬ.docx"),
            ("kriterii-etapa", "Критерии успешного прохождения этапа", "", "docx", B1 / "3. Критерии успешного прохождения этапа.docx"),
            ("fotoprotokol", "Стандарт фотопротокола", "Требования и порядок снимков", "pdftext", B1 / "4. Стандарты фотопротокола Денталь Профи.pdf"),
            ("pervichnyy-pacient", "Правила оформления первичного пациента", "Памятка для врача, ассистента и координатора", "image", B1 / "6. Изменения в методологии. Шаблоны" / "Правила_оформления_первичного_пациента.png"),
            ("treker-navykov", "Трекер навыков второго ассистента", "Интерактивная самооценка, допуск к следующему блоку", "html", B1 / "6. Изменения в методологии. Шаблоны" / "Трекер навыков — блок 1.html"),
        ],
    },
    {
        "n": 2, "title": "Диагностика и план лечения",
        "lead": "Мышление врача, чтение КТ и составление комплексного плана лечения.",
        "items": [
            ("myshlenie-vracha", "Мышление врача и принципы принятия решений", "Урок 1", "docx", B2 / "Исходники Word" / "1. Мышление врача и принципы принятия решений Денталь Профи.docx"),
            ("chtenie-kt", "Правила чтения КТ", "Урок 2", "docx", B2 / "Исходники Word" / "2. Правила чтения КТ.docx"),
            ("diagnostika-planirovanie", "Диагностика и планирование комплексной реабилитации", "Урок 3", "docx", B2 / "Исходники Word" / "3. Диагностика и планирование комплексной реабилитации Денталь Профи.docx"),
            ("zadanie-blok-2", "Задание после блока", "Урок 5", "docx", B2 / "Исходники Word" / "5. Задание после блока Диагностика и составление плана лечения..docx"),
            ("dopolnenie-plana", "Правило дополнения плана лечения", "", "docx", B2 / "Правило дополнения плана лечения ДП.docx"),
            ("shema-bloka-2", "Схема блока: диагностика и планирование", "Вся логика блока на одном листе", "image", B2 / "7. Диагностика и планирование Dental Profi.png"),
            ("process-plana", "Процесс создания плана лечения", "От первичной консультации до выдачи плана", "html", B2 / "Алгоритм составления плана по новому конструктору" / "Схема — процесс создания плана лечения.html"),
        ],
    },
    {
        "n": 3, "title": "Методология дизайна улыбки (VSD)",
        "lead": "Virtual Smile Design: от фотопротокола к клинической гипотезе и управляемому эстетическому результату.",
        "items": [
            ("metodologiya-vsd", "Методология дизайна улыбки (VSD)", "", "docx", B3 / "Исходники Word" / "1. Методология дизайна улыбки Денталь Профи (VSD).docx"),
            ("shema-vsd", "Методология VSD: блок-схема", "", "image", B3 / "5. Методология VSD Денталь Профи (блок-схема).png"),
        ],
    },
    {
        "n": 4, "title": "Философия и мышление Денталь Профи",
        "lead": "Ресурсы специалиста, миссия, ценности клиники и правила коммуникации.",
        "items": [
            ("filosofiya-kratko", "Философия роста врача: методичка", "7 ресурсов специалиста", "docx", B4W / "7 ресурсов" / "Методичка. Философия роста врача Денталь Профи.docx"),
            ("filosofiya-polnaya", "Философия роста врача: полная версия", "7 ресурсов специалиста", "docx", B4W / "7 ресурсов" / "Философия роста врача (полная версия).docx"),
            ("missiya", "Миссия Денталь Профи", "", "docx", B4W / "Миссия Денталь Профи" / "Миссия Денталь Профи.docx"),
            ("cennosti", "Корпоративные ценности и философия", "", "docx", B4W / "Корпоративные ценности и философия  Денталь Профи" / "Корпоративные ценности и философия  Денталь Профи.docx"),
            ("kkc", "Ключевые клиентские ценности", "За что нас ценят", "docx", B4W / "ККЦ" / "Ключевые клиентские ценности или За что нас ценят.docx"),
            ("kommunikaciya", "Правила коммуникации", "", "docx", B4W / "Правила коммуникации" / "Правила коммуникации Денталь Профи.docx"),
            ("s-assistentom", "Взаимоотношения внутри команды", "Работа с ассистентом", "docx", B4W / "Взаимоотношения с ассистентом" / "Взаимоотношения внутри команды (с ассистентом).docx"),
        ],
    },
    {
        "n": 5, "title": "Препарирование под различные виды конструкций",
        "lead": "Коронки, накладки, виниры: последовательность действий, ретракция и практическое задание.",
        "items": [
            ("konspekt-preparirovanie", "Препарирование и ретракция: конспект", "Конспект к шести видео Александра Хана", "pdfpages", B5 / "8. Препарирование и ретракция - конспект.pdf"),
            ("zadanie-preparirovanie", "Практическое задание: препарирование зубов", "", "pdfpages", B5 / "7. Практическое задание - препарирование зубов.pdf"),
        ],
    },
    {
        "n": 6, "title": "Стандарты и протоколы Dental Profi",
        "lead": "Стандарты качества, работа с лабораторией, анестезия и протоколы ортопедических приёмов.",
        "draft": "Редакция от 1 октября 2026 года. Блок ещё не утверждён как клинический стандарт.",
        "items": [
            ("standarty-kachestva", "Стандарты качества", "", "docx", B6 / "01 Стандарты качества" / "Стандарты качества Dental Profi.docx"),
            ("vybor-materiala", "Сравнительная характеристика материалов", "Таблица", "xlsx", B6 / "02 Сравнение методов и материалов" / "Сравнительная характеристика материалов.xlsx"),
            ("vkladki-metody", "Прямой и непрямой методы изготовления вкладки", "Таблица", "xlsx", B6 / "02 Сравнение методов и материалов" / "Прямой и непрямой методы изготовления вкладки — сравнение.xlsx"),
            ("fiksaciya-implanty", "Критерии фиксации на имплантах", "Таблица", "xlsx", B6 / "02 Сравнение методов и материалов" / "Критерии фиксации на имплантах.xlsx"),
            ("zubotehnicheskie-standarty", "Зуботехнические стандарты", "Правила работы с лабораторией", "docx", B6 / "03 Зуботехнические стандарты" / "Зуботехнические стандарты Dental Profi — правила работы с лабораторией.docx"),
            ("anesteziya", "Методология инфильтрационной и мандибулярной анестезии", "Редакция 1.1", "docx", B6 / "04 Анестезия" / "Методология инфильтрационной и мандибулярной анестезии Dental Profi v1.1.docx"),
            ("perechen-protokolov", "Перечень ортопедических протоколов", "", "docx", B6P / "Перечень ортопедических протоколов Dental Profi.docx"),
            ("protokoly-priemov", "Протоколы ортопедических приёмов", "Основной документ", "docx", B6P / "Протоколы ортопедических приёмов Dental Profi.docx"),
            ("protokoly-assistenta", "Протоколы ассистента на ортопедическом приёме", "", "docx", B6P / "Протоколы ассистента на ортопедическом приёме Dental Profi.docx"),
        ],
    },
]

# Логотип клиники вставлен в начало документов блока 6 и VSD – на сайте он уже есть в шапке.
DROP_LOGO_IMAGES = {"metodologiya-vsd"} | {s for s, *_ in BLOCKS[5]["items"]}

e = html.escape


def page(title, body, depth, desc=""):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc or 'Учебные материалы Академии ортопедов Dental Profi')}">
<link rel="icon" href="{up}assets/mark.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/style.css">
</head>
<body>
<header class="top"><div class="wrap">
<a class="brand" href="{up}index.html"><img src="{up}assets/logo.png" alt="Денталь Профи"><span>Академия ортопедов</span></a>
<nav><a href="{up}index.html#bloki">Учебные блоки</a></nav>
</div></header>
<main>
{body}
</main>
<footer class="foot"><div class="wrap">Академия ортопедов Dental Profi · учебные материалы</div></footer>
</body>
</html>
"""


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, **kw)


def docx_html(src, slug, outdir, drop_logo):
    media = outdir / "media" / slug
    if media.exists():
        shutil.rmtree(media)
    r = run(["pandoc", str(src), "-t", "html5", "--wrap=none", f"--extract-media={media}"], text=True)
    out = r.stdout
    out = out.replace(str(media) + "/", f"media/{slug}/")
    # сжать картинки из Word: инфографика в PNG весит по 1.5 МБ
    for p in list(media.rglob("*")):
        if p.suffix.lower() in (".png", ".jpg", ".jpeg"):
            im = Image.open(p).convert("RGB")
            im.thumbnail((1800, 4000))
            jp = p.with_suffix(".jpg")
            p.unlink()
            im.save(jp, quality=85, optimize=True)
            rel = str(p.relative_to(outdir))
            out = out.replace(rel, str(jp.relative_to(outdir)))
    if drop_logo:
        out = re.sub(r"<p>\s*<img [^>]*>\s*</p>|<img [^>]*>", "", out, count=1)
        if media.exists():
            shutil.rmtree(media)
    out = re.sub(r'(<img )', r'\1loading="lazy" ', out)
    # первый заголовок Word дублирует название страницы – понижаем все h1 до h2
    out = re.sub(r"<(/?)h1", r"<\1h2", out)
    out = re.sub(r"<colgroup>.*?</colgroup>", "", out, flags=re.S)
    # таблица в одну колонку в Word – это выноска
    def callout(m):
        t = m.group(0)
        if t.count("<th") + t.count("<td") <= 2 and "<tr" in t and t.count("<tr") <= 2:
            inner = re.sub(r"</?(table|thead|tbody|tr|th|td)[^>]*>", "", t)
            return f'<div class="callout">{inner.strip()}</div>'
        if len(re.findall(r"<th[ >]", t.split("</tr>")[0])) > 3:
            t = t.replace("<table>", '<table class="many">', 1)
        return f'<div class="tablewrap">{t}</div>'
    out = re.sub(r"<table>.*?</table>", callout, out, flags=re.S)
    return out


def photoprotocol_html(src):
    """Текст стандарта фотопротокола. В PDF он перемешан со снимками пациента, поэтому
    структура задана здесь, а слова сверяются с PDF: если в PDF фразы нет, сборка падает."""
    pdf = re.sub(r"\s+", " ", run(["pdftotext", str(src), "-"], text=True).stdout)
    intro = ("Фотопротокол – обязательная часть диагностики, планирования лечения, контроля качества, "
             "диспансерного приема, внутренней коммуникации между врачами и формирования клинической "
             "документации. Стандартизированные фотографии позволяют объективно анализировать клиническую "
             "ситуацию, отслеживать динамику лечения и формировать единый профессиональный подход внутри "
             "команды. Фотопротокол входит в стандарт качества «Денталь Профи» и обязателен для выполнения "
             "всеми врачами клиники.")
    general = ["Все фотографии должны быть четкими, светлыми и без пересвета.",
               "Фотографии должны быть выровнены по горизонтали и вертикальной оси.",
               "Необходимо убрать все лишнее из кадра.",
               "На фото должны быть хорошо видны зубы, окклюзия и мягкие ткани.",
               "Зеркала должны быть чистыми, без запотевания и разводов.",
               "Перед съемкой необходимо убрать слюну и пузырьки воздуха.",
               "Фотографии загружаются в папку пациента в день приема."]
    intra = ["Фронтальная проекция в привычном прикусе",
             "Фронтальная проекция в приоткрытом состоянии",
             "Правая (пациента) боковая проекция в привычном прикусе (должно быть видно смыкание клыков и первых моляров)",
             "Левая (пациента) боковая проекция в привычном прикусе (должно быть видно смыкание клыков и первых моляров)",
             "Верхний зубной ряд (слева от нас – правая сторона пациента, и наоборот, как на ОПТГ, должны быть видны все зубы)",
             "Нижний зубной ряд (слева от нас – правая сторона пациента, и наоборот, как на ОПТГ, должны быть видны все зубы)",
             "Язычная поверхность нижних фронтальных зубов"]
    portrait_lead = ("В стандарт портретного фотопротокола входят 8 последовательных фотографий (дополнения "
                     "могут быть при ортодонтической диагностике и цифровом дизайне улыбки):")
    portrait = ["Лицо анфас в покое", "Лицо анфас с приоткрытым ртом", "Лицо анфас с легкой улыбкой",
                "Лицо анфас с максимально широкой улыбкой", "Поворот 45 градусов вправо",
                "Поворот 45 градусов влево", "Лицо в профиль в покое", "Лицо в профиль в улыбке"]
    for frag in [intro, portrait_lead, *general, *intra, *portrait]:
        assert frag in pdf, f"фраза не найдена в PDF фотопротокола: {frag[:60]}"
    li = lambda xs: "".join(f"<li>{e(x)}</li>" for x in xs)
    return f"""<div class="callout">Примеры снимков есть в исходном документе. На открытом сайте их нет, потому что на них пациент.</div>
<p>{e(intro)}</p>
<h2>Общие требования</h2><ul>{li(general)}</ul>
<h2>Внутриротовой фотопротокол</h2><p>Состоит из 7 последовательных фотографий:</p><ol>{li(intra)}</ol>
<h2>Портретный фотопротокол</h2><p>{e(portrait_lead)}</p><ol>{li(portrait)}</ol>"""


def pdf_pages_html(src, slug, outdir):
    media = outdir / "media" / slug
    if media.exists():
        shutil.rmtree(media)
    media.mkdir(parents=True)
    run(["pdftoppm", "-r", "130", "-png", str(src), str(media / "p")])
    parts = []
    for i, p in enumerate(sorted(media.glob("p*.png")), 1):
        im = Image.open(p).convert("RGB")
        jp = p.with_suffix(".jpg")
        im.save(jp, quality=85, optimize=True)
        p.unlink()
        parts.append(f'<img class="sheet" loading="lazy" src="media/{slug}/{jp.name}" alt="Страница {i}">')
    pdf = media / f"{slug}.pdf"
    shutil.copy(src, pdf)
    return (f'<p><a class="btn" href="media/{slug}/{slug}.pdf" download>Скачать PDF</a></p>'
            + "\n".join(parts))


def image_html(src, slug, outdir):
    media = outdir / "media" / slug
    media.mkdir(parents=True, exist_ok=True)
    im = Image.open(src).convert("RGB")
    full = media / f"{slug}.jpg"
    im2 = im.copy()
    im2.thumbnail((3200, 3200))
    im2.save(full, quality=86, optimize=True)
    return (f'<a href="media/{slug}/{slug}.jpg" target="_blank" rel="noopener">'
            f'<img class="sheet" src="media/{slug}/{slug}.jpg" alt=""></a>'
            f'<p class="hint">Нажмите на изображение, чтобы открыть его в полном размере.</p>')


def xlsx_html(src):
    wb = openpyxl.load_workbook(src, data_only=True)
    out = []
    for ws in wb:
        rows = [[c.value for c in r] for r in ws.iter_rows()]
        rows = [r for r in rows if any(v not in (None, "") for v in r)]
        if not rows:
            continue
        out.append(f"<h2>{e(ws.title)}</h2>")
        # строки с одним значением сверху – подзаголовки листа
        while rows and sum(v not in (None, "") for v in rows[0]) == 1:
            v = next(v for v in rows[0] if v not in (None, ""))
            if ws.title != rows[0][0] and v != ws.title:
                out.append(f'<p class="lead-sm">{e(str(v))}</p>')
            rows.pop(0)
        if not rows:
            continue
        head, *body = rows
        def cell(v):
            s = "" if v is None else str(v)
            if s.startswith("http"):
                return f'<a href="{e(s)}" target="_blank" rel="noopener">ссылка</a>'
            return e(s)
        cls = ' class="many"' if len(head) > 3 else ""
        t = f"<table{cls}><thead><tr>" +"".join(f"<th>{cell(v)}</th>" for v in head) + "</tr></thead><tbody>"
        t += "".join("<tr>" + "".join(f"<td>{cell(v)}</td>" for v in r) + "</tr>" for r in body)
        out.append(f'<div class="tablewrap">{t}</tbody></table></div>')
    return "\n".join(out)


def main():
    for d in OUT.glob("blok-*"):
        shutil.rmtree(d)
    assets = OUT / "assets"
    assets.mkdir(exist_ok=True)
    for name, dst, w in (("синий логотип.png", "logo.png", 360), ("синий знак.png", "mark.png", 128),
                         ("белый логотип.png", "logo-white.png", 520)):
        im = Image.open(LOGO / name)
        im.thumbnail((w, w))
        im.save(assets / dst, optimize=True)

    cards = []
    for b in BLOCKS:
        n = b["n"]
        bdir = OUT / f"blok-{n}"
        bdir.mkdir(parents=True)
        rows = []
        for slug, title, sub, kind, src in b["items"]:
            if kind == "html":
                shutil.copy(src, bdir / f"{slug}.html")
                href = f"{slug}.html"
            else:
                if kind == "docx":
                    content = docx_html(src, slug, bdir, slug in DROP_LOGO_IMAGES)
                elif kind == "pdftext":
                    content = photoprotocol_html(src)
                elif kind == "pdfpages":
                    content = pdf_pages_html(src, slug, bdir)
                elif kind == "image":
                    content = image_html(src, slug, bdir)
                elif kind == "xlsx":
                    content = xlsx_html(src)
                draft = f'<div class="draft">{e(b["draft"])}</div>' if b.get("draft") else ""
                body = f"""<div class="wrap doc">
<p class="crumbs"><a href="../index.html">Академия</a> · <a href="index.html">Блок {n}. {e(b['title'])}</a></p>
<h1>{e(title)}</h1>
{f'<p class="sub">{e(sub)}</p>' if sub else ''}
{draft}
<article class="content{' wide' if kind in ('image', 'xlsx') else ''}">
{content}
</article>
<p class="back"><a href="index.html">← Все материалы блока {n}</a></p>
</div>"""
                (bdir / f"{slug}.html").write_text(page(f"{title} · Академия Dental Profi", body, 1), encoding="utf-8")
                href = f"{slug}.html"
            rows.append(f'<li><a href="{href}"><span class="i">{len(rows) + 1:02d}</span>'
                        f'<span class="t">{e(title)}{f"<small>{e(sub)}</small>" if sub else ""}</span>'
                        f'<span class="arr">→</span></a></li>')
        draft = f'<div class="draft">{e(b["draft"])}</div>' if b.get("draft") else ""
        body = f"""<section class="bhero"><div class="wrap">
<p class="crumbs"><a href="../index.html">Академия</a></p>
<p class="kicker">Блок {n}</p>
<h1>{e(b['title'])}</h1>
<p class="lead">{e(b['lead'])}</p>
</div></section>
<div class="wrap">{draft}<ol class="mats">{''.join(rows)}</ol></div>"""
        (bdir / "index.html").write_text(page(f"Блок {n}. {b['title']} · Академия Dental Profi", body, 1, b["lead"]), encoding="utf-8")
        cards.append(f'<a class="card" href="blok-{n}/index.html"><span class="num">{n}</span>'
                     f'<h3>{e(b["title"])}</h3><p>{e(b["lead"])}</p>'
                     f'<span class="meta">{len(b["items"])} материалов{" · черновик" if b.get("draft") else ""}</span></a>')

    body = f"""<section class="hero"><div class="wrap">
<p class="kicker">Денталь Профи · центр восстановления улыбок</p>
<h1>Академия ортопедов</h1>
<p class="lead">Учебная программа клиники: от работы вторым ассистентом до самостоятельного ведения комплексной ортопедической реабилитации. Блоки проходятся по порядку.</p>
<a class="btn light" href="blok-1/index.html">Начать с блока 1</a>
</div></section>
<section class="wrap" id="bloki">
<h2 class="sec">Учебные блоки</h2>
<div class="grid">{''.join(cards)}</div>
</section>"""
    (OUT / "index.html").write_text(page("Академия ортопедов Dental Profi", body, 0), encoding="utf-8")
    (OUT / ".nojekyll").write_text("")


if __name__ == "__main__":
    main()
