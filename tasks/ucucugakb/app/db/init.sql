CREATE DATABASE IF NOT EXISTS appdb DEFAULT CHARSET utf8mb4;

USE appdb;

CREATE TABLE tasks(
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    task_name CHAR(30) NOT NULL,
    title CHAR(100) NOT NULL,
    points INT NOT NULL,
    category CHAR(10) NOT NULL,
    author CHAR(20) NOT NULL,
    flag CHAR(100) NOT NULL,
    ctf CHAR(50) NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("devzero", "Без единиц", 250, "stegano", "kalan", "ugra_did_you_ever_feel_that_clean", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("intercom", "Домофон", 100, "recon", "ksixty", "ugra_pati_na_hate", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("exam", "Экзамен по истории", 100, "reverse", "kalan", "ugra_teacher_is_so_proud_of_you", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("mnist", "Мнистерство статистики", 350, "ppc", "kalan", "ugra_apply_now_for_senior_ai_researcher", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("subdomain", "Запросы", 300, "forensics", "nsychev", "ugra_http2_is_nice_but_better_with_iodine", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("selectric", "IBM Selectric", 200, "crypto", "kalan", "ugra_does_one_like_new_3d_episodes", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("iswho", "Кто", 100, "web", "ksixty", "ugra_good_languages_do_not_force_you_to_rely_on_bash", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("friends", "Друзья", 250, "web", "nsychev", "ugra_oh_no_totp_secret_leaked", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("sancta", "Святая простота", 150, "stegano", "kalan", "ugra_no_firewood_required_for_now", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("formulae", "Формулы", 150, "reverse", "kalan", "ugra_school_informatics_isnt_that_useless", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("pycfail", "Великий математик", 150, "reverse", "nsychev", "ugra_weird_gcd_calculation", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("passman", "Менеджер паролей", 300, "web", "nsychev", "ugra_lets_forget_xor_forever", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("mines", "Сапёр-неудачник", 200, "reverse", "abbradar", "ugra_avoid_the_mines", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("feedback", "Отзыв", 50, "crypto", "nsychev", "ugra_i_love_emoji", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("ege", "ЕГЭ", 350, "ppc", "ksixty", "ugra_durnytsya_dribnitsya", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("anthem2", "Гимн года II", 300, "stegano", "kalan", "ugra_like_and_subscribe", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("mybrick", "Мой Кирпич", 200, "web", "nsychev", "ugra_validate_user_input", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("homepage", "Домашняя страница", 50, "web", "nsychev", "ugra_what_is_your_erdos_number", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("hitech2", "Хай-тек II", 150, "recon", "nsychev", "ugra_we_all_make_good_websites", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("flappy", "Турбоптица", 150, "joy", "abbradar", "ugra_moore_is_flapping_in_his_dreams", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("gaffer", "Дед файл сделал", 100, "crypto", "kalan", "ugra_my_main_backup_is_my_last_will", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("jk", "Самый короткий анекдот", 300, "stegano", "kalan", "ugra_when_i_was_this_small_it_already_had_a_beard_that_long", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("promotion", "Самый важный таск", 25, "joy", "nsychev", "ugra_thanks_for_good_photo", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("anthem1", "Гимн года I", 50, "stegano", "kalan", "ugra_do_the_guys_a_favor", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("shrink", "Расширение сознания", 350, "reverse", "ksixty", "ugra_shrunk_the_shrink", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("hitech3", "Хай-тек III", 300, "recon", "nsychev", "ugra_querystring_is_the_new_cookie", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("hitech1", "Хай-тек I", 100, "forensics", "nsychev", "ugra_vim_saves_the_world", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("bestrsa", "Больше, чем RSA", 250, "crypto", "nsychev", "ugra_3rsa_is_secure_unless_you_get_bad_primes", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("noteasy5", "noteasy₅", 150, "crypto", "kalan", "ugra_rituals_may_vary_and_so_do_quirks", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("japclock", "Праздник в Японии", 200, "recon", "kalan", "ugra_arubaito_toranpu_pasokon", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("casino", "777", 200, "web", "abbradar", "ugra_vulnerability_beats_probability", "ugractf-2020-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("reverse", "Перевёртыш", 100, "crypto", "kalan", "ugra_deified_civic_radar_reviver", "ugractf-2020-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("onair", "В эфире", 150, "web", "nsychev", "ugra_who_writes_so_bad_code", "ugractf-2020-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("artist", "Он так видит", 200, "reverse", "kalan", "ugra_art_is_so_jvneovpakwnvjtoalqing_great", "ugractf-2020-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("dumpster", "Сага о резервных копиях", 200, "forensics", "kalan", "ugra_mind_your_updates", "ugractf-2020-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("lms", "Задача 27", 250, "pwn", "abbradar", "ugra_use_well_tested_sandboxes", "ugractf-2020-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("hello", "Пинг", 200, "stegano", "nsychev", "ugra_this_bit_is_r5s5rv5d", "ugractf-2020-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("zinaida", "Вопрос на миллион", 300, "ppc", "kalan", "ugra_must_be_funny_in_a_rich_man_s_world", "ugractf-2020-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("uniform", "Камуфляж", 300, "stegano", "kalan", "ugra_who_s_that_writin_john_the_revelator", "ugractf-2020-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("printme", "Напечатай это", 100, "forensics", "kalan", "ugra_slowly_losing_bits_of_sanity", "ugractf-2020-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("octathlon", "Восьмиборье", 150, "stegano", "abbradar", "ugra_not_as_easy_as_it_used_to", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("hantatonlive", "Hantaton Live", 350, "stegano", "ksixty", "ugra_everything_is_a_remix_even", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("linear", "Набор отрезков", 200, "misc", "kalan", "ugra_null_pager_quad_jogger_collab", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("noteasy82", "noteasy+82", 250, "crypto", "kalan", "ugra_just_honk_and_bibimbap", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("powerful", "Мощный шифр", 250, "crypto", "nsychev", "ugra_it_is_too_powerful_rsa_right", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("nothingtosee", "Nothing to see", 100, "web", "javach", "ugra_v1_p0sm0tr3l1", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("soviet", "ЦНИИВТ", 150, "stegano", "nsychev", "ugra_soviet_technologies_are_eternal", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("round", "Вокруг да около", 150, "reverse", "abbradar", "ugra_look_around", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("support", "База знаний", 250, "misc", "nsychev", "ugra_you_can_do_sqli_in_telegram_too", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("dreamteam", "Команда мечты", 100, "recon", "kalan", "ugra_from_friendship_in_sports_to_the_world_on_the_land", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("developers", "Новейшая разработка", 200, "forensics", "kalan", "ugra_the_yellow_purse", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("battleship", "Морской бой", 300, "ppc", "abbradar", "ugra_gotta_hit_fast", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("antivirus", "Антивирус", 250, "pwn", "abbradar", "ugra_who_checks_the_checker", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("daodejing", "Книга пути и достоинства", 150, "misc", "kalan", "ugra_grandpa_take_your_pills_or_we_will_beat_up_your", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("smallercitylights", "Огни города поменьше", 400, "recon", "kalan", "ugra_we_will_go_we_will_swim_we_will_crawl", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("congress", "Конгресс", 200, "ppc", "nsychev", "ugra_what_a_beautiful_number", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("thevillage", "Сельский клуб", 300, "web", "ksixty", "ugra_come_for_tasks_stay_for", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("compliance", "Сертификация соответствия", 150, "web", "kalan", "ugra_said_secret_service_secretly_succumbs", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("apl", "Арбатско-Покровская линия?", 150, "crypto", "ksixty", "ugra_the_next_station_is_esoteric_programming", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("onestop", "Служба одного порта", 200, "network", "abbradar", "ugra_social_services_for_the_masses", "ugractf-2021-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("dropbox", "Dropbox", 200, "web", "javach", "ugra_dvoinoi_ris_etot", "ugractf-2021-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("buggy", "Альфа-версия", 350, "reverse", "abbradar", "ugra_smaller_is_better", "ugractf-2021-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("wrapped", "Упаковано", 100, "crypto", "kalan", "ugra_seal_it_file_it_batch_it_mark_it", "ugractf-2021-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("backforth", "Безопасный чат", 150, "reverse", "abbradar", "ugra_obscure_unix_security", "ugractf-2021-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("japcipher", "Японский шифр", 150, "crypto", "ksixty", "ugra_i_is_to_ro_as_ro_is_to_ha", "ugractf-2021-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("airlines", "S21 Airlines", 150, "web", "ksixty", "ugra_booking_numbers_are_sequential_yet_ticket_prices_are_exponential", "ugractf-2021-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("agency", "Агентство", 300, "forensics", "kalan", "ugra_agents_of_a_feather_duck_together", "ugractf-2021-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("urtracing", "Юртогонки!", 200, "ppc", "ksixty", "ugra_etot_paren_byl_iz_teh", "ugractf-2021-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("agronft", "NFT Bezopasniy Enclave", 300, "reverse", "ksixty", "ugra_kerckhoffs_saw_disassemblers_coming", "ugractf-2022-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("thermal", "Термопринтер", 400, "reverse", "kalan", "ugra_esc_pos_goes_lprrrrrrrr", "ugractf-2022-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("onaplate", "На блюдечке...", 25, "web", "ksixty", "ugra_as_easy_as_it_gets", "ugractf-2022-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("shout", "Поорите", 75, "pwn", "nsychev", "ugra_aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", "ugractf-2022-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("betagost", "ГОСТ 34.13-2022", 100, "crypto", "nsychev", "ugra_lfsr_is_so_cyclic", "ugractf-2022-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("asciirsa", "ASCII-RSA", 75, "crypto", "nsychev", "ugra_dont_roll_asciirsa_crypto", "ugractf-2022-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("snekpeek", "Разборчивая змейка", 250, "ppc", "kalan", "ugra_i_specifically_requested_the_opposite_of_this", "ugractf-2022-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("margin", "Поля слишком узки", 100, "misc", "kalan", "ugra_i_wish_fermat_had_css", "ugractf-2022-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("noteasy03", "noteasy03", 350, "crypto", "ksixty", "ugra_in_case_of_losing_your_sanity_dial_oh_three", "ugractf-2022-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("xoxoracing", "Хохорейсинг", 100, "crypto", "kalan", "ugra_go_go_go_come_on_yes_yes_a_bit_more_just_a_little", "ugractf-2022-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("neatfind", "Прикольная находка", 100, "forensics", "ksixty", "ugra_every_big_thing_consists_of_many_little_ones", "ugractf-2022-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("symphony", "Играет как умеет", 350, "ppc", "kalan", "ugra_wavy_obnoxious_squirrels", "ugractf-2022-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("well", "Well known and loved", 100, "web", "nsychev", "ugra_matrix_is_well_known_to_everyone", "ugractf-2022-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("cacaptcha", "CACAPTCHA", 250, "ppc", "ksixty", "ugra_did_you_know_that_captcha_is_a_trademark", "ugractf-2022-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("barberwireless", "Случай в парикмахерской", 200, "forensics", "kalan", "ugra_cracking_be_in_the_air_tonight", "ugractf-2022-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("sacredplace", "Свято место пусто не бывает", 50, "web", "ksixty", "ugra_unless_it_is_not_really_that_sacred", "ugractf-2022-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("stairwell", "Лестница", 300, "osint", "kalan", "ugra_and_she_is_buying_one_to_heaven", "ugractf-2022-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("tictactoe", "Крестики-нолики", 300, "reverse", "kolya", "ugra_tic_tac_reverse_takes_time", "ugractf-2022-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("cryptoneliner", "Криптобаш", 200, "crypto", "baksist", "ugra_oneliners_rule", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("pebcak", "PEBCAK", 150, "reverse", "purplesyringa", "ugra_thats_not_how_access_control_works", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("safestr", "Безопасность должна быть доступной", 100, "pwn", "gudn", "ugra_safe_0r_no7_5afe", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("qrec", "Советские вступительные в ясельный класс", 400, "ppc", "gudn", "ugra_ugra_ugra_ugrec", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("crypdle", "Crypdle", 250, "reverse", "purplesyringa", "ugra_no_you_cant_replace_backend_with_crypto", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("goodolddays", "Старые добрые времена", 200, "web", "purplesyringa", "ugra_stop_reinventing_the_wheel", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("bookkeeping", "Бухгалтерия", 100, "stegano", "purplesyringa", "ugra_you_asked_for_lattices", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("seeker", "Кто ищет, тот всегда найдёт", 200, "osint", "baksist", "ugra_dont_expose_usernames", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("warmup", "Поле для сдачи флага", 10, "misc", "nsychev", "ugra", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("whirlpool", "Водоворот", 50, "crypto", "purplesyringa", "ugra_double_security_for_only_50_more_bucks", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("trisection", "Трисекция", 100, "web", "baksist", "ugra_triangles_are_cool_but_triflags_are_way_cooler", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("hollywood", "Голливуд", 250, "ppc", "purplesyringa", "ugra_how_about_a_nice_game_of_chess", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("depth", "Глубина", 150, "ppc", "purplesyringa", "ugra_i_have_always_imagined_that_paradise_will_be_a_kind_of_library", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("thevillage2", "Сельский блог", 100, "web", "nsychev", "ugra_please_dont_read_it_you_didnt_pay", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("takefive", "Музыкальная пятиминутка", 50, "stegano", "ksixty", "ugra_we_support_local_artists", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("proofbyintimidation", "Доказательство запугиванием", 200, "ctb", "purplesyringa", "ugra_this_aint_funny_this_is_cursed", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("espionage", "Прямо как у NSA", 150, "crypto", "purplesyringa", "ugra_you_guys_are_getting_encryption", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("mazerunner", "Maze Runner", 300, "ppc", "purplesyringa", "ugra_listen_to_in_the_dark_by_bmth", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("pity", "Мультфильмы", 150, "misc", "purplesyringa", "ugra_weve_got_terminals", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("snowcrash", "Snow Crash", 300, "reverse", "purplesyringa", "ugra_dont_roll_your_own_cryptography_unless_you_are_nist", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("elementary", "Элементарно", 100, "reverse", "purplesyringa", "ugra_astonishing", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("capture", "Захват трафика", 100, "forensics", "baksist", "ugra_traffic_extractor", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("collateral", "Антивирус возвращается", 200, "ctb", "purplesyringa", "ugra_ever_wondered_who_uses_virustotal_most_huh", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("tortoise", "Скорость без границ", 350, "crypto", "purplesyringa", "ugra_never_underestimate_predictability", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("nucached", "Nucached", 200, "web", "purplesyringa", "ugra_now_go_patch_your_own_websites", "ugractf-2023-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("circulation", "Циркуляция", 200, "forensics", "baksist", "ugra_sum_around_and_check_out", "ugractf-2023-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("nucached2", "Nucached 2.0", 200, "ctb", "purplesyringa", "ugra_you_should_have_rewritten_it_in_rust", "ugractf-2023-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("moonshot", "Очень удалённый доступ", 300, "pwn", "purplesyringa", "ugra_friendly_reminder_that_web_browsers_use_jit_too", "ugractf-2023-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("msr", "Minimum system requirements", 400, "reverse", "rozetkin", "ugra_wow_that_was_a_cool_cat", "ugractf-2023-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("classic", "Классическая дискета", 200, "forensics", "ksixty", "ugra_you_are_a_power_macintosh_user", "ugractf-2023-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("endlessline", "Очередь", 150, "web", "astrra", "ugra_spasibo_za_ozhidaniye", "ugractf-2023-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("brevity", "Краткость — сестра таланта", 100, "ppc", "baksist", "ugra_do_you_speak_oneliner_well_i_do", "ugractf-2023-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("payoff", "Решите капчу за нас", 150, "web", "gudn", "ugra_thanks_and_give_your_money", "ugractf-2023-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("classified", "[ДАННЫЕ УДАЛЕНЫ]", 250, "ppc", "purplesyringa", "ugra_airgaps_can_be_bypassed", "ugractf-2023-school");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("cmap1", "cmap I", 150, "ppc", "nsychev", "ugra_you_do_not_need_usepackage_cmap", "ugractf-2022-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("cmap2", "cmap II", 300, "forensics", "nsychev", "ugra_oh_what_a_weird_font_here", "ugractf-2022-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("webdept", "Веб-департамент", 300, "web", "nsychev", "ugra_isolate_your_public_hosts", "ugractf-2022-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("webdeptcrypto", "Крипто-департамент", 300, "web", "nsychev", "ugra_do_not_ever_use_cbc", "ugractf-2022-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("melodrama1", "Melodrama I", 150, "pwn", "nsychev", "ugra_nullptr_is_a_zero", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("melodrama2", "Melodrama II", 250, "pwn", "nsychev", "ugra_zerobyte_does_not_count", "ugractf-2020-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("qualification", "Qualification", 200, "reverse", "rozetkin", "ugra_android_rev3r53_not_5o_easy_bu7_it_1s_c0o7", "ugractf-2023-quals");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("ecipher", "Bege", 300, "reverse", "gudn", "ugra_r0tate_brack3ts", "ugractf-2023-quals");
-- open tasks
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("ucucugakb", "UcucugaKB", 0, "web", "baksist", "placeholder_for_flag", "ugractf-2023-open");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("sayinggoes", "Просто скажи", 0, "crypto", "kalan", "TBA", "ugractf-2023-open");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("bururute", "Войти и не пострадать", 0, "web", "kalan", "TBA", "ugractf-2023-open");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("weblog", "Web log", 0, "web", "purplesyringa", "TBA", "ugractf-2023-open");
INSERT INTO tasks (task_name, title, points, category, author, flag, ctf) VALUES ("noteotp", "Ничего не забыть", 0, "web", "gudn", "TBA", "ugractf-2023-open");