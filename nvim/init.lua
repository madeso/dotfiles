if vim.loop.os_uname().sysname ~= 'Linux' then
    vim.api.nvim_exec('language en_US', true)
end

vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.autoindent = true
vim.opt.tabstop = 4
vim.opt.shiftwidth = 4
vim.opt.smarttab = true
vim.opt.softtabstop = 4

vim.o.background = "light"
require("madeso.colorscheme").setup()
require("madeso.statusline").setup()

vim.o.tabstop = 4
vim.o.shiftwidth = 4
vim.o.softtabstop = 4
vim.o.smarttab = true
vim.api.nvim_win_set_option(0, "cursorline", true)

vim.o.scrolloff = 3
vim.o.sidescrolloff = 5

-- todo:
-- packager
-- fuzzy finder: telescope
-- color theme
-- nvim-tree
-- nvim-tree/nvim-web-devicons
-- lsp server
-- tree sitter

