# cli-solitaire
A command line interface solitaire game.

## install
Preferable method is to run it in a temporary environment using [uv](https://github.com/astral-sh/uv):
``` shell
uvx --from git+https://github.com/thurbridi/cli-solitaire cli-solitaire
```
## commands
You make moves in `cli-solitaire` using text-based inputs at the bottom of the terminal where the prompt "move " is displayed.

```
stock  waste      foundations
╭────╮            ╭────╮╭────╮╭────╮╭────╮
│   ?│            │   ♣││   ♥││   ♠││   ♦│
│    │            │    ││    ││    ││    │
╰────╯            ╰────╯╰────╯╰────╯╰────╯
╭────╮╭────╮╭────╮╭────╮╭────╮╭────╮╭────╮ tableau
│ 8 ♦││   ?││   ?││   ?││   ?││   ?││   ?│
│    │╭────╮╭────╮╭────╮╭────╮╭────╮╭────╮
╰────╯│Q  ♦││   ?││   ?││   ?││   ?││   ?│
      │    │╭────╮╭────╮╭────╮╭────╮╭────╮
      ╰────╯│K  ♥││   ?││   ?││   ?││   ?│
            │    │╭────╮╭────╮╭────╮╭────╮
            ╰────╯│10 ♠││   ?││   ?││   ?│
                  │    │╭────╮╭────╮╭────╮
                  ╰────╯│ 2 ♦││   ?││   ?│
                        │    │╭────╮╭────╮
                        ╰────╯│ 4 ♥││   ?│
                              │    │╭────╮
                              ╰────╯│J  ♣│
                                    │    │
                                    ╰────╯

move 
```
This is the list of allowed moves/commands:
- `s` pulls the next card from the stock and places it on the waste pile.
- `<amount> from [1-7] to [1-7]` moves `<amount>` cards from one column to the another on the tableau 
- `from [1-7]|w|f[1-4] to [1-7]|f` moves 1 card from a column/waste/foundation to another column/foundations 
- `win` when the stock and waste are empty and all the cards are properly ordered in the tableau, this command will start an animation and move the remaining cards on the tableau to the foundations.
- `reset` start a new random run.
- `exit` closes the game.
