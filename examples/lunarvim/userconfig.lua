-- Default vim config
vim.cmd("set number") --	" Show line numbers
vim.cmd("set nowrap") --	" Wrap lines
vim.cmd("set showbreak=+++") -- 	" Wrap-broken line prefix
vim.cmd("set textwidth=100") --	" Line wrap (number of cols)
vim.cmd("set showmatch") --	" Highlight matching brace
vim.cmd("set visualbell") --	" Use visual bell (no beeping)
vim.cmd("set scrolloff=999") -- " Always keep cursor in center of screen
 
vim.cmd("set hlsearch") --	" Highlight all search results
vim.cmd("set smartcase") --	" Enable smart-case search
vim.cmd("set ignorecase") --	" Always case-insensitive
vim.cmd("set incsearch") --	" Searches for strings incrementally
 
-- vim.cmd("set autoindent") --	" Auto-indent new lines
vim.cmd("set expandtab") --	" Use spaces instead of tabs
vim.cmd("set shiftwidth=4") --" Number of auto-indent spaces
vim.cmd("set smarttab") --	" Enable smart-tabs
vim.cmd("set softtabstop=4") --" Number of spaces per Tab
 
-- Advanced
vim.cmd("set ruler") --	" Show row and column ruler information
 
vim.cmd("set undolevels=1000") --	" Number of undo levels
vim.cmd("set backspace=indent,eol,start") --	" Backspace behaviour
-- undo file
vim.cmd("set undofile") --                " Save undos after file closes
vim.cmd("set undodir=$HOME/.vim/undo") -- " where to save undo histories
vim.cmd("set undoreload=10000") --        " number of lines to save for undo

-- escape to nohl
vim.cmd("nnoremap <esc> :noh<return><esc>")

-- Don't force wrap text use a formatter instead
vim.cmd("set formatoptions-=t")

-- Interactive substitute
vim.cmd("set inccommand=nosplit")

-- Auto select the first completion https://vi.stackexchange.com/a/15403
vim.cmd("set completeopt=menu,noinsert")

-- Tab menu don't complete the whole thing
vim.cmd("set wildmode=longest,list,full")


-- LUNAR VIM
-- remove weird jk mapping in insert. See https://github.com/LunarVim/LunarVim/pull/1949/files
lvim.keys.insert_mode["jk"] = false
lvim.keys.insert_mode["jj"] = false
lvim.keys.insert_mode["kj"] = false
-- Change leader
lvim.leader = "\\"
-- Which key wait before popping up
vim.opt.timeoutlen = 500
-- Don't quit unsaved changes
vim.opt.confirm = true

-- Add plugins
lvim.plugins = {
  -- Autosave
  {
    "Pocco81/AutoSave.nvim",
    config = function()
      require("autosave").setup()
    end,
  },
  -- Lightspeed
  {
    "ggandor/lightspeed.nvim",
    event = "BufRead"
  },
}

-- Modify cmp's default to not show me ghost_text it's too visually jarring
lvim.builtin.cmp.experimental.ghost_text = false
-- cmp use enter to insert the first item
local cmp = require'cmp'
lvim.builtin.cmp.mapping["<CR>"] = cmp.mapping.confirm({select=true, behavior=cmp.ConfirmBehavior.Replace})
local opts = { noremap=true, silent=true }
vim.api.nvim_set_keymap('n', 'gh', "<cmd>lua vim.lsp.buf.hover()<CR>", opts)


