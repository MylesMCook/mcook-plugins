# Attribution

The native feedback integration and setup code are authored by Myles Cook and
distributed under this plugin's MIT license. Burf test snapshots retain Burf and
upstream Berth/Shipyard MIT authorship and the original copyright/permission
notice in [the fixture license](skills/wails/assets/native-feedback/tests/fixtures/LICENSE).

The optional frontend dependency is [Agentation](https://www.agentation.com/),
pinned to 3.1.2. It and the optional `agentation-mcp` 1.3.2 companion use the
PolyForm Shield license; this plugin's MIT license does not replace their terms.
Installed dependencies retain their own license files. The runner copies the
companion's license beside its generated private CLI adapter.

The companion adapter verifies SHA-256
`5ab7f2ed13dc966d7265a0a6815a0757e673a9615dd6966dfaac7bd8a2345612`
before redirecting only its data-directory selection. Generated CLI bytes and
private data are excluded from source control and are not bundled in this plugin.

[Wails](https://github.com/wailsapp/wails) provides the desktop runtime under
the MIT license. The initial target pins Wails v3.0.0-beta.28; later versions
need version-specific verification before changing bridge assumptions.

The optional development adapter matches the full runtime emitted by
`@stylexjs/unplugin` 0.19.1, whose package declares MIT. StyleX remains an
existing application dependency; the adapter changes its in-memory Vite output
only in feedback mode. No upstream package or complete runtime is vendored.
