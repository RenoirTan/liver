# LiVer v0.4.1 Changelog

## Version 0.4.1

Add arguments and parameters to "Variables".

## Version 0.4.0

Change Python API for converting templates into themes in anticipation for
palette inheritance.

Decrease the brightness of `dark-gray` and `calm-black` to make everything
stand out more.

Simplify syntax highlighting for operators, punctuation, keywords and
string interpolation.

Constants (static) are now vermillion again.

Literals are now lilac instead of violet.

String interpolators and formatting sequences are now yellow.

## Version 0.3.0

Added Liver Purple and Liver Purple Full, derivatives of Liver Dark and
Liver Dark Full respectively with violet backgrounds with white as the accent
colour.

Added Yellow.

Orchid is now brighter, but is still unused.

Lavender renamed to violet. This means any setting that uses violet will now
look like lavender.

Dark-silver, light-gray and dark-gray added to dark.json for more granular
control of colours.

Make calm-gray darker.

New palette called purple.json added and is derived from dark.json.

Generator colours have been renamed so that they do not reference any specific
colour (helps with portability).

The colour of the icons in the activity bar and inactive line numbers has
been brightened.

The minimap slider's colour will be the same as the scrollbar when you hover
your mouse over it.

The scrollbar is now less transparent when you hover over it.

Shadows are now coloured.

Dereference (`*ptr`) and unpacking operators (`...args`) have been removed from
"Keyword Operator".

Escape characters are now yellow and not cyan.

"Ini Table" names are now blue-violet.

## Version 0.2.2

Fix colour of the `noexcept` keyword (keyword.operator.noexcept) in a
constructor with member initialisation lists so that it is treated as a keyword
instead of as an operator.

Fix error where a hex RGB literal results in a `ValueError`.

Remove special colours for markup font styles specified by the users
and instead give them special font styles to allow users to tell them apart
by default in *Liver Dark*.

Keys reorganised into 3 types:

1. Config Key (key, white): For keys in style files like CSS.
2. Json Key (jsonkey, fuchsia): For keys in JSON.
3. Ini Key (inikey, fuchsia): For keys in Ini-like files (e.g. TOML),
   previously "Configuration File Key".

Colour literals now have their own token style: "Color Literal" (Lilac)

`keyword.other.unit` added to "Keyword".
(e.g. The px in 5px in a typical CSS file)

Remove `source.python punctuation` from "Punctuation".

`punctuation.definition.decorator` removed from "Punctuation". This means
their colour now inherits from the entity it is attached to.

Remove `meta.function-call` from "Function, Method" to remove
weird rendering behaviour.

Markup inline code now correctly renders as vermillion.

Add `storage.type.generic` to "Types, Class, Support, Imports" otherwise it
will be coloured like a keyword in Java.

## Version 0.2.1

Fix progress bar colour to match other accented elements.

Flip the order of versions in this Changelog.

## Version 0.2.0

Overhaul the entire theme generation process:

1. Themes will be generated from ./templates and dumped into ./themes.
2. Themes no longer require an explicit hex color value. Instead, you can
choose a palette and define additional colors and styles, whose names you
can use as substitutes to the actual hex color values. For example, the
color "red" in the palette dark.json maps to `#ff1a1a`, which will be the
value used in the actual theme.
3. Scripts have been written to help generate themes from templates.

*liver* has been renamed Liver Dark Full, which is a derivative of Liver Dark,
a theme without font styling.

Indent guides, focused items, sashes, etc. have been grouped under "accents",
whose colour is lavender.

Rename `neutral` to `centrist`.

## Version 0.1.5

Remove sample code from tracking because with them Github mistakenly
counts them as part of the repo.

Change the colour of constants and builtins from orange to red.

Merge Operator 1 and Trivial Operators and remove
keyword.operator.assignment from "Punctuation".

Change the colour of operators to red.

Classes and types are now lavender, like functions.

Ruby variables are now silver like in other languages because they don't
deserve to be special.

Arrows for return values are now grouped under "Function, Method".

## Version 0.1.4

Add imported objects to "Types, Class, Support" and rename it to
"Types, Class, Support, Imports". This fixes the bug where imports
in Java are blue-violet but should instead be lilac like all class
names.

Set "source.toml punctuation.definition.table.toml" to "Punctuation"
so that it doesn't appear purple.

Explicitly include "constant.other.boolean" to "Builtin Variables".

Add "constant.other.date" and "constant.other.datetime" to "Numbers"
so they are rendered like numbers in languages like TOML.

Add TOML to screenshots folder.

Add "punctuation.definition.metadata" to "Markdown Delimiter".

## Version 0.1.3

Add preview screenshots to README.md. I didn't want to increment the
patch number but `vsce` said I could not publish liver with the same
semver and twisted my arm into doing it.

## Version 0.1.2

1. Moved keyword operators from "Keyword" to "Keyword Operator, Operator 2".
2. Add `keyword.operator.range` (like Ruby ```..```) to "Trivial Operator".
3. Add `variable.legacy.builtin` to "Builtin Variables". This means legacy
builtins like Python's `functools.reduce` get a special orange colour to
showcase their old age.

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

## Version 0.0.x

Original version.
