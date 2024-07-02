async def get_prompt_news(text):
    prompt = f"""Перепиши следующий текст для канала Gambler Pepe | NEWS:

{text}

Инструкции:
1. Начни с приветствия: "Доброе время суток, уважаемые криптаны, Пепе вещает! 🐸" (или подобное, упоминая Pepe).
2. Используй HTML-форматирование ОБЯЗАТЕЛЬНО:
   - Жирный текст: <b>пример</b>
   - Курсив: <i>пример</i>
   - Спойлер: <tg-spoiler>пример</tg-spoiler>
3. Добавь разнообразные эмодзи по тематики (минимум 3-5 разных).
4. Перепиши текст, сохраняя всю информацию, но изменяя структуру и используя синонимы.
5. Сделай текст официальным, но с намеком на неформальность.
6. Измени порядок информации, сохраняя смысл.
7. Добавь HTML-форматирование к ключевым фразам и числам.
8. ОБЯЗАТЕЛЬНО: Итоговый текст должен содержать не более 950 символов. Это критически важно!
9. НЕ добавляй никаких примечаний или комментариев от себя в конце текста.

Пример форматирования:
<b>Важная новость!</b> 🚀 Криптомир снова <i>удивляет</i>... <tg-spoiler>Вы не поверите, что произошло!</tg-spoiler>

Помни: текст должен быть уникальным, информативным и привлекательным для читателей, но не превышать 950 символов."""
    return prompt

async def get_prompt_sol(text):
    prompt = f"""Перепиши следующий текст для канала Gambler Pepe | SOL:

{text}

Инструкции:
1. Начни с уникального приветствия, упоминая Pepe и SOL. Например: "Солана-мафия, Пепе на связи! 🐸☀️"
2. ОБЯЗАТЕЛЬНО используй HTML-форматирование:
   - Жирный текст: <b>пример</b>
   - Курсив: <i>пример</i>
   - Спойлер: <tg-spoiler>пример</tg-spoiler>
3. Добавь разнообразные эмодзи по тематики (минимум 5-7 разных).
4. Начни с провокационного заявления или вопроса.
5. Перепиши текст, сохраняя информацию, но меняя структуру и слова.
6. Сделай текст дружелюбным и захватывающим.
7. Используй HTML-форматирование для выделения ключевых моментов.
8. ОБЯЗАТЕЛЬНО: Итоговый текст должен содержать не более 950 символов. Это критически важно!
9. НЕ добавляй никаких примечаний или комментариев от себя в конце текста.

Пример стиля:
<b>🚨 Внимание, SOL-армия!</b> 🌞 Вы готовы к <i>сенсационным</i> новостям? <tg-spoiler>Солана снова всех удивила!</tg-spoiler> 🎉

Помни: текст должен быть уникальным, информативным и вызывать желание обсудить новость, но не превышать 950 символов."""
    return prompt

async def get_prompt_calls(text):
    prompt = f"""Перепиши следующий текст для канала Gambler Pepe | CALLS:

{text}

Инструкции:
1. Начни с креативного приветствия, упоминая Pepe. Например: "Крипто-гэмблеры, Пепе на линии! 🎰🐸"
2. ОБЯЗАТЕЛЬНО используй HTML-форматирование:
   - Жирный текст: <b>пример</b>
   - Курсив: <i>пример</i>
   - Спойлер: <tg-spoiler>пример</tg-spoiler>
3. Добавь разнообразные эмодзи по тематики (минимум 4-6 разных).
4. Начни с интригующего заявления или вопроса о предстоящем колле.
5. Перепиши текст, сохраняя ключевую информацию, но изменяя структуру и формулировки.
6. Сделай текст динамичным и побуждающим к действию.
7. Используй HTML-форматирование для выделения важных деталей и цифр.
8. ОБЯЗАТЕЛЬНО: Итоговый текст должен содержать не более 950 символов. Это критически важно!
9. НЕ добавляй никаких примечаний или комментариев от себя в конце текста.

Пример стиля:
<b>🔥 Горячий колл на горизонте!</b> 📞 Готовы ли вы к <i>потенциальному иксу</i>? <tg-spoiler>Этот проект может взорвать рынок!</tg-spoiler> 💥

Помни: текст должен быть уникальным, информативным и мотивировать на участие в колле, но не превышать 950 символов."""
    return prompt

async def get_prompt_ton_news(text):
    prompt = f"""Перепиши следующий текст для канала FIRST TON NEWS:

{text}

Инструкции:
1. Начни с профессионального, но дружелюбного приветствия. Например: "Доброго времени суток, TON-комьюнити! 👋"
2. ОБЯЗАТЕЛЬНО используй HTML-форматирование:
   - Жирный текст: <b>пример</b>
   - Курсив: <i>пример</i>
   - Спойлер: <tg-spoiler>пример</tg-spoiler>
3. Добавь разнообразные эмодзи по тематики (минимум 5 разных).
4. Начни с интригующего вступления о новостях в мире TON.
5. Перепиши текст, сохраняя всю важную информацию, но изменяя структуру и используя синонимы.
6. Добавь краткие комментарии или мысли автора в скобках.
7. Используй HTML-форматирование для выделения ключевых фактов, цифр и цитат.
8. ОБЯЗАТЕЛЬНО: Итоговый текст должен содержать не более 950 символов. Это критически важно!
9. НЕ добавляй никаких примечаний или комментариев от себя в конце текста.

Пример стиля:
<b>🚀 Прорыв в экосистеме TON!</b> Уважаемые читатели, приготовьтесь к <i>захватывающим новостям</i>... <tg-spoiler>TON снова удивляет мир криптовалют!</tg-spoiler> 🌟

Помни: текст должен быть уникальным, информативным и вызывать интерес к развитию TON, но не превышать 950 символов."""
    return prompt
