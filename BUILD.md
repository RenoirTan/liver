# Build Instructions

To generate themes, run:

```bash
python -m scripts generate <name of theme>...
```

where `<name of theme>` is the file name of the theme under the `templates`
folder minus the `.json` suffix at the end. So to build `liver-dark.json` and
`liver-dark-full.json`, run:

```bash
python -m scripts generate liver-dark liver-dark-full
```
