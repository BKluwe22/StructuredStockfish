# Structured Stockfish

## Primary Aim 
Extend functionality of Stockfish 15.1 for developing programs/GUIs designed for self-guided analysis.

## Changes from Stockfish 15.1
Added two commands: ```structuredEval``` and ```structuredGo```. Everything else is Stockfish 15.1 as you know it.
As the names suggest, the functionality of these commands is effectively identical to ```eval``` and ```go```, respectively. However, the output is JSON which makes using their outputs much easier for developers. 

## Motivation
Although I'm bad at chess **:((((** I really enjoy playing it. After losing my games, I frequently cry as Game Review shows me how I hung my queen and blundered mate in one. On a more serious note, I usually have trouble understanding deeper engine lines when I do self-analysis. I think adding information other than just lines would help me and other chess players understand the game better.  

Stockfish provides a beautiful, understandable evaluation visualization for the "eval" command. See the position evaluation below after e2e4:
```
eval
Received command: eval
info string NNUE evaluation using nn-ad9b42354671.nnue enabled

 Contributing terms for the classical eval:
+------------+-------------+-------------+-------------+
|    Term    |    White    |    Black    |    Total    |
|            |   MG    EG  |   MG    EG  |   MG    EG  |
+------------+-------------+-------------+-------------+
|   Material |  ----  ---- |  ----  ---- |  0.06 -0.08 |
|  Imbalance |  ----  ---- |  ----  ---- |  0.00  0.00 |
|      Pawns |  0.12 -0.02 |  0.13 -0.02 | -0.02  0.00 |
|    Knights | -0.02 -0.11 | -0.02 -0.11 |  0.00  0.00 |
|    Bishops | -0.00 -0.21 | -0.00 -0.21 |  0.00  0.00 |
|      Rooks | -0.15 -0.04 | -0.15 -0.04 |  0.00  0.00 |
|     Queens |  0.00  0.00 |  0.00  0.00 |  0.00  0.00 |
|   Mobility | -0.13 -0.17 | -0.50 -0.66 |  0.38  0.49 |
|King safety |  0.53 -0.06 |  0.46 -0.06 |  0.07  0.00 |
|    Threats |  0.00  0.00 |  0.02  0.02 | -0.02 -0.02 |
|     Passed |  0.00  0.00 |  0.00  0.00 |  0.00  0.00 |
|      Space |  0.29  0.00 |  0.17  0.00 |  0.12  0.00 |
|   Winnable |  ----  ---- |  ----  ---- |  0.00  0.11 |
+------------+-------------+-------------+-------------+
|      Total |  ----  ---- |  ----  ---- |  0.59  0.50 |
+------------+-------------+-------------+-------------+

 NNUE derived piece values:
+-------+-------+-------+-------+-------+-------+-------+-------+
|   r   |   n   |   b   |   q   |   k   |   b   |   n   |   r   |
| -5.27 | -4.08 | -4.26 | -6.45 |       | -4.53 | -4.29 | -5.53 |
+-------+-------+-------+-------+-------+-------+-------+-------+
|   p   |   p   |   p   |   p   |   p   |   p   |   p   |   p   |
| -0.49 | -0.94 | -0.85 | -0.93 | -0.86 | -1.34 | -1.13 | -0.41 |
+-------+-------+-------+-------+-------+-------+-------+-------+
|       |       |       |       |       |       |       |       |
|       |       |       |       |       |       |       |       |
+-------+-------+-------+-------+-------+-------+-------+-------+
|       |       |       |       |       |       |       |       |
|       |       |       |       |       |       |       |       |
+-------+-------+-------+-------+-------+-------+-------+-------+
|       |       |       |       |   P   |       |       |       |
|       |       |       |       | +1.52 |       |       |       |
+-------+-------+-------+-------+-------+-------+-------+-------+
|       |       |       |       |       |       |       |       |
|       |       |       |       |       |       |       |       |
+-------+-------+-------+-------+-------+-------+-------+-------+
|   P   |   P   |   P   |   P   |       |   P   |   P   |   P   |
| +0.64 | +1.19 | +1.03 | +0.90 |       | +1.16 | +1.14 | +0.38 |
+-------+-------+-------+-------+-------+-------+-------+-------+
|   R   |   N   |   B   |   Q   |   K   |   B   |   N   |   R   |
| +6.45 | +4.83 | +5.85 | +8.50 |       | +5.54 | +4.81 | +6.26 |
+-------+-------+-------+-------+-------+-------+-------+-------+

 NNUE network contributions (Black to move)
+------------+------------+------------+------------+
|   Bucket   |  Material  | Positional |   Total    |
|            |   (PSQT)   |  (Layers)  |            |
+------------+------------+------------+------------+
|  0         |  +  0.15   |  -  2.84   |  -  2.69   |
|  1         |  +  0.01   |  -  0.06   |  -  0.05   |
|  2         |  +  0.06   |  -  0.52   |  -  0.47   |
|  3         |  +  0.06   |  -  0.23   |  -  0.17   |
|  4         |  +  0.06   |  -  0.23   |  -  0.17   |
|  5         |  +  0.06   |  -  0.16   |  -  0.10   |
|  6         |  +  0.04   |  -  0.04   |     0.00   |
|  7         |  +  0.03   |  -  0.18   |  -  0.14   | <-- this bucket is used
+------------+------------+------------+------------+


Classical evaluation   +0.58 (white side)
NNUE evaluation        +0.14 (white side)
Final evaluation       +0.18 (white side) [with scaled NNUE, hybrid, ...]
```
Unfortunately, adding this information into a GUI is not feasible without tearing out your hair writing a parser. I'm hoping that this fork will make it easier to incorporate this information into self-analysis tools where you can see this type of evaluation for each move in an engine line.

## structuredEval
Returns the evaluation of the current position in JSON format. 
This is the general structure of the output
```
# FACTORs are: bishops, knights, rooks, queens, pawns, kingSafety, mobility, passed, space, threats, material, imbalance, winnable

# evaluations are a single value (normalized centipawns) representing the evaluation of the position. A negative value indicates an advantage for black, a positive value indicates an advantage for white.
{
    "FEN_STRING": {
        "classical": {
            "FACTOR": { 
                "black": {
                    "eg": "float", # eg = endgame evaluation score
                    "mg": "float" # mg = middlegame evaluation score
                },
                "white": {
                    "eg": "float",
                    "mg": "float"
                },
                "total": {
                    "eg": "float",
                    "mg": "float"
                }
            },
            ...
        },
        "evaluations": {
            "classical": "float", 
            "final": "float",
            "nnue": "float"
        },
        "nnue": {
            "estimatedPieceValues": {
                "SQUARE": {
                    "piece": "string",
                    "value": "float/string" <- # if there is no piece on the square, this will be "None"
                },
                ...
            },
            "networkContributions": {
                "LAYER_INDEX": {
                    "Material (PSQT)": "float", # Material evaluation from the Piece-Square Table
                    "Positional (Layers)": "float", # Positional evaluation from the neural network layer
                    "Total": "float", # Total evaluation for the layer
                    "used": "boolean" # Indicates if this layer's evaluation was used in the final evaluation.
                },
                ...
            }
        }
    }
}
```

## structuredGo
Does the same thing as ```go``` but also outputs following data when it stops
```
{
    "bestMove": "string",       // The best move determined by the engine 
    "ponder": "string",         // The move the engine expects the opponent to play next
    "searchInfo": [
        [
            {
                "bound": "string",               // Indicates if the score is a lower bound, upper bound, or exact
                "depth": "integer",              // Depth of the search in the game tree
                "enginePOVEval": "float",        // Evaluation score from the engine's point of view
                "enginePOVScore": "string",      // Evaluation score in centipawns or mate notation.
                "hashfull": "integer",           // Percentage of the transposition table (hash table) that is full
                "multipv": "integer",            // Indicates which principal variation this is (1 for best, 2 for second best, etc.)
                "nodes": "integer",              // Total number of nodes (positions) evaluated
                "nps": "integer",                // Nodes per second, indicating the engine's speed
                "pv": ["string", ...],           // Principal variation: sequence of best moves determined by the engine
                "rootFen": "string",             // FEN notation of the root position from which the search started
                "seldepth": "integer",           // Selective depth: the maximum depth reached during the search considering pruning
                "tbhits": "integer",             // Number of times the tablebase was accessed
                "time": "integer"                // Time (in milliseconds) taken for the search
            },
            ...
        ],
        ...
    ]
}
```

## How to Use Programmatically
Right now I have a simple Python script under /examples that will get you started. In this script I inherit from the Stockfish class from the [python Stockfish library](https://github.com/zhelyabuzhsky/stockfish) and add two methods (get_lines and get_eval) that incorporate structuredEval and structuredGo. Make sure that you install the python stockfish library (```pip install stockfish```) and point to the StructuredStockfish binary when you call the constructor.

## Contributing 
Please feel free to suggest modifications, raise issues, submit a PR, etc!

## Future Directions 
I will probably try to make a [Stockfish.js](https://github.com/nmrugg/stockfish.js) fork using this fork of Stockfish 15.1 so that this can be used on the web. I would also like to make a free Chess GUI that incorporates visual information about positional evaluation by Stockfish. 






# Stockfish Chess Engine README.md
## Overview

[Stockfish][website-link] is a free, powerful UCI chess engine derived from
Glaurung 2.1. Stockfish is not a complete chess program and requires a UCI-compatible
graphical user interface (GUI) (e.g. XBoard with PolyGlot, Scid, Cute Chess, eboard,
Arena, Sigma Chess, Shredder, Chess Partner or Fritz) in order to be used comfortably.
Read the documentation for your GUI of choice for information about how to use
Stockfish with it.

The Stockfish engine features two evaluation functions for chess. The efficiently
updatable neural network (NNUE) based evaluation is the default and by far the strongest.
The classical evaluation based on handcrafted terms remains available. The strongest
network is integrated in the binary and downloaded automatically during the build process.
The NNUE evaluation benefits from the vector intrinsics available on most CPUs (sse2,
avx2, neon, or similar).

## Files

This distribution of Stockfish consists of the following files:

  * [README.md][readme-link], the file you are currently reading.

  * [Copying.txt][license-link], a text file containing the GNU General Public License
    version 3.

  * [AUTHORS][authors-link], a text file with the list of authors for the project.

  * [src][src-link], a subdirectory containing the full source code, including a Makefile
    that can be used to compile Stockfish on Unix-like systems.

  * a file with the .nnue extension, storing the neural network for the NNUE evaluation.
    Binary distributions will have this file embedded.

## The UCI protocol and available options

The Universal Chess Interface (UCI) is a standard protocol used to communicate with
a chess engine, and is the recommended way to do so for typical graphical user interfaces
(GUI) or chess tools. Stockfish implements the majority of its options as described
in [the UCI protocol][uci-link].

Developers can see the default values for UCI options available in Stockfish by typing
`./stockfish uci` in a terminal, but the majority of users will typically see them and
change them via a chess GUI. This is a list of available UCI options in Stockfish:

  * #### Threads
    The number of CPU threads used for searching a position. For best performance, set
    this equal to the number of CPU cores available.

  * #### Hash
    The size of the hash table in MB. It is recommended to set Hash after setting Threads.

  * #### Clear Hash
    Clear the hash table.

  * #### Ponder
    Let Stockfish ponder its next move while the opponent is thinking.

  * #### MultiPV
    Output the N best lines (principal variations, PVs) when searching.
    Leave at 1 for best performance.

  * #### Use NNUE
    Toggle between the NNUE and classical evaluation functions. If set to "true",
    the network parameters must be available to load from file (see also EvalFile),
    if they are not embedded in the binary.

  * #### EvalFile
    The name of the file of the NNUE evaluation parameters. Depending on the GUI the
    filename might have to include the full path to the folder/directory that contains
    the file. Other locations, such as the directory that contains the binary and the
    working directory, are also searched.

  * #### UCI_AnalyseMode
    An option handled by your GUI.

  * #### UCI_Chess960
    An option handled by your GUI. If true, Stockfish will play Chess960.

  * #### UCI_ShowWDL
    If enabled, show approximate WDL statistics as part of the engine output.
    These WDL numbers model expected game outcomes for a given evaluation and
    game ply for engine self-play at fishtest LTC conditions (60+0.6s per game).

  * #### UCI_LimitStrength
    Enable weaker play aiming for an Elo rating as set by UCI_Elo. This option overrides Skill Level.

  * #### UCI_Elo
    If enabled by UCI_LimitStrength, aim for an engine strength of the given Elo.
    This Elo rating has been calibrated at a time control of 60s+0.6s and anchored to CCRL 40/4.

  * #### Skill Level
    Lower the Skill Level in order to make Stockfish play weaker (see also UCI_LimitStrength).
    Internally, MultiPV is enabled, and with a certain probability depending on the Skill Level a
    weaker move will be played.

  * #### SyzygyPath
    Path to the folders/directories storing the Syzygy tablebase files. Multiple
    directories are to be separated by ";" on Windows and by ":" on Unix-based
    operating systems. Do not use spaces around the ";" or ":".

    Example: `C:\tablebases\wdl345;C:\tablebases\wdl6;D:\tablebases\dtz345;D:\tablebases\dtz6`

    It is recommended to store .rtbw files on an SSD. There is no loss in storing
    the .rtbz files on a regular HDD. It is recommended to verify all md5 checksums
    of the downloaded tablebase files (`md5sum -c checksum.md5`) as corruption will
    lead to engine crashes.

  * #### SyzygyProbeDepth
    Minimum remaining search depth for which a position is probed. Set this option
    to a higher value to probe less aggressively if you experience too much slowdown
    (in terms of nps) due to tablebase probing.

  * #### Syzygy50MoveRule
    Disable to let fifty-move rule draws detected by Syzygy tablebase probes count
    as wins or losses. This is useful for ICCF correspondence games.

  * #### SyzygyProbeLimit
    Limit Syzygy tablebase probing to positions with at most this many pieces left
    (including kings and pawns).

  * #### Move Overhead
    Assume a time delay of x ms due to network and GUI overheads. This is useful to
    avoid losses on time in those cases.

  * #### Slow Mover
    Lower values will make Stockfish take less time in games, higher values will
    make it think longer.

  * #### nodestime
    Tells the engine to use nodes searched instead of wall time to account for
    elapsed time. Useful for engine testing.

  * #### Debug Log File
    Write all communication to and from the engine into a text file.

For developers the following non-standard commands might be of interest, mainly useful for debugging:

  * #### bench *ttSize threads limit fenFile limitType evalType*
    Performs a standard benchmark using various options. The signature of a version
    (standard node count) is obtained using all defaults. `bench` is currently
    `bench 16 1 13 default depth mixed`.

  * #### compiler
    Give information about the compiler and environment used for building a binary.

  * #### d
    Display the current position, with ascii art and fen.

  * #### eval
    Return the evaluation of the current position.

  * #### export_net [filename]
    Exports the currently loaded network to a file.
    If the currently loaded network is the embedded network and the filename
    is not specified then the network is saved to the file matching the name
    of the embedded network, as defined in evaluate.h.
    If the currently loaded network is not the embedded network (some net set
    through the UCI setoption) then the filename parameter is required and the
    network is saved into that file.

  * #### flip
    Flips the side to move.


## A note on classical evaluation versus NNUE evaluation

Both approaches assign a value to a position that is used in alpha-beta (PVS) search
to find the best move. The classical evaluation computes this value as a function
of various chess concepts, handcrafted by experts, tested and tuned using fishtest.
The NNUE evaluation computes this value with a neural network based on basic
inputs (e.g. piece positions only). The network is optimized and trained
on the evaluations of millions of positions at moderate search depth.

The NNUE evaluation was first introduced in shogi, and ported to Stockfish afterward.
It can be evaluated efficiently on CPUs, and exploits the fact that only parts
of the neural network need to be updated after a typical chess move.
[The nodchip repository][nodchip-link] provided the first version of the needed tools
to train and develop the NNUE networks. Today, more advanced training tools are
available in [the nnue-pytorch repository][pytorch-link], while data generation tools
are available in [a dedicated branch][tools-link].

On CPUs supporting modern vector instructions (avx2 and similar), the NNUE evaluation
results in much stronger playing strength, even if the nodes per second computed by
the engine is somewhat lower (roughly 80% of nps is typical).

Notes:

1) the NNUE evaluation depends on the Stockfish binary and the network parameter file
(see the EvalFile UCI option). Not every parameter file is compatible with a given
Stockfish binary, but the default value of the EvalFile UCI option is the name of a
network that is guaranteed to be compatible with that binary.

2) to use the NNUE evaluation, the additional data file with neural network parameters
needs to be available. Normally, this file is already embedded in the binary or it can
be downloaded. The filename for the default (recommended) net can be found as the default
value of the `EvalFile` UCI option, with the format `nn-[SHA256 first 12 digits].nnue`
(for instance, `nn-c157e0a5755b.nnue`). This file can be downloaded from
```
https://tests.stockfishchess.org/api/nn/[filename]
```
replacing `[filename]` as needed.

## What to expect from the Syzygy tablebases?

If the engine is searching a position that is not in the tablebases (e.g.
a position with 8 pieces), it will access the tablebases during the search.
If the engine reports a very large score (typically 153.xx), this means
it has found a winning line into a tablebase position.

If the engine is given a position to search that is in the tablebases, it
will use the tablebases at the beginning of the search to preselect all
good moves, i.e. all moves that preserve the win or preserve the draw while
taking into account the 50-move rule.
It will then perform a search only on those moves. **The engine will not move
immediately**, unless there is only a single good move. **The engine likely
will not report a mate score, even if the position is known to be won.**

It is therefore clear that this behaviour is not identical to what one might
be used to with Nalimov tablebases. There are technical reasons for this
difference, the main technical reason being that Nalimov tablebases use the
DTM metric (distance-to-mate), while the Syzygy tablebases use a variation of the
DTZ metric (distance-to-zero, zero meaning any move that resets the 50-move
counter). This special metric is one of the reasons that the Syzygy tablebases are
more compact than Nalimov tablebases, while still storing all information
needed for optimal play and in addition being able to take into account
the 50-move rule.

## Large Pages

Stockfish supports large pages on Linux and Windows. Large pages make
the hash access more efficient, improving the engine speed, especially
on large hash sizes. Typical increases are 5..10% in terms of nodes per
second, but speed increases up to 30% have been measured. The support is
automatic. Stockfish attempts to use large pages when available and
will fall back to regular memory allocation when this is not the case.

### Support on Linux

Large page support on Linux is obtained by the Linux kernel
transparent huge pages functionality. Typically, transparent huge pages
are already enabled, and no configuration is needed.

### Support on Windows

The use of large pages requires "Lock Pages in Memory" privilege. See
[Enable the Lock Pages in Memory Option (Windows)][lockpages-link]
on how to enable this privilege, then run [RAMMap][rammap-link]
to double-check that large pages are used. We suggest that you reboot
your computer after you have enabled large pages, because long Windows
sessions suffer from memory fragmentation, which may prevent Stockfish
from getting large pages: a fresh session is better in this regard.

## Compiling Stockfish yourself from the sources

Stockfish has support for 32 or 64-bit CPUs, certain hardware
instructions, big-endian machines such as Power PC, and other platforms.

On Unix-like systems, it should be easy to compile Stockfish
directly from the source code with the included Makefile in the folder
`src`. In general it is recommended to run `make help` to see a list of make
targets with corresponding descriptions.

```
    cd src
    make help
    make net
    make build ARCH=x86-64-modern
```

When not using the Makefile to compile (for instance, with Microsoft MSVC) you
need to manually set/unset some switches in the compiler command line; see
file *types.h* for a quick reference.

When reporting an issue or a bug, please tell us which Stockfish version
and which compiler you used to create your executable. This information
can be found by typing the following command in a console:

```
    ./stockfish compiler
```

## Understanding the code base and participating in the project

Stockfish's improvement over the last decade has been a great community
effort. There are a few ways to help contribute to its growth.

### Donating hardware

Improving Stockfish requires a massive amount of testing. You can donate
your hardware resources by installing the [Fishtest Worker][worker-link]
and view the current tests on [Fishtest][fishtest-link].

### Improving the code

If you want to help improve the code, there are several valuable resources:

* [In this wiki,][programming-link] many techniques used in
Stockfish are explained with a lot of background information.

* [The section on Stockfish][programmingsf-link]
describes many features and techniques used by Stockfish. However, it is
generic rather than being focused on Stockfish's precise implementation.
Nevertheless, a helpful resource.

* The latest source can always be found on [GitHub][github-link].
Discussions about Stockfish take place these days mainly in the [FishCooking][fishcooking-link]
group and on the [Stockfish Discord channel][discord-link].
The engine testing is done on [Fishtest][fishtest-link].
If you want to help improve Stockfish, please read this [guideline][guideline-link]
first, where the basics of Stockfish development are explained.


## Terms of use

Stockfish is free, and distributed under the **GNU General Public License version 3**
(GPL v3). Essentially, this means you are free to do almost exactly
what you want with the program, including distributing it among your
friends, making it available for download from your website, selling
it (either by itself or as part of some bigger software package), or
using it as the starting point for a software project of your own.

The only real limitation is that whenever you distribute Stockfish in
some way, you MUST always include the license and the full source code
(or a pointer to where the source code can be found) to generate the
exact binary you are distributing. If you make any changes to the
source code, these changes must also be made available under the GPL v3.

For full details, read the copy of the GPL v3 found in the file named
[*Copying.txt*][license-link].


[authors-link]:       https://github.com/official-stockfish/Stockfish/blob/master/AUTHORS
[build-link]:         https://github.com/official-stockfish/Stockfish/actions/workflows/stockfish.yml
[commits-link]:       https://github.com/official-stockfish/Stockfish/commits/master
[discord-link]:       https://discord.gg/GWDRS3kU6R
[fishcooking-link]:   https://groups.google.com/g/fishcooking
[fishtest-link]:      https://tests.stockfishchess.org/tests
[github-link]:        https://github.com/official-stockfish/Stockfish
[guideline-link]:     https://github.com/glinscott/fishtest/wiki/Creating-my-first-test
[license-link]:       https://github.com/official-stockfish/Stockfish/blob/master/Copying.txt
[lockpages-link]:     https://docs.microsoft.com/en-us/sql/database-engine/configure-windows/enable-the-lock-pages-in-memory-option-windows
[nodchip-link]:       https://github.com/nodchip/Stockfish
[programming-link]:   https://www.chessprogramming.org/Main_Page
[programmingsf-link]: https://www.chessprogramming.org/Stockfish
[pytorch-link]:       https://github.com/glinscott/nnue-pytorch
[rammap-link]:        https://docs.microsoft.com/en-us/sysinternals/downloads/rammap
[readme-link]:        https://github.com/official-stockfish/Stockfish/blob/master/README.md
[release-link]:       https://github.com/official-stockfish/Stockfish/releases/latest
[src-link]:           https://github.com/official-stockfish/Stockfish/tree/master/src
[stockfish128-logo]:  https://stockfishchess.org/images/logo/icon_128x128.png
[tools-link]:         https://github.com/official-stockfish/Stockfish/tree/tools
[uci-link]:           https://www.shredderchess.com/download/div/uci.zip
[website-link]:       https://stockfishchess.org
[worker-link]:        https://github.com/glinscott/fishtest/wiki/Running-the-worker:-overview

[build-badge]:        https://img.shields.io/github/workflow/status/official-stockfish/Stockfish/Stockfish?style=for-the-badge&label=stockfish&logo=github
[commits-badge]:      https://img.shields.io/github/commits-since/official-stockfish/Stockfish/latest?style=for-the-badge
[discord-badge]:      https://img.shields.io/discord/435943710472011776?style=for-the-badge&label=discord&logo=Discord
[fishtest-badge]:     https://img.shields.io/website?style=for-the-badge&down_color=red&down_message=Offline&label=Fishtest&up_color=success&up_message=Online&url=https%3A%2F%2Ftests.stockfishchess.org%2Ftests%2Ffinished
[license-badge]:      https://img.shields.io/github/license/official-stockfish/Stockfish?style=for-the-badge&label=license&color=success
[release-badge]:      https://img.shields.io/github/v/release/official-stockfish/Stockfish?style=for-the-badge&label=official%20release
[website-badge]:      https://img.shields.io/website?style=for-the-badge&down_color=red&down_message=Offline&label=website&up_color=success&up_message=Online&url=https%3A%2F%2Fstockfishchess.org
