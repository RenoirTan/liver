# LiVer v0.1.0 Changelog

## Version 0.0.x

Original version.

## Version 0.1.0

Decrease the saturation of:

1. violet,
2. lilac,
3. lavender,
4. blue-violet,
5. cyan,
6. mint-green

In addition, `neutral`'s hex color value has been changed from `#797979` to
`#7f7f7f` after I realised that 0xFF / 2 is 0x7F and not 0x79.

White has been darkened from `#eeeeee` to `#e3e3e3`.

## Version 0.1.1

### v0.1.1: Basic Changes

1. "Builtin Variables" are no longer bold
2. punctuation.section.embedded has been removed from "Tag".

### v0.1.1: More Detailed Changes

Group keyword operators under "Keyword" whose TextMate scopes are:

1. keyword.operator.new,
2. keyword.operator.delete,
3. keyword.operator.expression,
4. keyword.operator.arrow,
5. keyword.operator.dereference,
6. keyword.operator.unpacking

This should hopefully fix certain keywords such as Python's `in`
(in for loops) and JavaScript's `void`.

Some operators have been transferred to "Punctuation". This includes:

1. keyword.operator.assignment,
2. keyword.operator.namespace,
3. keyword.operator.access

In addition, the following scopes have been introduced to "Inline Expressions":

1. punctuation.definition.template-expression,
2. punctuation.section.embedded,
3. source.rust punctuation.definition.interpolation,
4. source.rust meta.interpolation

so that the brackets delimiting the beginning and end of an expression in an
"f-string" in Rust, Ruby and JavaScript have the same colour as the ones
I have set for Python.

Also, I somehow managed to forget TOML and the bois exist and had to change
the colours of their table names. This called for a new set under `tokenColors`
called "Ini Table".
