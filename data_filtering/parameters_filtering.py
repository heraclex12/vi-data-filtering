import string
from emoji import UNICODE_EMOJI_ENGLISH

main_special_characters = string.punctuation + string.digits + string.whitespace
other_special_characters = (
    "    　    ￼’“”–ー一▬…✦�­£​•€«»°·═"
    "×士＾˘⇓↓↑←→（）§″′´¿−±∈﻿¢ø‚„½¼¾¹²³―⁃，ˌ¸‹›ʺˈʻ¦‐⠀‰‑≤≥‖"
    "◆●■►▼▲▴∆▻¡★☆✱ːº。¯˜¥ɪ≈†上ン：∼⁄・♡✓⊕․．⋅÷１‟；،、¨ाাी्े◦˚゜ʼ≖ʼ¤ッツシ℃√！【】‿∞➤～πه۩☛₨➩☻๑٪♥ıॽ《‘©﴿٬？▷Г♫∟™ª₪®「—❖」﴾》"
)
emoji = list(UNICODE_EMOJI_ENGLISH.keys())

special_characters_default = set(main_special_characters + other_special_characters)
special_characters_default.update(emoji)

parameters_filtering = {
    "cond_uniform_whitespace": True,
    "cond_replace_unicode_punctuation": False,
    "cond_remove_words_with_incorrect_substrings": True,
    "incorrect_word_substrings": ["http", "www", ".com", "href", "//"],
    "cond_remove_long_words": True,
    "length_word_max_cutoff": 25,
    "cond_check_number_words": True,
    "tokenization": False,
    "strip_characters": special_characters_default,
    "number_words_min_cutoff": 30,
    "number_words_max_cutoff": 100000,
    "cond_check_character_repetition_removal": True,
    "character_repetition_length": 10,
    "character_repetition_max_cutoff": 0.15,
    "cond_check_word_repetition_removal": True,
    "word_repetition_length": 5,
    "word_repetition_max_cutoff": 0.20,
    "cond_check_special_characters": True,
    "special_characters": special_characters_default,
    "special_characters_max_cutoff": 0.34,
    "cond_words_augmentation": True,
    "words_augmentation_group_sizes": [2],
    "words_augmentation_join_char": " ",
    "cond_check_stopwords": True,
    "stopwords_min_cutoff": 0.08,
    "cond_check_flagged_words": True,
    "flagged_words_max_cutoff": 0.005,
    "cond_check_lang_id": False,   # Temporarily turn off filtering lang id for Vietnamese Common Crawl Data
    "lang_id_min_cutoff": 0.90,
    "cond_check_perplexity": True,
    "perplexity_max_cutoff": 1600,
}
