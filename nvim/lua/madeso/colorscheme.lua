local function generate_solarized()
    local solarized = {
        white = '#FFFFFF',
        black = '#000000',
    }

    solarized.base03     = '#002b36'
    solarized.base02     = '#073642'
    solarized.base01     = '#586e75'
    solarized.base00     = '#657b83'
    solarized.base0      = '#839496'
    solarized.base1      = '#93a1a1'
    solarized.base2      = '#eee8d5'
    solarized.base3      = '#fdf6e3'
    solarized.yellow     = '#b58900'
    solarized.orange     = '#cb4b16'
    solarized.red        = '#dc322f'
    solarized.magenta    = '#d33682'
    solarized.violet     = '#6c71c4'
    solarized.blue       = '#268bd2'
    solarized.cyan       = '#2aa198'
    solarized.green      = '#859900'

    if vim.o.background == 'dark' then
        solarized.heavy = solarized.base3
        solarized.strong = solarized.base2
        solarized.emph = solarized.base1
        solarized.text = solarized.base0
        solarized.comment = solarized.base01
        solarized.highlight = solarized.base02
        solarized.back = solarized.base03
    else
        solarized.heavy = solarized.base03
        solarized.strong = solarized.base02
        solarized.emph = solarized.base01
        solarized.text = solarized.base00
        solarized.comment = solarized.base1
        solarized.highlight = solarized.base2
        solarized.back = solarized.base3
    end
    return solarized
end

local function generate_alabaster(solarized)
    local alabaster = {}
    
    alabaster.strings = solarized.green
    alabaster.constants = solarized.blue
    alabaster.comments = solarized.strong
    alabaster.globals = solarized.emph
    alabaster.text = solarized.text

    return alabaster
end

-- terminal and group functions heavily inspired by https://github.com/Shatur/neovim-ayu/tree/

local function set_terminal_colors(s, a)
    local bg = s.back
    local fg = s.text
    local fg_idle = s.highlight

    local accent = s.orange
    local comment = s.comment
    local constant = s.emph
    local error = s.red
    local markup = s.blue
    local regexp = s.magenta
    local string = s.green
    local tag = s.violet

    vim.g.terminal_color_0 = bg
    vim.g.terminal_color_1 = markup
    vim.g.terminal_color_2 = string
    vim.g.terminal_color_3 = accent
    vim.g.terminal_color_4 = tag
    vim.g.terminal_color_5 = constant
    vim.g.terminal_color_6 = regexp
    vim.g.terminal_color_7 = fg
    vim.g.terminal_color_8 = fg_idle
    vim.g.terminal_color_9 = error
    vim.g.terminal_color_10 = string
    vim.g.terminal_color_11 = accent
    vim.g.terminal_color_12 = tag
    vim.g.terminal_color_13 = constant
    vim.g.terminal_color_14 = regexp
    vim.g.terminal_color_15 = comment
    vim.g.terminal_color_background = bg
    vim.g.terminal_color_foreground = fg
end

local function generate_groups(s, a)
    local unknown = s.red

    local colors = {}

    colors.accent = s.blue
    colors.bg = s.back
    colors.fg = s.text
    colors.ui = s.text
    
    colors.tag = s.blue
    colors.func = a.text
    colors.entity = a.text
    colors.string = a.strings
    colors.regexp = a.strings
    colors.markup = a.text
    colors.keyword = a.text
    colors.special = a.text
    colors.comment = a.comment
    colors.constant = a.constants
    colors.operator = a.text
    colors.error = s.red
    colors.lsp_parameter = s.comment

    colors.line = s.highlight
    colors.panel_bg = s.back
    colors.panel_shadow = s.back
    colors.panel_border = s.text
    colors.gutter_normal = s.highlight
    colors.gutter_active = s.highlight
    colors.selection_bg = s.highlight
    colors.selection_inactive = s.highlight
    colors.selection_border = s.text
    colors.guide_active = s.highlight
    colors.guide_normal = s.text

    colors.vcs_added = s.green
    colors.vcs_modified = s.blue
    colors.vcs_removed = s.red

    colors.vcs_added_bg = s.highlight
    colors.vcs_removed_bg = s.highlight

    colors.fg_idle = s.text
    colors.warning = s.red

    local groups = {
        -- Base.
        Normal = { fg = colors.fg, bg = colors.bg },
        NormalFloat = { bg = colors.bg },
        FloatBorder = { fg = colors.comment },
        FloatTitle = { fg = colors.fg },
        ColorColumn = { bg = colors.line },
        Cursor = { fg = colors.bg, bg = colors.fg },
        CursorColumn = { bg = colors.line },
        CursorLine = { bg = colors.line },
        CursorLineNr = { fg = colors.accent, bg = colors.line },
        LineNr = { fg = colors.guide_normal },

        Directory = { fg = colors.func },
        ErrorMsg = { fg = colors.error },
        VertSplit = { fg = colors.panel_border, bg = colors.bg },
        Folded = { fg = colors.fg_idle, bg = colors.panel_bg },
        FoldColumn = { bg = colors.bg },
        SignColumn = { bg = colors.bg },

        MatchParen = { sp = colors.func, underline = true },
        ModeMsg = { fg = colors.string },
        MoreMsg = { fg = colors.string },
        NonText = { fg = colors.guide_normal },
        Pmenu = { fg = colors.fg, bg = colors.selection_inactive },
        PmenuSel = { fg = colors.fg, bg = colors.selection_inactive, reverse = true },
        Question = { fg = colors.string },
        Search = { fg = colors.bg, bg = colors.constant },
        CurSearch = { fg = colors.bg, bg = colors.special },
        IncSearch = { fg = colors.keyword, bg = colors.selection_inactive },
        SpecialKey = { fg = colors.selection_inactive },
        SpellCap = { sp = colors.tag, undercurl = true },
        SpellLocal = { sp = colors.keyword, undercurl = true },
        SpellBad = { sp = colors.error, undercurl = true },
        SpellRare = { sp = colors.regexp, undercurl = true },
        StatusLine = { fg = colors.fg, bg = colors.panel_bg },
        StatusLineNC = { fg = colors.fg_idle, bg = colors.panel_bg },
        WildMenu = { fg = colors.fg, bg = colors.markup },
        TabLine = { fg = colors.comment, bg = colors.panel_shadow },
        TabLineFill = { fg = colors.fg, bg = colors.panel_border },
        TabLineSel = { fg = colors.fg, bg = colors.bg },
        Title = { fg = colors.keyword },
        Visual = { bg = colors.selection_inactive },
        WarningMsg = { fg = colors.warning },

        Comment = { fg = colors.comment, italic = true },
        Constant = { fg = colors.constant },
        String = { fg = colors.string },
        Identifier = { fg = colors.entity },
        Function = { fg = colors.func },
        Statement = { fg = colors.keyword },
        Operator = { fg = colors.operator },
        Exception = { fg = colors.markup },
        PreProc = { fg = colors.accent },
        Type = { fg = colors.entity },
        Structure = { fg = colors.special },
        Special = { fg = colors.accent },
        Delimiter = { fg = colors.special },
        Underlined = { sp = colors.tag, underline = true },
        Ignore = { fg = colors.fg },
        Error = { fg = colors.white, bg = colors.error },
        Todo = { fg = colors.markup },
        qfLineNr = { fg = colors.keyword },
        qfError = { fg = colors.error },
        Conceal = { fg = colors.comment },
        CursorLineConceal = { fg = colors.guide_normal, bg = colors.line },

        DiffAdd = { bg = colors.vcs_added_bg },
        DiffAdded = { fg = colors.vcs_added },
        DiffDelete = { bg = colors.vcs_removed_bg },
        DiffRemoved = { fg = colors.vcs_removed },
        DiffText = { bg = colors.gutter_normal },
        DiffChange = { bg = colors.selection_inactive },

        -- LSP.
        DiagnosticError = { fg = colors.error },
        DiagnosticWarn = { fg = colors.keyword },
        DiagnosticInfo = { fg = colors.tag },
        DiagnosticHint = { fg = colors.regexp },

        DiagnosticUnderlineError = { sp = colors.error, undercurl = true },
        DiagnosticUnderlineWarn = { sp = colors.keyword, undercurl = true },
        DiagnosticUnderlineInfo = { sp = colors.tag, undercurl = true },
        DiagnosticUnderlineHint = { sp = colors.regexp, undercurl = true },

        -- Markdown.
        markdownCode = { fg = colors.special },

        -- TreeSitter.
        ['@property'] = { fg = colors.tag },
        ['@tag'] = { fg = colors.keyword },
        ['@tag.attribute'] = { fg = colors.entity },
        ['@tag.delimiter'] = { link = 'Delimiter' },
        ['@type.qualifier'] = { fg = colors.keyword },
        ['@variable'] = { fg = colors.fg },
        ['@variable.builtin'] = { fg = colors.func },
        ['@variable.member'] = { fg = colors.tag },
        ['@variable.parameter'] = { fg = colors.fg },
        ['@module'] = { fg = colors.func },
        ['@markup.heading'] = { fg = colors.keyword },
        ['@keyword.storage'] = { fg = colors.keyword },

        ['@lsp.type.namespace'] = { link = '@module' },
        ['@lsp.type.type'] = { link = '@type' },
        ['@lsp.type.class'] = { link = '@type' },
        ['@lsp.type.enum'] = { link = '@type' },
        ['@lsp.type.interface'] = { link = '@type' },
        ['@lsp.type.struct'] = { link = '@variable.member' },
        ['@lsp.type.parameter'] = { fg = colors.lsp_parameter },
        ['@lsp.type.field'] = { link = '@variable.member' },
        ['@lsp.type.variable'] = { link = '@variable' },
        ['@lsp.type.property'] = { link = '@property' },
        ['@lsp.type.enumMember'] = { link = '@constant' },
        ['@lsp.type.function'] = { link = '@function' },
        ['@lsp.type.method'] = { link = '@function.method' },
        ['@lsp.type.macro'] = { link = '@function.macro' },
        ['@lsp.type.decorator'] = { link = '@function' },
        ['@lsp.mod.constant'] = { link = '@constant' },

        -- TreesitterContext.
        TreesitterContext = { bg = colors.selection_inactive },

        -- Gitsigns.
        GitSignsAddLn = { fg = colors.vcs_added },
        GitSignsDeleteLn = { fg = colors.vcs_removed },
        GitSignsChange = { fg = colors.vcs_modified },

        -- Telescope.
        TelescopePromptBorder = { fg = colors.accent },

        -- Cmp.
        CmpItemAbbrMatch = { fg = colors.keyword },
        CmpItemAbbrMatchFuzzy = { fg = colors.func },
        CmpItemKindText = { fg = colors.string },
        CmpItemKindMethod = { fg = colors.keyword },
        CmpItemKindFunction = { fg = colors.func },
        CmpItemKindConstructor = { fg = colors.keyword },
        CmpItemKindField = { fg = colors.entity },
        CmpItemKindVariable = { fg = colors.tag },
        CmpItemKindClass = { fg = colors.entity },
        CmpItemKindInterface = { fg = colors.entity },
        CmpItemKindModule = { fg = colors.keyword },
        CmpItemKindProperty = { fg = colors.keyword },
        CmpItemKindUnit = { fg = colors.constant },
        CmpItemKindValue = { fg = colors.constant },
        CmpItemKindEnum = { fg = colors.entity },
        CmpItemKindKeyword = { fg = colors.keyword },
        CmpItemKindSnippet = { fg = colors.regexp },
        CmpItemKindColor = { fg = colors.special },
        CmpItemKindFile = { fg = colors.special },
        CmpItemKindReference = { fg = colors.special },
        CmpItemKindFolder = { fg = colors.special },
        CmpItemKindEnumMember = { fg = colors.constant },
        CmpItemKindConstant = { fg = colors.constant },
        CmpItemKindStruct = { fg = colors.entity },
        CmpItemKindEvent = { fg = colors.tag },
        CmpItemKindOperator = { fg = colors.operator },
        CmpItemKindTypeParameter = { fg = colors.tag },
        CmpItemMenu = { fg = colors.comment },

        -- Word under cursor.
        CursorWord = { bg = colors.selection_inactive },
        CursorWord0 = { bg = colors.selection_inactive },
        CursorWord1 = { bg = colors.selection_inactive },

        -- Noice
        NoiceLspProgressTitle = { fg = colors.fg },
        NoiceLspProgressClient = { fg = colors.special },

        -- NvimTree.
        NvimTreeGitDirty = { fg = colors.accent },
        NvimTreeGitStaged = { fg = colors.vcs_modified },
        NvimTreeGitMerge = { fg = colors.error },
        NvimTreeGitNew = { fg = colors.vcs_added },
        NvimTreeGitDeleted = { fg = colors.vcs_removed },

        NvimTreeFolderName = { fg = colors.special },
        NvimTreeFolderIcon = { fg = colors.accent },
        NvimTreeOpenedFolderName = { fg = colors.special },
        NvimTreeRootFolder = { fg = colors.keyword },
        NvimTreeSpecialFile = { fg = colors.fg },
        NvimTreeExecFile = { fg = colors.fg },
        NvimTreeIndentMarker = { fg = colors.guide_normal },

        NvimTreeWindowPicker = { fg = colors.keyword, bg = colors.panel_border, bold = true },

        -- Neo-tree.
        NeoTreeRootName = { fg = colors.fg, bold = true },

        -- WhichKey.
        WhichKeyFloat = { bg = colors.bg },

        -- Indent blankline.
        IndentBlanklineContextChar = { fg = colors.comment },

        -- Neogit.
        NeogitDiffContextHighlight = { bg = colors.line },
        NeogitHunkHeader = { fg = colors.tag },
        NeogitHunkHeaderHighlight = { fg = colors.tag, bg = colors.line },
        NeogitDiffAddHighlight = { bg = colors.vcs_added_bg },
        NeogitDiffDeleteHighlight = { bg = colors.vcs_removed_bg },

        -- Hop.
        HopNextKey = { fg = colors.keyword, bold = true, underline = true },
        HopNextKey1 = { fg = colors.entity, bold = true, underline = true },
        HopNextKey2 = { fg = colors.tag },
        HopUnmatched = { fg = colors.comment },

        -- Leap.
        LeapMatch = { fg = colors.regexp, underline = true },
        LeapLabelPrimary = { fg = colors.bg, bg = colors.regexp },
        LeapLabelSecondary = { fg = colors.bg, bg = colors.entity },
        LeapLabelSelected = { fg = colors.bg, bg = colors.tag },

        -- LSP Signature.
        LspSignatureActiveParameter = { italic = true },

        -- Notify.
        NotifyERROR = { fg = colors.vcs_removed },
        NotifyWARN = { fg = colors.func },
        NotifyINFO = { fg = colors.vcs_added },
        NotifyDEBUG = { fg = colors.comment },
        NotifyTRACE = { fg = colors.vcs_modified },
        NotifyERRORTitle = { fg = colors.error },
        NotifyWARNTitle = { fg = colors.warning },
        NotifyINFOTitle = { fg = colors.string },
        NotifyDEBUGTitle = { fg = colors.ui },
        NotifyTRACETitle = { fg = colors.entity },

        -- Dap.
        NvimDapVirtualText = { fg = colors.regexp },

        -- DAP UI.
        DapUIScope = { fg = colors.func },
        DapUIType = { fg = colors.entity },
        DapUIDecoration = { fg = colors.tag },
        DapUIThread = { fg = colors.string },
        DapUIStoppedThread = { fg = colors.special },
        DapUISource = { fg = colors.regexp },
        DapUILineNumber = { fg = colors.constant },
        DapUIFloatBorder = { fg = colors.panel_border },
        DapUIWatchesEmpty = { fg = colors.warning },
        DapUIWatchesValue = { fg = colors.string },
        DapUIWatchesError = { fg = colors.error },
        DapUIBreakpointsPath = { fg = colors.regexp },
        DapUIBreakpointsInfo = { fg = colors.constant },
        DapUIBreakpointsCurrentLine = { fg = colors.constant, bold = true },

        -- Visual Multi.
        VM_Extend = { bg = colors.selection_inactive },
        VM_Cursor = { bg = colors.selection_inactive, sp = colors.fg, underline = true },
        VM_Insert = { sp = colors.fg, underline = true },
        VM_Mono = { fg = colors.bg, bg = colors.comment },
    }
    return groups
end

local function set_groups(s, a)
    local groups = generate_groups(s, a)
    for group, parameters in pairs(groups) do
        vim.api.nvim_set_hl(0, group, parameters)
    end
end

local function set_colors(solarized, alabaster)
    set_terminal_colors(solarized, alabaster)
    set_groups(solarized, alabaster)
end


local scheme = {}
function scheme.setup()
    local solarized = generate_solarized()
    local alabaster = generate_alabaster(solarized)
    set_colors(solarized, alabaster)
end

return scheme