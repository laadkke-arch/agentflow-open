-- AF-RES-096 P4: researcher synthesis, NOT an executed success receipt.
-- Based on the pinned Pandoc 3.6 Lua-filter example, GPL-2.0-or-later:
-- https://github.com/jgm/pandoc/blob/8a72b8449ddccd84fcdffc1a09ae18c4baaca32a/doc/lua-filters.md
-- Original request and exact libraries/settings:
-- https://stackoverflow.com/revisions/79393445/1
-- Scope: the supplied single tikzpicture environment; HTML output only.

local system = require 'pandoc.system'

-- The original example's package/library/global settings are deliberately
-- carried into the isolated image compile; do not silently drop them.
local preamble = [[
\documentclass{standalone}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{automata, positioning, arrows}
\tikzset{->, >=stealth', node distance=3cm, every state/.style={thick, fill=gray!10}, initial text=$ $,}
\begin{document}
\nopagecolor
]]

function RawBlock(el)
  if el.format ~= 'latex' and el.format ~= 'tex' then
    return nil
  end
  -- Unlike the minimal published example, tolerate leading whitespace.
  -- This is intentionally scoped to the R0's non-nested tikzpicture.
  local picture = el.text:match('(\\begin{tikzpicture}.-\\end{tikzpicture})')
  if not picture then
    return nil
  end

  local tex = preamble .. picture .. '\n\\end{document}\n'
  local basename = 'af096-tikz-' .. pandoc.sha1(tex) .. '.svg'
  local destination = system.get_working_directory() .. '/' .. basename

  system.with_temporary_directory('af096-tikz', function(tmpdir)
    system.with_working_directory(tmpdir, function()
      local handle = assert(io.open('diagram.tex', 'w'))
      handle:write(tex)
      handle:close()
      -- Command, arguments, and stdin are separate. A nonzero exit propagates.
      pandoc.pipe('pdflatex',
                  {'-interaction=nonstopmode', '-halt-on-error', 'diagram.tex'}, '')
      pandoc.pipe('pdf2svg', {'diagram.pdf', destination}, '')
    end)
  end)

  return pandoc.Para({pandoc.Image({}, basename)})
end
