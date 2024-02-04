module.exports = grammar({
    name: 'mira',

    rules: {
        module: $ => repeat(choice(
            $.comment,
            $.block_comment,
            $.expr
        )),

        comment: $ => token(seq('#', /[^#].*/)),

        block_comment: $ => prec(2, token(seq('##', /(.|\n|#[^#]])*/, '##'))),

        expr: $ => choice(prec(2, $.num), prec(1, $.int), $.ident, $.binary),

        binary: $ => choice(prec.left(1, seq($.expr, "+", $.expr))),

        num: $ => token(/[+-]?\d+(\.\d*|[eE][+-]?\d+)/),

        int: $ => token(/[+-]?[0-9]+/),

        ident: $ => token(/[_a-zA-Z]+[_a-zA-Z0-9]*/),







    }
});
