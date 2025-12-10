-- Sends game state and heartbeat messages over UDP.
--
-- Note: Currently all stats assume that player 1 is the correct
-- player to track and that surface 1, "nauvis", is the correct
-- surface to export statistics for.

settings = require("settings")

local function add_map_seed(game_state)
  game_state["seed"] = game.players[1].surface.map_gen_settings.seed
end

local function add_item_stats(game_state)
  local prod_stats = game.players[1].force.get_item_production_statistics(1)
  produced = prod_stats.input_counts
  consumed = prod_stats.output_counts
  for k, v in pairs(produced) do
    game_state["produced-"..k] = v
  end
  for k, v in pairs(consumed) do
    game_state["consumed-"..k] = v
  end
end

local function add_tech_stats(game_state)
  for name, tech in pairs(game.players[1].force.technologies) do
    if tech.researched then
      game_state["researched-" .. name] = 1
    end
  end
end

local function add_health_stats(game_state)
  if game.players[1].character ~= nil then
    game_state["player-health-ratio"] = game.players[1].character.get_health_ratio()
  else
    game_state["player-health-ratio"] = 0
    game_state["respawning"] = 1
  end
end

local function add_player_position(game_state)
  if game.players[1].character ~= nil then
    game_state["player-x"] = game.players[1].character.position.x
    game_state["player-y"] = game.players[1].character.position.y
  else
    game_state["player-x"] = 0
    game_state["player-y"] = 0
  end
end

local function add_losses_stats(game_state)
  local stats = game.players[1].force.get_kill_count_statistics(1)
  for k, v in pairs(stats.output_counts) do
    game_state["lost-" .. k] = v
  end
end

-- Set as an 'on_pre_death' event to skip the respawn menu and
-- instantly respawn the player's character.
local function skip_respawn_menu(event)
  local player = game.players[1]
  local surface = player.surface

  local spawn_target = player.force.get_spawn_position(surface.index)
  local spawn = surface.find_non_colliding_position("character", spawn_target, 16, 0.5) or spawn_target
  local new_c = surface.create_entity{
    name = "character",
    position = spawn,
    force = player.force
  }
  player.character = new_c
end

local function on_tick(event)
  if event.tick % 4 ~= 0 then
    return
  end

  send_game_state = false
  if event.tick % 32 == 0 then
    send_game_state = true
  end

  message = {}
  message["tick"] = event.tick

  if send_game_state then
    add_map_seed(message)
    add_item_stats(message)
    add_tech_stats(message)
    add_health_stats(message)
    add_player_position(message)
    add_losses_stats(message)
  end

  data = helpers.table_to_json(message)
  if settings.verbose then
    game.print(data)
  end
  helpers.send_udp(settings.port_num, data)
end

script.on_event(defines.events.on_tick, on_tick)
script.on_event(defines.events.on_pre_player_died, skip_respawn_menu)
