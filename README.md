# LiVer v0.1.2

*[Github Repo](https://github.com/RenoirTan/liver)*

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

## Screenshots

Some screenshots of code samples taken using
[CodeSnap](https://marketplace.visualstudio.com/items?itemName=adpyke.codesnap).

### Welcome Page

![Welcome Page](https://raw.githubusercontent.com/RenoirTan/liver/screenshots/screenshots/welcome_page.png)

### Python

![Python](https://raw.githubusercontent.com/RenoirTan/liver/screenshots/screenshots/python-s.png)

### C

![C](https://raw.githubusercontent.com/RenoirTan/liver/screenshots/screenshots/c.png)

### HTML

![HTML](https://raw.githubusercontent.com/RenoirTan/liver/screenshots/screenshots/html.png)

### JavaScript

![JavaScript](https://raw.githubusercontent.com/RenoirTan/liver/screenshots/screenshots/javascript.png)

### CSS

![CSS](https://raw.githubusercontent.com/RenoirTan/liver/screenshots/screenshots/css.png)
