# pico-os packages

Programs for [pico-os](https://github.com/Andre-cmd-rgb/pico-os), the
system of the PocketType pocket computer, written in its pico language
and installed with its `pkg` command:

```sh
pkg update            # what there is
pkg install snake     # into ~/bin: then just `snake`
pkg list              # * for what is installed
pkg upgrade           # the ones that have a new version
pkg remove snake
```

| Package | What it is |
|---|---|
| guess | guess the number from 1 to 100 |
| life | Conway's game of life in the terminal |
| mandel | an animated Mandelbrot zoom |
| matrix | digital rain, as in the film |
| snake | the game: arrows or WASD steer, eat, grow, don't crash |
| weather | the weather now anywhere, from Open-Meteo: `weather Tokyo` |

## How it works

A package is its pico source, `packages/NAME/NAME.pico`, and
`packages/NAME/package.txt`:

```
version 1.0
about what it is, in a few words
```

`index.txt` lists them all with their size and SHA-256. The board
downloads a package's source, checks it against that line, and compiles
it with its own `picoc` into `~/bin/NAME`, so a package always matches the
language the board speaks. A name that is already one of the board's own
commands is refused.

Every push to `main` is built by GitHub Actions
(`.github/workflows/build.yml`): pico-os's compiler is built, every package
compiled with it -- one that does not compile fails the build -- and the
index written again and committed when it has changed.

## Adding one

1. `packages/NAME/NAME.pico`, with `int main(str[] args)`, and
   `packages/NAME/package.txt` with its version and about line.
2. Try it on the board first: `pico NAME.pico`.
3. `python3 tools/mkindex.py > index.txt`, or let the build do it.
4. Raise the version whenever the source changes, so `pkg upgrade` sees it.
