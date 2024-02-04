#include <tree_sitter/parser.h>

#if defined(__GNUC__) || defined(__clang__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wmissing-field-initializers"
#endif

#define LANGUAGE_VERSION 14
#define STATE_COUNT 12
#define LARGE_STATE_COUNT 9
#define SYMBOL_COUNT 12
#define ALIAS_COUNT 0
#define TOKEN_COUNT 7
#define EXTERNAL_TOKEN_COUNT 0
#define FIELD_COUNT 0
#define MAX_ALIAS_SEQUENCE_LENGTH 3
#define PRODUCTION_ID_COUNT 1

enum {
  sym_comment = 1,
  aux_sym_block_comment_token1 = 2,
  anon_sym_PLUS = 3,
  sym_num = 4,
  sym_int = 5,
  sym_ident = 6,
  sym_module = 7,
  sym_block_comment = 8,
  sym_expr = 9,
  sym_binary = 10,
  aux_sym_module_repeat1 = 11,
};

static const char * const ts_symbol_names[] = {
  [ts_builtin_sym_end] = "end",
  [sym_comment] = "comment",
  [aux_sym_block_comment_token1] = "block_comment_token1",
  [anon_sym_PLUS] = "+",
  [sym_num] = "num",
  [sym_int] = "int",
  [sym_ident] = "ident",
  [sym_module] = "module",
  [sym_block_comment] = "block_comment",
  [sym_expr] = "expr",
  [sym_binary] = "binary",
  [aux_sym_module_repeat1] = "module_repeat1",
};

static const TSSymbol ts_symbol_map[] = {
  [ts_builtin_sym_end] = ts_builtin_sym_end,
  [sym_comment] = sym_comment,
  [aux_sym_block_comment_token1] = aux_sym_block_comment_token1,
  [anon_sym_PLUS] = anon_sym_PLUS,
  [sym_num] = sym_num,
  [sym_int] = sym_int,
  [sym_ident] = sym_ident,
  [sym_module] = sym_module,
  [sym_block_comment] = sym_block_comment,
  [sym_expr] = sym_expr,
  [sym_binary] = sym_binary,
  [aux_sym_module_repeat1] = aux_sym_module_repeat1,
};

static const TSSymbolMetadata ts_symbol_metadata[] = {
  [ts_builtin_sym_end] = {
    .visible = false,
    .named = true,
  },
  [sym_comment] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_block_comment_token1] = {
    .visible = false,
    .named = false,
  },
  [anon_sym_PLUS] = {
    .visible = true,
    .named = false,
  },
  [sym_num] = {
    .visible = true,
    .named = true,
  },
  [sym_int] = {
    .visible = true,
    .named = true,
  },
  [sym_ident] = {
    .visible = true,
    .named = true,
  },
  [sym_module] = {
    .visible = true,
    .named = true,
  },
  [sym_block_comment] = {
    .visible = true,
    .named = true,
  },
  [sym_expr] = {
    .visible = true,
    .named = true,
  },
  [sym_binary] = {
    .visible = true,
    .named = true,
  },
  [aux_sym_module_repeat1] = {
    .visible = false,
    .named = false,
  },
};

static const TSSymbol ts_alias_sequences[PRODUCTION_ID_COUNT][MAX_ALIAS_SEQUENCE_LENGTH] = {
  [0] = {0},
};

static const uint16_t ts_non_terminal_alias_map[] = {
  0,
};

static const TSStateId ts_primary_state_ids[STATE_COUNT] = {
  [0] = 0,
  [1] = 1,
  [2] = 2,
  [3] = 3,
  [4] = 4,
  [5] = 5,
  [6] = 6,
  [7] = 7,
  [8] = 8,
  [9] = 9,
  [10] = 10,
  [11] = 11,
};

static bool ts_lex(TSLexer *lexer, TSStateId state) {
  START_LEXER();
  eof = lexer->eof(lexer);
  switch (state) {
    case 0:
      if (eof) ADVANCE(7);
      if (lookahead == '#') ADVANCE(1);
      if (lookahead == '+') ADVANCE(10);
      if (lookahead == '-') ADVANCE(3);
      if (lookahead == '\t' ||
          lookahead == '\n' ||
          lookahead == '\r' ||
          lookahead == ' ') SKIP(0)
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(12);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(13);
      END_STATE();
    case 1:
      if (lookahead == '#') ADVANCE(6);
      if (lookahead != 0) ADVANCE(8);
      END_STATE();
    case 2:
      if (lookahead == '+' ||
          lookahead == '-') ADVANCE(4);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(11);
      END_STATE();
    case 3:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(12);
      END_STATE();
    case 4:
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(11);
      END_STATE();
    case 5:
      if (lookahead != 0 &&
          lookahead != '#') ADVANCE(6);
      if (lookahead == '#') ADVANCE(9);
      END_STATE();
    case 6:
      if (lookahead != 0 &&
          lookahead != '#') ADVANCE(6);
      if (lookahead == '#') ADVANCE(5);
      END_STATE();
    case 7:
      ACCEPT_TOKEN(ts_builtin_sym_end);
      END_STATE();
    case 8:
      ACCEPT_TOKEN(sym_comment);
      if (lookahead != 0 &&
          lookahead != '\n') ADVANCE(8);
      END_STATE();
    case 9:
      ACCEPT_TOKEN(aux_sym_block_comment_token1);
      if (lookahead != 0 &&
          lookahead != '#') ADVANCE(6);
      if (lookahead == '#') ADVANCE(9);
      END_STATE();
    case 10:
      ACCEPT_TOKEN(anon_sym_PLUS);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(12);
      END_STATE();
    case 11:
      ACCEPT_TOKEN(sym_num);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(11);
      END_STATE();
    case 12:
      ACCEPT_TOKEN(sym_int);
      if (lookahead == '.') ADVANCE(11);
      if (lookahead == 'E' ||
          lookahead == 'e') ADVANCE(2);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(12);
      END_STATE();
    case 13:
      ACCEPT_TOKEN(sym_ident);
      if (('0' <= lookahead && lookahead <= '9')) ADVANCE(14);
      if (('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(13);
      END_STATE();
    case 14:
      ACCEPT_TOKEN(sym_ident);
      if (('0' <= lookahead && lookahead <= '9') ||
          ('A' <= lookahead && lookahead <= 'Z') ||
          lookahead == '_' ||
          ('a' <= lookahead && lookahead <= 'z')) ADVANCE(14);
      END_STATE();
    default:
      return false;
  }
}

static const TSLexMode ts_lex_modes[STATE_COUNT] = {
  [0] = {.lex_state = 0},
  [1] = {.lex_state = 0},
  [2] = {.lex_state = 0},
  [3] = {.lex_state = 0},
  [4] = {.lex_state = 0},
  [5] = {.lex_state = 0},
  [6] = {.lex_state = 0},
  [7] = {.lex_state = 0},
  [8] = {.lex_state = 0},
  [9] = {.lex_state = 0},
  [10] = {.lex_state = 0},
  [11] = {.lex_state = 0},
};

static const uint16_t ts_parse_table[LARGE_STATE_COUNT][SYMBOL_COUNT] = {
  [0] = {
    [ts_builtin_sym_end] = ACTIONS(1),
    [sym_comment] = ACTIONS(1),
    [aux_sym_block_comment_token1] = ACTIONS(1),
    [anon_sym_PLUS] = ACTIONS(1),
    [sym_num] = ACTIONS(1),
    [sym_int] = ACTIONS(1),
    [sym_ident] = ACTIONS(1),
  },
  [1] = {
    [sym_module] = STATE(11),
    [sym_block_comment] = STATE(2),
    [sym_expr] = STATE(7),
    [sym_binary] = STATE(6),
    [aux_sym_module_repeat1] = STATE(2),
    [ts_builtin_sym_end] = ACTIONS(3),
    [sym_comment] = ACTIONS(5),
    [aux_sym_block_comment_token1] = ACTIONS(7),
    [sym_num] = ACTIONS(9),
    [sym_int] = ACTIONS(11),
    [sym_ident] = ACTIONS(13),
  },
  [2] = {
    [sym_block_comment] = STATE(3),
    [sym_expr] = STATE(7),
    [sym_binary] = STATE(6),
    [aux_sym_module_repeat1] = STATE(3),
    [ts_builtin_sym_end] = ACTIONS(15),
    [sym_comment] = ACTIONS(17),
    [aux_sym_block_comment_token1] = ACTIONS(7),
    [sym_num] = ACTIONS(9),
    [sym_int] = ACTIONS(11),
    [sym_ident] = ACTIONS(13),
  },
  [3] = {
    [sym_block_comment] = STATE(3),
    [sym_expr] = STATE(7),
    [sym_binary] = STATE(6),
    [aux_sym_module_repeat1] = STATE(3),
    [ts_builtin_sym_end] = ACTIONS(19),
    [sym_comment] = ACTIONS(21),
    [aux_sym_block_comment_token1] = ACTIONS(24),
    [sym_num] = ACTIONS(27),
    [sym_int] = ACTIONS(30),
    [sym_ident] = ACTIONS(33),
  },
  [4] = {
    [ts_builtin_sym_end] = ACTIONS(36),
    [sym_comment] = ACTIONS(36),
    [aux_sym_block_comment_token1] = ACTIONS(36),
    [anon_sym_PLUS] = ACTIONS(38),
    [sym_num] = ACTIONS(36),
    [sym_int] = ACTIONS(38),
    [sym_ident] = ACTIONS(36),
  },
  [5] = {
    [ts_builtin_sym_end] = ACTIONS(36),
    [sym_comment] = ACTIONS(36),
    [aux_sym_block_comment_token1] = ACTIONS(36),
    [anon_sym_PLUS] = ACTIONS(38),
    [sym_num] = ACTIONS(36),
    [sym_int] = ACTIONS(38),
    [sym_ident] = ACTIONS(36),
  },
  [6] = {
    [ts_builtin_sym_end] = ACTIONS(36),
    [sym_comment] = ACTIONS(36),
    [aux_sym_block_comment_token1] = ACTIONS(36),
    [anon_sym_PLUS] = ACTIONS(38),
    [sym_num] = ACTIONS(36),
    [sym_int] = ACTIONS(38),
    [sym_ident] = ACTIONS(36),
  },
  [7] = {
    [ts_builtin_sym_end] = ACTIONS(40),
    [sym_comment] = ACTIONS(40),
    [aux_sym_block_comment_token1] = ACTIONS(40),
    [anon_sym_PLUS] = ACTIONS(42),
    [sym_num] = ACTIONS(40),
    [sym_int] = ACTIONS(44),
    [sym_ident] = ACTIONS(40),
  },
  [8] = {
    [ts_builtin_sym_end] = ACTIONS(46),
    [sym_comment] = ACTIONS(46),
    [aux_sym_block_comment_token1] = ACTIONS(46),
    [anon_sym_PLUS] = ACTIONS(48),
    [sym_num] = ACTIONS(46),
    [sym_int] = ACTIONS(48),
    [sym_ident] = ACTIONS(46),
  },
};

static const uint16_t ts_small_parse_table[] = {
  [0] = 2,
    ACTIONS(52), 1,
      sym_int,
    ACTIONS(50), 5,
      ts_builtin_sym_end,
      sym_comment,
      aux_sym_block_comment_token1,
      sym_num,
      sym_ident,
  [11] = 5,
    ACTIONS(9), 1,
      sym_num,
    ACTIONS(11), 1,
      sym_int,
    ACTIONS(13), 1,
      sym_ident,
    STATE(6), 1,
      sym_binary,
    STATE(8), 1,
      sym_expr,
  [27] = 1,
    ACTIONS(54), 1,
      ts_builtin_sym_end,
};

static const uint32_t ts_small_parse_table_map[] = {
  [SMALL_STATE(9)] = 0,
  [SMALL_STATE(10)] = 11,
  [SMALL_STATE(11)] = 27,
};

static const TSParseActionEntry ts_parse_actions[] = {
  [0] = {.entry = {.count = 0, .reusable = false}},
  [1] = {.entry = {.count = 1, .reusable = false}}, RECOVER(),
  [3] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_module, 0),
  [5] = {.entry = {.count = 1, .reusable = true}}, SHIFT(2),
  [7] = {.entry = {.count = 1, .reusable = true}}, SHIFT(9),
  [9] = {.entry = {.count = 1, .reusable = true}}, SHIFT(4),
  [11] = {.entry = {.count = 1, .reusable = false}}, SHIFT(5),
  [13] = {.entry = {.count = 1, .reusable = true}}, SHIFT(6),
  [15] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_module, 1),
  [17] = {.entry = {.count = 1, .reusable = true}}, SHIFT(3),
  [19] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_module_repeat1, 2),
  [21] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_module_repeat1, 2), SHIFT_REPEAT(3),
  [24] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_module_repeat1, 2), SHIFT_REPEAT(9),
  [27] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_module_repeat1, 2), SHIFT_REPEAT(4),
  [30] = {.entry = {.count = 2, .reusable = false}}, REDUCE(aux_sym_module_repeat1, 2), SHIFT_REPEAT(5),
  [33] = {.entry = {.count = 2, .reusable = true}}, REDUCE(aux_sym_module_repeat1, 2), SHIFT_REPEAT(6),
  [36] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_expr, 1),
  [38] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_expr, 1),
  [40] = {.entry = {.count = 1, .reusable = true}}, REDUCE(aux_sym_module_repeat1, 1),
  [42] = {.entry = {.count = 1, .reusable = false}}, SHIFT(10),
  [44] = {.entry = {.count = 1, .reusable = false}}, REDUCE(aux_sym_module_repeat1, 1),
  [46] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_binary, 3),
  [48] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_binary, 3),
  [50] = {.entry = {.count = 1, .reusable = true}}, REDUCE(sym_block_comment, 1),
  [52] = {.entry = {.count = 1, .reusable = false}}, REDUCE(sym_block_comment, 1),
  [54] = {.entry = {.count = 1, .reusable = true}},  ACCEPT_INPUT(),
};

#ifdef __cplusplus
extern "C" {
#endif
#ifdef _WIN32
#define extern __declspec(dllexport)
#endif

extern const TSLanguage *tree_sitter_mira(void) {
  static const TSLanguage language = {
    .version = LANGUAGE_VERSION,
    .symbol_count = SYMBOL_COUNT,
    .alias_count = ALIAS_COUNT,
    .token_count = TOKEN_COUNT,
    .external_token_count = EXTERNAL_TOKEN_COUNT,
    .state_count = STATE_COUNT,
    .large_state_count = LARGE_STATE_COUNT,
    .production_id_count = PRODUCTION_ID_COUNT,
    .field_count = FIELD_COUNT,
    .max_alias_sequence_length = MAX_ALIAS_SEQUENCE_LENGTH,
    .parse_table = &ts_parse_table[0][0],
    .small_parse_table = ts_small_parse_table,
    .small_parse_table_map = ts_small_parse_table_map,
    .parse_actions = ts_parse_actions,
    .symbol_names = ts_symbol_names,
    .symbol_metadata = ts_symbol_metadata,
    .public_symbol_map = ts_symbol_map,
    .alias_map = ts_non_terminal_alias_map,
    .alias_sequences = &ts_alias_sequences[0][0],
    .lex_modes = ts_lex_modes,
    .lex_fn = ts_lex,
    .primary_state_ids = ts_primary_state_ids,
  };
  return &language;
}
#ifdef __cplusplus
}
#endif
