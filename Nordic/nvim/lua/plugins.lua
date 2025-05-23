-- Setup lazy.nvim
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  local lazyrepo = "https://github.com/folke/lazy.nvim.git"
  local out = vim.fn.system({ "git", "clone", "--filter=blob:none", "--branch=stable", lazyrepo, lazypath })
  if vim.v.shell_error ~= 0 then
    vim.api.nvim_echo({
      { "Failed to clone lazy.nvim:\n", "ErrorMsg" },
      { out, "WarningMsg" },
      { "\nPress any key to exit..." },
    }, true, {})
    vim.fn.getchar()
    os.exit(1)
  end
end
vim.opt.rtp:prepend(lazypath)

-- Plugins
require("lazy").setup({
    spec = {
        {"shaunsingh/nord.nvim",
        config = function()
            vim.cmd.colorscheme("nord")
        end,
        },

        {"nvim-treesitter/nvim-treesitter",
        config = function()
            require"nvim-treesitter.configs".setup{
                ensure_installed = { "c", "python", "lua", "vim", "vimdoc", "query", "markdown", "markdown_inline" },
                sync_install = false,
                auto_install = true,
                ignore_install = { "javascript" },
                highlight = {
                    enable = true
                },
                incremental_selection = {
                    enable = true,
                    keymaps = {
                        init_selection = "<Leader>ss",
                        node_incremental = "<Leader>si",
                        scope_incremental = "<Leader>sc",
                        node_decremental = "<Leader>sd",
                    },
                },
                textobjects = {
                    select = {
                        enable = true,
                        lookahead = true,
                        keymaps = {
                            ["af"] = "@function.outer",
                            ["if"] = "@function.inner",
                            ["ac"] = "@class.outer",
                            ["ic"] = { query = "@class.inner", desc = "Select inner part of a class region" },
                            ["as"] = { query = "@local.scope", query_group = "locals", desc = "Select language scope" },
                        },
                        selection_modes = {
                            ['@parameter.outer'] = 'v', -- charwise
                            ['@function.outer'] = 'V', -- linewise
                            ['@class.outer'] = '<c-v>', -- blockwise
                        },
                        include_surrounding_whitespace = true,
                    },
                },
            }
        end,
        },

        {"nvim-treesitter/nvim-treesitter-textobjects",
        },

        {"neovim/nvim-lspconfig",
        },

        {"mason-org/mason.nvim",
        config = function()
            require("mason").setup()
        end,
        },

        {"mason-org/mason-lspconfig.nvim",
        dependencies = {"mason.nvim"},
        config = function()
            require("mason-lspconfig").setup()
        end,
        },

        {"Saghen/blink.cmp",
            dependencies = { "rafamadriz/friendly-snippets" },
            version = "1.*",

            ---@module "blink.cmp"
            ---@type blink.cmp.Config
            opts = {
                keymap = { preset = "super-tab" },

            appearance = {
                nerd_font_variant = "mono"
            },

            completion = { documentation = { auto_show = false } },

            sources = {
                default = {"lazydev", "lsp", "path", "snippets", "buffer" },
                providers = {
                    lazydev = {
                        name = "LazyDev",
                        module = "lazydev.integrations.blink",
                        -- make lazydev completions top priority (see `:h blink.cmp`)
                        score_offset = 100,
                    },
                },
            },

            fuzzy = { implementation = "prefer_rust_with_warning" }
            },
            opts_extend = { "sources.default" }
        },
        {"folke/lazydev.nvim",
            ft = "lua", -- only load on lua files
            opts = {
                library = {
                    { path = "${3rd}/luv/library", words = { "vim%.uv" } },
                },
            },
        },
        {"kylechui/nvim-surround",
            version = "^3.0.0",
            event = "VeryLazy",
            config = function()
                require("nvim-surround").setup({
                    '<C-u>', '<C-d>',
                    '<C-b>', '<C-f>',
                    '<C-y>', '<C-e>',
                    'zt', 'zz', 'zb',
                })
            end
        },
        {"lukas-reineke/indent-blankline.nvim",
        main = "ibl",
        ---@module "ibl"
        ---@type ibl.config
        opts = {},
        },
    },
    install = { colorscheme = { "nord" } },
    checker = { enabled = true },
})
