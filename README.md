# nvim-replit-v2-codeinstruct
The plugin is designed to work in the Neovim editor. The primary function of this code is to take user instructions in the form of a string, process them using `replit-v2-codeinstruct-3b.q4_1.bin`, and generate a code response based on the given instructions. 

Save file at `~/.config/nvim/rplugin/python/t2t.py`

Next, execute `:UpdateRemotePlugins` every time a remote plugin is installed, updated, or deleted.

The user can invoke the plugin by typing the `:T2T` followed by the instruction. Example,

`:T2T Write a program in C to add two numbers` 

