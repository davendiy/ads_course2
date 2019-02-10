#!/usr/bin/env python3
# -*-encoding: utf-8-*-

"""
Торговець володіє трьома видами товарів: алмази, яблука та шовк.
Для кожного товару відомо вартість у золотих монетах за одиницю ваги та його кількість у торговця.

В країні, де живе торговець, є N міст, які пронумеровані від 1 до N.
Рідне місто торговця має номер 1, а столиця - номер N.
Щоб дістатися столиці, де торговець може продати товар, йому потрібно проїхати
певним маршрутом через інші міста. Між деякими парами міст існують дороги,
проїзд по яким коштує певної кількості золотих.
У кожному місті стягується податок за провезення кожного з видів товару,
заданий у відсотках від вартості провезеного через місто товару.
Відомо, що виїхавши з будь-якого міста, торговець не може до нього повернутися.
Будь-які два міста з’єднані не більше ніж однією дорогою.

Задача торговця отримати найбільший прибуток – різницю отриманих у столиці коштів
за проданий товар та витрат за подорож до столиці.
Він не зобов’язаний брати з собою весь свій товар.
Торговець завжди має достатньо золотих для виплати податків, та не може розрахуватися товаром,
який він везе до столиці. Усі дороги ведуть лише в одному напрямку.

Напишіть програму, що за інформацією про кількість одиниць ваги різних видів товару у торговця,
ціни на ці товари у столиці, податки у містах,
дороги між містами та вартість проїзду по цих дорогах встановить максимальний прибуток,
що може отримати торговець від реалізації товару.

Вхідні дані

Перший рядок містить два цілих числа N (2 ≤ N ≤ 500) та M (M ≥ 1) - кількість міст та доріг між ними.
Другий рядок містить три цілих невід’ємних числа,
що відповідають кількостям одиниць ваги алмазів, яблук та шовку, що належать торговцю.
Третій рядок містить три цілих невід’ємних числа - вартість одиниці ваги алмазів, яблук та шовку відповідно.
Наступні рядки з 4-го по N + 1 містять по три цілих числа від 0 до 100 включно,
що відповідають відсоткам від вартості алмазів, яблук та шовку,
що стягується у відповідно у містах від 2 до N - 1 у якості податку.
У списку міст не враховані рідне місто торговця 1 та столиця N, як такі, що не стягують податок.
Наступні M рядків містять по три цілих невід’ємних числа, перші два з яких від 1 до N задають пару міст,
між якими прокладено дорогу, а третє - вартість проїзду цією дорогою.
Дороги ведуть в напрямку від міста, яке вказано першим, до того, яке вказано другим.
Кількості одиниць ваги кожного з видів товару у торговця,
вартості товарів та ціни проїзду по дорогам не перевищують 100.

Вихідні дані

Вивести одне число - точне значення знайденого максимального прибутку від поїздки до столиці.
Відповідь завжди повинна містити рівно два знаки після крапки.
У випадках коли торговець не може отримати прибутку чи дістатися столиці існуючими дорогами, потрібно вивести 0.00
"""