# LiVer v0.1.0

This is a VSCode theme which uses colours mainly between lilac and vermillion.
It also tries to limit the use of bold and italic font styles to markup files
such as markdown. If you would like to disable font styles, you can add
these configurations to your `settings.json`.

```json
"editor.tokenColorCustomizations": {
    "textMateRules": [
        {
            "name": "Disable Font Styles",
            "scope": [
                "variable.other.constant",
                "variable.language",
                "constant.language",
                "constant.other.caps.python",
                "markup.bold",
                "markup.bold string",
                "markup.bold markup.italic",
                "markup.italic markup.bold",
                "markup.quote markup.bold",
                "markup.bold markup.italic string",
                "markup.italic markup.bold string",
                "markup.quote markup.bold string",

                "comment",
                "punctuation.definition.comment",
                "text.html.basic entity.other.attribute-name.html",
                "text.html.basic entity.other.attribute-name",
                "markup.italic",
                "markup.quote",
            ],
            "settings": {
                "fontStyle": "normal"
            }
        }
    ]
}
```
