# Third-party implementation and modifications

The MCP server, OAuth implementation, process sessions, recall store, worktree management and the base Docker runtime are NOT authored here. They come from `repairer5812/webjjonku` at `e0cef9118f612ed148c6db2806f1f8b6ea2661ad`, using `starlove7/spacedock` at `41df6ed1519242e742079c84989cd15b5a4e441b`.

Our layer changes the allowed-root configuration (demo, agentflow-open, shared), disables command execution for the shared knowledge root, and adapts the upstream live diagnostic to the demo root and non-misleading endpoint labels. The original configure and diagnostic files are retained in the image. The user-facing setup script orchestrates the existing implementation; it does not implement a replacement MCP server.

The upstream image retains its LICENSE and THIRD_PARTY_NOTICES.md, including SpaceDock, Cloudflared and UI notices. The diagnostic adaptation follows its MIT license:

MIT License

Copyright (c) 2026 repairer5812

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
