# Overview

This is a factorio mod and python library for reading and writing current factorio
game stats to a local UDP socket. 

# Exported Stats

Below is a table of all of the stats that the mod exports. All of them but
`player-health-ratio` and `tick` are cumulative totals from the start of the save.

The stats are generally exported roughly every second and may be on a slight delay.
Expect maybe an update every second for them to be delayed by maybe a second or so. Some
stats also update at different frequencies, notably, the tick count is updated more
quickly than the rest.

Stats exported:

| Statistic               | Key format             |  Type / range | 
| ----------------------- | ---------------------- | ------------: | 
| Tick                    | `tick`                 | Number        | 
| Items produced          | `produced-<item_name>` | Number        | 
| Items consumed          | `consumed-<item_name>` | Number        | 
| Tech researched         | `tech-<tech_name>`     | 0/1           | 
| Player health           | `player-health-ratio`  | float (0–1)   | 
| Entities lost/destroyed | `lost-<entity_name>`   | Number        | 
| Lives lost (character)  | `lost-character`       | Number        | 

# Limitations

The mod only supports single player games and exporting Nauvis-only stats. Feel free
to fork the project or file a feature request if want/need broader support.

# Usage

To install this mod, copy or symlink it in to your .../factorio/mods folder.

To use this mod, you must start factorio with the  `--enable_udp_port <factorio_listen_port>`.
The mod doesn't use the listening port, so unless it's needed for any other mods, you
can set an arbitrary available port on your machine.

# Configuration

The mod's settings can be configured with the `settings.lua` or `settings.lua.tpl`
files. The first file is the settings the mod is using, and the second file is a
templated version you can use to programmatically generate the settings file, though
you'll need to provide your own template evaluator.
