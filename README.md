# rbase24

A command line tool to print base16/base24 color schemes to the terminal.

To specify the location of the color scheme files either...

1. Set the `BASE24_SCHEME_DIR` environment variable to point to the directory
   containing the scheme files.
2. Create a `config.ini` file in `$HOME/.config/rbase24` with a single entry
   
   ```ini
   scheme_dir = "<scheme file directory>"
   ```

Run the `rbase24` command passing an optional filespec to filter the list of
files.

The filespec will have `\*` and `.yaml` added if necessary so
`gruvbox`, `gruvbox\*` and `gruvbox*.yaml` mean the same.

```bash
rbase24 primer
```

Displays the following

![console output](https://github.com/sffjunkie/rbase24/blob/main/src/doc/swappy-20240422-174952.png)
