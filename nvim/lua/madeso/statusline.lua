local stat = {}

-- inspired by
-- https://zignar.net/2022/01/21/a-boring-statusline-for-neovim/
-- https://nuxsh.is-a.dev/blog/custom-nvim-statusline.html#org1a20509
-- https://gabri.me/blog/diy-vim-statusline

function stat.statusline()
    local parts = {

        "%f ",                          -- file name
        "\\ ",
        "[%{strlen(&fenc)?&fenc:'none'},", --file encoding
        "%{&ff}]", --file format
        "%y",      --filetype
        "%h",      --help file flag
        "%m",      --modified flag
        "%r",      --read only flag
        "\\" ,
        -- %{SyntaxItem()}

        -- Puts in the current git status
        -- if count(g:pathogen_disabled, 'Fugitive') < 1   
        --  %{fugitive#statusline()}
        -- endif

        -- Puts in syntastic warnings
        --if count(g:pathogen_disabled, 'Syntastic') < 1  
        -- %#warningmsg#
        -- %{SyntasticStatuslineFlag()}
        -- %*
        -- endif


        "\\ %=",                        -- align left
        -- Line:%l/%L[%p%%]            -- line X of Y [percent of file]
        "ln:%l/%L",                    -- line X of Y
        "\\ Col:%c",                    -- current column
        "\\ Buf:%n"                    -- Buffer number
        -- \ [%b][0x%B]\               -- ASCII and byte code under cursor

    }

    return table.concat(parts, " ")
end

function stat.setup()
    vim.api.nvim_win_set_option(0, "statusline", "%!v:lua.require'madeso.statusline'.statusline()")
end

return stat