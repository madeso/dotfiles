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

-- todo:
-- packager
-- fuzzy finder: telescope
-- color theme
-- nvim-tree
-- nvim-tree/nvim-web-devicons
-- lsp server
-- tree sitter

