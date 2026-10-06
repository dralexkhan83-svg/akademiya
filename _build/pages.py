"""Страницы входа и кабинетов. Тексты взяты из материалов Академии:
критерии этапа и трекер навыков (блок 1), экзамен, справочник §5 и §11.3, журнал изменений."""
import html

e = html.escape

DEMO_NOTE = ('<div class="draft">Вход пока учебный: он запоминает вас только в этом браузере и не закрывает '
             'страницы от посторонних. Поэтому здесь нет данных пациентов, консультаций и цен.</div>')

ROLES = [
    ("uchenik", "Ученик", "Стажёр и будущий врач-ортопед",
     "Маршрут обучения, отметки об изученном, задания, экзамен и паспорт ученика."),
    ("kurator", "Куратор", "Старший ортопед",
     "Поддержка, проверка планов, приём экзаменов, обратная связь и решение о допуске."),
    ("rukovoditel", "Руководитель Академии", "Клиническая логика и утверждение материалов",
     "Статус блоков, слои учебного материала, модель Академии и журнал изменений."),
]


def role_cards(up):
    return "".join(
        f'<a class="card" href="{up}kabinet/{k}.html"><span class="num">{i}</span><h3>{e(t)}</h3>'
        f'<p><b>{e(who)}.</b> {e(what)}</p><span class="meta">Открыть кабинет</span></a>'
        for i, (k, t, who, what) in enumerate(ROLES, 1))


def hero(kicker, title, lead, crumbs=True):
    c = '<p class="crumbs"><a href="../index.html">Академия</a> · <a href="../kabinety.html">Кабинеты</a></p>' if crumbs else ""
    return (f'<section class="bhero"><div class="wrap">{c}<p class="kicker">{e(kicker)}</p>'
            f'<h1>{e(title)}</h1><p class="lead">{e(lead)}</p>'
            f'<p class="who" data-who></p></div></section>')


def section(title, inner, sid=""):
    return f'<section class="panel"{f" id={sid!r}" if sid else ""}><h2>{e(title)}</h2>{inner}</section>'


def ul(xs):
    return "<ul>" + "".join(f"<li>{x}</li>" for x in xs) + "</ul>"


def chain(xs):
    return '<ol class="chain">' + "".join(f"<li>{e(x)}</li>" for x in xs) + "</ol>"


def links(xs):
    return '<ul class="links">' + "".join(
        f'<li><a href="../{h}">{e(t)}</a>{f"<small>{e(s)}</small>" if s else ""}</li>' for h, t, s in xs) + "</ul>"


def field(fid, label, rows=3, hint=""):
    return (f'<label class="fld"><span>{e(label)}</span>'
            f'{f"<small>{e(hint)}</small>" if hint else ""}'
            f'<textarea data-save="{fid}" rows="{rows}"></textarea></label>')


def vhod():
    roles = "".join(
        f'<label class="role"><input type="radio" name="role" value="{k}"{" checked" if i == 0 else ""}>'
        f'<span><b>{e(t)}</b><small>{e(who)}</small></span></label>'
        for i, (k, t, who, _) in enumerate(ROLES))
    return f"""<section class="bhero"><div class="wrap"><p class="kicker">Академия ортопедов</p>
<h1>Вход</h1><p class="lead">Выберите свою роль, и сайт откроет ваш кабинет.</p></div></section>
<div class="wrap narrow">
<form class="panel login" id="login-form">
<label class="fld"><span>Как к вам обращаться</span><input name="name" autocomplete="name" placeholder="Имя и фамилия"></label>
<fieldset><legend>Роль</legend>{roles}</fieldset>
<button class="btn" type="submit">Войти</button>
<button class="btn ghost" type="button" id="logout">Выйти</button>
</form>
{DEMO_NOTE}
</div>"""


def kabinety():
    return f"""<section class="bhero"><div class="wrap"><p class="crumbs"><a href="index.html">Академия</a></p>
<p class="kicker">Академия ортопедов</p><h1>Кабинеты</h1>
<p class="lead">У каждой роли в Академии свой кабинет: ученик проходит маршрут, куратор проверяет и принимает решения о допуске, руководитель отвечает за методологию.</p></div></section>
<div class="wrap">
<div class="grid three">{role_cards("")}</div>
{section("Путь в Академии", chain(["Отбор", "Обучение и проверка навыков", "Доказательное портфолио", "Выход на рынок труда", "Связь и кадровый резерв"])
         + "<p>Академия готовит специалистов и кадровый резерв клиник Dental Profi. Просмотр материала, правильный ответ на экзамене и освоенная клиническая работа – разные результаты, и каждый проверяется отдельно.</p>")}
{DEMO_NOTE}
<p><a class="btn" href="vhod.html">Войти</a></p>
</div>"""


def uchenik():
    route = chain([
        "Этап 1. Второй ассистент: 1–2 месяца, 5–10 смен с куратором",
        "Промежуточный экзамен и отбор по трекеру навыков",
        "Допуск к стажировке: проходной балл, одобрение куратора, стабильные KPI",
        "Блоки 2–5: теория, задания, экзамен",
        "Самостоятельные планы лечения и цифровой дизайн улыбки",
        "Паспорт ученика и портфолио",
    ])
    stage1 = ul([
        "<b>Подэтап 1 (2–4 смены).</b> База данных, фотопротокол всех пациентов, история болезни, приглашение и проводы пациента, рекомендации, передача администраторам информации о следующих записях, мелкие клинические поручения.",
        "<b>Подэтап 2 (3–6 смен).</b> По одному клиническому кейсу на каждый приём: предварительный диагноз и план лечения. Обучение составлению планов, частично общение с пациентами, ежедневный разбор одной ошибки.",
    ]) + "<p>Порядок допуска после этапа уточняет куратор.</p>"
    tasks = links([
        ("blok-1/treker-navykov.html", "Трекер навыков второго ассистента", "Отмечайте только то, что стало нормой"),
        ("blok-1/karta-konsultacii.html", "Карта первичной консультации", "Рабочая форма"),
        ("blok-2/zadanie-blok-2.html", "Задание после блока 2", "Самостоятельные комплексные планы лечения"),
        ("blok-5/zadanie-preparirovanie.html", "Практическое задание: препарирование", "Два комплекта моделей, сдача наставнику"),
    ])
    passport = ('<p>Паспорт показывает, что вы действительно умеете. В нём различаются выполненные работы, ваш '
                'личный вклад, подтверждённые навыки и то, где ещё нужен контроль.</p>'
                + field("pass-works", "Выполненные работы", 4, "Что сделано: планы лечения, VSD, препарирование на моделях, ассистирование")
                + field("pass-role", "Личный вклад", 3, "Что именно сделали вы, а что – куратор или команда")
                + field("pass-skills", "Подтверждённые навыки", 3, "Кто и когда подтвердил")
                + field("pass-control", "Где нужен контроль", 3, "Что пока делаете только под присмотром куратора")
                + '<p class="actions"><button class="btn" type="button" onclick="window.print()">Распечатать паспорт</button>'
                  '<span class="saved" data-saved></span></p>')
    return f"""{hero("Кабинет", "Кабинет ученика", "Ваш маршрут по Академии, отметки об изученном и задания.")}
<div class="wrap">
{DEMO_NOTE}
{section("Мой прогресс", '<div id="progress"></div><p class="hint left">Отметки ставятся кнопкой «Изучено» на странице материала или здесь.</p>', "progress-sec")}
{section("Маршрут", route)}
{section("Этап 1. Второй ассистент", stage1)}
{section("Задания и проверка", tasks)}
{section("Паспорт ученика", passport, "pasport")}
</div>
<script src="../assets/catalog.js"></script>"""


def kurator():
    duties = ul(["Поддержка ученика на приёме и между сменами", "Проверка планов лечения", "Приём экзаменов",
                 "Обратная связь: принял, внедрил, улучшил", "Решение о допуске к следующему этапу"])
    review = ('<p>Разбор ответа ученика: что понято, где пробел, что повторить, что доработать и какие вопросы '
              'помогут закрепить материал. Черновик сохраняется в этом браузере.</p>'
              + '<div class="two">'
              + '<label class="fld"><span>Ученик</span><input data-save="rv-student"></label>'
              + '<label class="fld"><span>Материал или задание</span><input data-save="rv-topic"></label></div>'
              + field("rv-total", "Общий результат", 2)
              + field("rv-strong", "Сильные стороны", 3)
              + field("rv-gaps", "Пробелы", 3)
              + field("rv-repeat", "Что повторить", 2)
              + field("rv-redo", "Что доработать", 2)
              + field("rv-questions", "Вопросы на закрепление", 3, "Только по выявленным пробелам")
              + '<p class="actions"><button class="btn" type="button" id="copy-review">Скопировать разбор</button>'
                '<button class="btn ghost" type="button" id="clear-review">Очистить</button><span class="saved" data-saved></span></p>')
    tools = links([
        ("blok-1/treker-navykov.html", "Трекер навыков", "Оценка куратора и самооценка"),
        ("blok-1/karta-konsultacii.html", "Карта первичной консультации", "Рабочая форма"),
        ("blok-2/process-plana.html", "Процесс создания плана лечения", ""),
    ])
    students = ('<p>Список учеников, их консультации и разборы появятся здесь, когда у сайта будет настоящий '
                'закрытый вход. На открытом сайте их показывать нельзя: в консультациях данные пациентов.</p>')
    return f"""{hero("Кабинет", "Кабинет куратора", "Проверка, обратная связь и решение о допуске.")}
<div class="wrap">
{DEMO_NOTE}
{section("Задачи куратора", duties)}
{section("Разбор ответа ученика", review, "razbor")}
{section("Инструменты проверки", tools)}
{section("Мои ученики", students)}
</div>"""


def rukovoditel(blocks, journal):
    rows = "".join(
        f'<tr><td><a href="../blok-{b["n"]}/index.html">Блок {b["n"]}. {e(b["title"])}</a></td>'
        f'<td>{len(b["items"])}</td><td>{"<span class=tag-draft>на утверждении</span>" if b.get("draft") else "<span class=tag-ok>действует</span>"}</td></tr>'
        for b in blocks)
    status = f'<div class="tablewrap"><table><thead><tr><th>Блок</th><th>Материалов</th><th>Статус</th></tr></thead><tbody>{rows}</tbody></table></div>'
    layers = """<div class="tablewrap"><table><thead><tr><th>Слой</th><th>Что он должен дать</th></tr></thead><tbody>
<tr><td>Принцип</td><td>Что понять и зачем</td></tr>
<tr><td>Методология</td><td>Как рассуждать и выбирать действие</td></tr>
<tr><td>Стандарт</td><td>Какие требования соблюдать</td></tr>
<tr><td>Шаблон</td><td>В какой форме выполнить работу</td></tr>
<tr><td>Задание</td><td>Как проявить понимание или навык</td></tr>
<tr><td>Проверка</td><td>По каким критериям принять работу или отправить на доработку</td></tr>
</tbody></table></div>"""
    model = ("<p>Академия нужна прежде всего для подготовки специалистов и кадрового резерва собственных клиник и будущего "
             "роста сети. Внешняя продажа курсов не основная цель.</p>"
             + chain(["Мышление и принципы", "Чтение КТ и анализ данных", "Диагностика и планирование комплексной реабилитации",
                      "Видеоразборы", "Самостоятельные планы лечения"])
             + "<p>Новые клинические дополнения оформляются как предложения на утверждение, а не как принятая методология. "
               "Изменение методологии отражается в обучении, карте консультации и анализаторе и записывается в журнал изменений.</p>")
    return f"""{hero("Кабинет", "Кабинет руководителя Академии", "Методология, статус материалов и журнал изменений.")}
<div class="wrap">
{DEMO_NOTE}
{section("Статус учебных блоков", status)}
{section("Модель Академии", model)}
{section("Слои учебного материала", layers)}
{section("Журнал изменений", f'<div class="content flat">{journal}</div>', "zhurnal")}
</div>"""


def build(blocks, journal):
    return [
        ("vhod.html", "Вход · Академия Dental Profi", vhod(), 0),
        ("kabinety.html", "Кабинеты · Академия Dental Profi", kabinety(), 0),
        ("kabinet/uchenik.html", "Кабинет ученика · Академия Dental Profi", uchenik(), 1),
        ("kabinet/kurator.html", "Кабинет куратора · Академия Dental Profi", kurator(), 1),
        ("kabinet/rukovoditel.html", "Кабинет руководителя · Академия Dental Profi", rukovoditel(blocks, journal), 1),
    ]


def home_extra():
    return f"""<section class="wrap" id="kabinety">
<h2 class="sec">Кабинеты</h2>
<div class="grid three">{role_cards("")}</div>
</section>"""
