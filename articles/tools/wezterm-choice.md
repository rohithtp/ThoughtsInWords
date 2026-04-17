## Why I Chose WezTerm over Alacritty and Kitty

I picked WezTerm as my daily terminal because it strikes the best balance of modern features, performance, and licensing compared to Alacritty and Kitty.

### Key reasons

- **Native GPU acceleration + modern features:** WezTerm uses GPU acceleration for fast rendering and adds first-class features such as built-in split panes, tabs, multiplexing-like session management, and a powerful Lua-based configuration system. That makes it a one-stop replacement for the typical "terminal + tmux" workflow without extra dependencies.

- **Alacritty — effectively deprecated for my needs:** Alacritty historically offered excellent GPU-accelerated rendering and simplicity, but development activity and feature additions have slowed relative to alternatives. It relies on external multiplexers (like tmux) for pane management and lacks some of the higher-level conveniences WezTerm provides out of the box.

- **Kitty — good but GPL-related dependency concerns:** Kitty is very capable, with native panes and GPU acceleration, but its licensing (GPL) and some dependencies gave me pause when I preferred a more permissive ecosystem and simpler dependency profile. If someone is comfortable with GPL tooling, Kitty remains an excellent option.

### Practical implications

- With WezTerm you get a modern, fast terminal emulator that reduces the need for extra tools (multiplexer, complex scripting), while keeping a highly flexible config via Lua.
- Choosing WezTerm simplifies setup and maintenance, especially via Homebrew (brew install --cask wezterm).
- If you need a strictly minimal or very lightweight renderer and don't mind using tmux for panes, Alacritty still makes sense; if GPL licensing is fine, Kitty is a strong alternative.

### One-line verdict

WezTerm: best mix of GPU performance, built-in multiplexing, and flexible configuration — my daily driver.
