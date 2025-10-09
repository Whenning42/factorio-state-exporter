-- We manage settings with a settings template file
-- settings.lua.tpl and a generated settings.lua file
-- that exports the template specified settings in a
-- .lua file.
--
-- This strikes a nice balance between an interface 
-- that's easy to configure by hand during development
-- while also being easy for downstream software to
-- consume and configure.

${SETTINGS_AUTOGENERATION_WARNING}

return {port_num = ${PORT_NUM}, verbose = ${VERBOSE}}
