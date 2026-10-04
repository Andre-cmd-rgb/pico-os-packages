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
downloads a package's source and checks it against that line.

Every package is also compiled here, by GitHub Actions
(`.github/workflows/build.yml`), with pico-os's own compiler: the
programs are in `images/`, and `images.txt` lists each with the SHA-256
of the source it was made from. The board takes the program for the very
source it has, checks its SHA-256, and runs `picoc -t` on it -- the
loader and verifier, without running it -- so no compiling is done on
the board. When there is none that fits (a board on an older pico-os,
say), it compiles the source itself with its own `picoc`. A name that is
already one of the board's own commands is refused.

The build runs on every push to `main` and every day, so the programs
follow the compiler: a package that does not compile fails it, and the
programs and both indexes are committed again whenever they change.

## Adding one

1. `packages/NAME/NAME.pico`, with `int main(str[] args)`, and
   `packages/NAME/package.txt` with its version and about line.
2. Try it on the board first: `pico NAME.pico`.
3. Push: the build compiles it and writes both indexes.
4. Raise the version whenever the source changes, so `pkg upgrade` sees it.
