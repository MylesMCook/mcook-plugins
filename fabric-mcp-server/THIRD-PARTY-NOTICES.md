# Third-party notices

The bundled Windows executable is Fabric MCP Server 1.10.0. Its own source uses
the [ISC license](LICENSE); that license does not replace the terms of linked
third-party components.

This bundle preserves original license, copying, notice, authorship, and copyright
files from every registry package in the release's exact Cargo.lock. The set is
conservative: it includes build, development, and other-platform dependencies in
addition to the Windows runtime dependencies. Inclusion is not a claim that every
listed component is linked into the executable.

- Source release: [v1.10.0](https://github.com/MylesMCook/fabric-mcp/tree/c06920cae9defc7731448ab4419d6819d218eb94), commit `c06920cae9defc7731448ab4419d6819d218eb94`.
- Executable SHA-256: `ef5351f2c8621d8e4e2e7abffa292a1dead0b6c1dcf1ebfe24f0dc98e04cadbd`.
- [Preserved Cargo.lock](third-party-licenses/Cargo.lock).
- [Machine-readable provenance, crate archive checksums, file hashes, and coverage](third-party-licenses/manifest.json).
- Every one of the 231 registry archives was verified against its release-lockfile SHA-256 before any notice was copied. No crate build scripts or code were executed.
- Nested license directories and notices are retained, including vendored source notices in AWS-LC and ring.
- [Rust 1.95.0 toolchain notices](third-party-licenses/rust-1.95.0/source.json) preserve the standard library's MIT/Apache notices and upstream copyright inventory.

## Supplemental notice sources

The jni, jni-macros, jni-sys-macros, rmcp, and rmcp-macros archives omit their
license files. Their upstream root notices are included from the exact commit
recorded in each archive's `.cargo_vcs_info.json`, with source URLs and hashes in
the manifest.

The Android-only rustls-platform-verifier-android archive omits both license
files and VCS identity. Its MIT/Apache declarations are retained in Cargo.toml;
supplemental upstream notices come from commit
`669ace0a801ef4be8e0e23d9c534849497ee5782`, the last repository commit before
that crate's publication. Exact archive-to-commit identity is unavailable. This
package is included for lockfile coverage and is not a Windows runtime component.

These notices cover the checked-in release. Regenerate and review them whenever
the executable, Cargo.lock, toolchain, or target changes. Native platform SDK and
Microsoft runtime redistribution terms remain governed by their providers.

## Registry package index

| Package | Version | Declared license expression | Preserved notice files |
| --- | --- | --- | --- |
| `aho-corasick` | `1.1.5` | Unlicense OR MIT | [COPYING](third-party-licenses/aho-corasick-1.1.5/COPYING), [LICENSE-MIT](third-party-licenses/aho-corasick-1.1.5/LICENSE-MIT) |
| `android_system_properties` | `0.1.6` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/android_system_properties-0.1.6/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/android_system_properties-0.1.6/LICENSE-MIT) |
| `anyhow` | `1.0.104` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/anyhow-1.0.104/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/anyhow-1.0.104/LICENSE-MIT) |
| `async-trait` | `0.1.92` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/async-trait-0.1.92/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/async-trait-0.1.92/LICENSE-MIT) |
| `atomic-waker` | `1.1.2` | Apache-2.0 OR MIT | [LICENSE-APACHE](third-party-licenses/atomic-waker-1.1.2/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/atomic-waker-1.1.2/LICENSE-MIT), [LICENSE-THIRD-PARTY](third-party-licenses/atomic-waker-1.1.2/LICENSE-THIRD-PARTY) |
| `autocfg` | `1.5.1` | Apache-2.0 OR MIT | [LICENSE-APACHE](third-party-licenses/autocfg-1.5.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/autocfg-1.5.1/LICENSE-MIT) |
| `aws-lc-rs` | `1.18.0` | ISC AND (Apache-2.0 OR ISC) | [LICENSE](third-party-licenses/aws-lc-rs-1.18.0/LICENSE) |
| `aws-lc-sys` | `0.44.0` | ISC AND (Apache-2.0 OR ISC) AND Apache-2.0 AND MIT AND BSD-3-Clause AND (Apache-2.0 OR ISC OR MIT) AND (Apache-2.0 OR ISC OR MIT-0) | [LICENSE](third-party-licenses/aws-lc-sys-0.44.0/LICENSE), [LICENSE](third-party-licenses/aws-lc-sys-0.44.0/aws-lc/LICENSE), [LICENSE](third-party-licenses/aws-lc-sys-0.44.0/aws-lc/third_party/fiat/LICENSE) |
| `axum` | `0.8.9` | MIT | [LICENSE](third-party-licenses/axum-0.8.9/LICENSE) |
| `axum-core` | `0.5.6` | MIT | [LICENSE](third-party-licenses/axum-core-0.5.6/LICENSE) |
| `base64` | `0.22.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/base64-0.22.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/base64-0.22.1/LICENSE-MIT) |
| `base64` | `0.23.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/base64-0.23.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/base64-0.23.1/LICENSE-MIT) |
| `bitflags` | `2.13.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/bitflags-2.13.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/bitflags-2.13.1/LICENSE-MIT) |
| `block-buffer` | `0.10.4` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/block-buffer-0.10.4/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/block-buffer-0.10.4/LICENSE-MIT) |
| `bumpalo` | `3.20.3` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/bumpalo-3.20.3/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/bumpalo-3.20.3/LICENSE-MIT) |
| `bytes` | `1.12.1` | MIT | [LICENSE](third-party-licenses/bytes-1.12.1/LICENSE) |
| `cc` | `1.4.2` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/cc-1.4.2/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/cc-1.4.2/LICENSE-MIT) |
| `cfg-if` | `1.0.4` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/cfg-if-1.0.4/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/cfg-if-1.0.4/LICENSE-MIT) |
| `cfg_aliases` | `0.2.2` | MIT | [LICENSE](third-party-licenses/cfg_aliases-0.2.2/LICENSE) |
| `chacha20` | `0.10.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/chacha20-0.10.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/chacha20-0.10.1/LICENSE-MIT) |
| `chrono` | `0.4.45` | MIT OR Apache-2.0 | [LICENSE.txt](third-party-licenses/chrono-0.4.45/LICENSE.txt) |
| `cmake` | `0.1.58` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/cmake-0.1.58/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/cmake-0.1.58/LICENSE-MIT) |
| `combine` | `4.6.7` | MIT | [LICENSE](third-party-licenses/combine-4.6.7/LICENSE) |
| `core-foundation` | `0.10.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/core-foundation-0.10.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/core-foundation-0.10.1/LICENSE-MIT) |
| `core-foundation` | `0.9.4` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/core-foundation-0.9.4/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/core-foundation-0.9.4/LICENSE-MIT) |
| `core-foundation-sys` | `0.8.7` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/core-foundation-sys-0.8.7/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/core-foundation-sys-0.8.7/LICENSE-MIT) |
| `cpufeatures` | `0.2.17` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/cpufeatures-0.2.17/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/cpufeatures-0.2.17/LICENSE-MIT) |
| `cpufeatures` | `0.3.0` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/cpufeatures-0.3.0/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/cpufeatures-0.3.0/LICENSE-MIT) |
| `crypto-common` | `0.1.7` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/crypto-common-0.1.7/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/crypto-common-0.1.7/LICENSE-MIT) |
| `darling` | `0.24.0` | MIT | [LICENSE](third-party-licenses/darling-0.24.0/LICENSE) |
| `darling_core` | `0.24.0` | MIT | [LICENSE](third-party-licenses/darling_core-0.24.0/LICENSE) |
| `darling_macro` | `0.24.0` | MIT | [LICENSE](third-party-licenses/darling_macro-0.24.0/LICENSE) |
| `diff` | `0.1.13` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/diff-0.1.13/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/diff-0.1.13/LICENSE-MIT) |
| `digest` | `0.10.7` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/digest-0.10.7/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/digest-0.10.7/LICENSE-MIT) |
| `displaydoc` | `0.2.7` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/displaydoc-0.2.7/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/displaydoc-0.2.7/LICENSE-MIT) |
| `dunce` | `1.0.5` | CC0-1.0 OR MIT-0 OR Apache-2.0 | [LICENSE](third-party-licenses/dunce-1.0.5/LICENSE) |
| `dyn-clone` | `1.0.20` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/dyn-clone-1.0.20/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/dyn-clone-1.0.20/LICENSE-MIT) |
| `encoding_rs` | `0.8.35` | (Apache-2.0 OR MIT) AND BSD-3-Clause | [COPYRIGHT](third-party-licenses/encoding_rs-0.8.35/COPYRIGHT), [LICENSE-APACHE](third-party-licenses/encoding_rs-0.8.35/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/encoding_rs-0.8.35/LICENSE-MIT), [LICENSE-WHATWG](third-party-licenses/encoding_rs-0.8.35/LICENSE-WHATWG) |
| `equivalent` | `1.0.2` | Apache-2.0 OR MIT | [LICENSE-APACHE](third-party-licenses/equivalent-1.0.2/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/equivalent-1.0.2/LICENSE-MIT) |
| `errno` | `0.3.14` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/errno-0.3.14/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/errno-0.3.14/LICENSE-MIT) |
| `find-msvc-tools` | `0.1.10` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/find-msvc-tools-0.1.10/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/find-msvc-tools-0.1.10/LICENSE-MIT) |
| `fnv` | `1.0.7` | Apache-2.0 / MIT | [LICENSE-APACHE](third-party-licenses/fnv-1.0.7/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/fnv-1.0.7/LICENSE-MIT) |
| `form_urlencoded` | `1.2.2` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/form_urlencoded-1.2.2/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/form_urlencoded-1.2.2/LICENSE-MIT) |
| `fs_extra` | `1.3.0` | MIT | [LICENSE](third-party-licenses/fs_extra-1.3.0/LICENSE) |
| `futures` | `0.3.33` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/futures-0.3.33/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/futures-0.3.33/LICENSE-MIT) |
| `futures-channel` | `0.3.33` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/futures-channel-0.3.33/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/futures-channel-0.3.33/LICENSE-MIT) |
| `futures-core` | `0.3.33` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/futures-core-0.3.33/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/futures-core-0.3.33/LICENSE-MIT) |
| `futures-executor` | `0.3.33` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/futures-executor-0.3.33/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/futures-executor-0.3.33/LICENSE-MIT) |
| `futures-io` | `0.3.33` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/futures-io-0.3.33/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/futures-io-0.3.33/LICENSE-MIT) |
| `futures-macro` | `0.3.33` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/futures-macro-0.3.33/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/futures-macro-0.3.33/LICENSE-MIT) |
| `futures-sink` | `0.3.33` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/futures-sink-0.3.33/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/futures-sink-0.3.33/LICENSE-MIT) |
| `futures-task` | `0.3.33` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/futures-task-0.3.33/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/futures-task-0.3.33/LICENSE-MIT) |
| `futures-util` | `0.3.33` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/futures-util-0.3.33/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/futures-util-0.3.33/LICENSE-MIT) |
| `generic-array` | `0.14.7` | MIT | [LICENSE](third-party-licenses/generic-array-0.14.7/LICENSE) |
| `getrandom` | `0.2.17` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/getrandom-0.2.17/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/getrandom-0.2.17/LICENSE-MIT) |
| `getrandom` | `0.4.3` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/getrandom-0.4.3/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/getrandom-0.4.3/LICENSE-MIT) |
| `h2` | `0.4.15` | MIT | [LICENSE](third-party-licenses/h2-0.4.15/LICENSE) |
| `hashbrown` | `0.17.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/hashbrown-0.17.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/hashbrown-0.17.1/LICENSE-MIT) |
| `http` | `1.5.0` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/http-1.5.0/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/http-1.5.0/LICENSE-MIT) |
| `http-body` | `1.1.0` | MIT | [LICENSE](third-party-licenses/http-body-1.1.0/LICENSE) |
| `http-body-util` | `0.1.4` | MIT | [LICENSE](third-party-licenses/http-body-util-0.1.4/LICENSE) |
| `httparse` | `1.10.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/httparse-1.10.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/httparse-1.10.1/LICENSE-MIT) |
| `httpdate` | `1.0.3` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/httpdate-1.0.3/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/httpdate-1.0.3/LICENSE-MIT) |
| `hyper` | `1.11.0` | MIT | [LICENSE](third-party-licenses/hyper-1.11.0/LICENSE) |
| `hyper-rustls` | `0.27.9` | Apache-2.0 OR ISC OR MIT | [LICENSE-APACHE](third-party-licenses/hyper-rustls-0.27.9/LICENSE-APACHE), [LICENSE-ISC](third-party-licenses/hyper-rustls-0.27.9/LICENSE-ISC), [LICENSE-MIT](third-party-licenses/hyper-rustls-0.27.9/LICENSE-MIT) |
| `hyper-util` | `0.1.20` | MIT | [LICENSE](third-party-licenses/hyper-util-0.1.20/LICENSE) |
| `iana-time-zone` | `0.1.65` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/iana-time-zone-0.1.65/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/iana-time-zone-0.1.65/LICENSE-MIT) |
| `iana-time-zone-haiku` | `0.1.2` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/iana-time-zone-haiku-0.1.2/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/iana-time-zone-haiku-0.1.2/LICENSE-MIT) |
| `icu_collections` | `2.2.0` | Unicode-3.0 | [LICENSE](third-party-licenses/icu_collections-2.2.0/LICENSE) |
| `icu_locale_core` | `2.2.0` | Unicode-3.0 | [LICENSE](third-party-licenses/icu_locale_core-2.2.0/LICENSE) |
| `icu_normalizer` | `2.2.0` | Unicode-3.0 | [LICENSE](third-party-licenses/icu_normalizer-2.2.0/LICENSE) |
| `icu_normalizer_data` | `2.2.0` | Unicode-3.0 | [LICENSE](third-party-licenses/icu_normalizer_data-2.2.0/LICENSE) |
| `icu_properties` | `2.2.0` | Unicode-3.0 | [LICENSE](third-party-licenses/icu_properties-2.2.0/LICENSE) |
| `icu_properties_data` | `2.2.0` | Unicode-3.0 | [LICENSE](third-party-licenses/icu_properties_data-2.2.0/LICENSE) |
| `icu_provider` | `2.2.0` | Unicode-3.0 | [LICENSE](third-party-licenses/icu_provider-2.2.0/LICENSE) |
| `ident_case` | `1.0.1` | MIT/Apache-2.0 | [LICENSE](third-party-licenses/ident_case-1.0.1/LICENSE) |
| `idna` | `1.1.0` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/idna-1.1.0/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/idna-1.1.0/LICENSE-MIT) |
| `idna_adapter` | `1.2.2` | Apache-2.0 OR MIT | [LICENSE-APACHE](third-party-licenses/idna_adapter-1.2.2/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/idna_adapter-1.2.2/LICENSE-MIT) |
| `indexmap` | `2.14.0` | Apache-2.0 OR MIT | [LICENSE-APACHE](third-party-licenses/indexmap-2.14.0/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/indexmap-2.14.0/LICENSE-MIT) |
| `ipnet` | `2.12.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/ipnet-2.12.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/ipnet-2.12.1/LICENSE-MIT) |
| `itoa` | `1.0.18` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/itoa-1.0.18/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/itoa-1.0.18/LICENSE-MIT) |
| `jni` | `0.22.4` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/jni-0.22.4/upstream/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/jni-0.22.4/upstream/LICENSE-MIT) |
| `jni-macros` | `0.22.4` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/jni-macros-0.22.4/upstream/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/jni-macros-0.22.4/upstream/LICENSE-MIT) |
| `jni-sys` | `0.4.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/jni-sys-0.4.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/jni-sys-0.4.1/LICENSE-MIT) |
| `jni-sys-macros` | `0.4.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/jni-sys-macros-0.4.1/upstream/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/jni-sys-macros-0.4.1/upstream/LICENSE-MIT) |
| `jobserver` | `0.1.35` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/jobserver-0.1.35/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/jobserver-0.1.35/LICENSE-MIT) |
| `js-sys` | `0.3.104` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/js-sys-0.3.104/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/js-sys-0.3.104/LICENSE-MIT) |
| `libc` | `0.2.189` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/libc-0.2.189/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/libc-0.2.189/LICENSE-MIT) |
| `litemap` | `0.8.2` | Unicode-3.0 | [LICENSE](third-party-licenses/litemap-0.8.2/LICENSE) |
| `log` | `0.4.33` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/log-0.4.33/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/log-0.4.33/LICENSE-MIT) |
| `lru-slab` | `0.1.2` | MIT OR Apache-2.0 OR Zlib | [LICENSE-APACHE](third-party-licenses/lru-slab-0.1.2/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/lru-slab-0.1.2/LICENSE-MIT), [LICENSE-ZLIB](third-party-licenses/lru-slab-0.1.2/LICENSE-ZLIB) |
| `matchit` | `0.8.4` | MIT AND BSD-3-Clause | [LICENSE](third-party-licenses/matchit-0.8.4/LICENSE), [LICENSE.httprouter](third-party-licenses/matchit-0.8.4/LICENSE.httprouter) |
| `memchr` | `2.8.3` | Unlicense OR MIT | [COPYING](third-party-licenses/memchr-2.8.3/COPYING), [LICENSE-MIT](third-party-licenses/memchr-2.8.3/LICENSE-MIT) |
| `mime` | `0.3.17` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/mime-0.3.17/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/mime-0.3.17/LICENSE-MIT) |
| `mio` | `1.2.2` | MIT | [LICENSE](third-party-licenses/mio-1.2.2/LICENSE) |
| `num-traits` | `0.2.19` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/num-traits-0.2.19/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/num-traits-0.2.19/LICENSE-MIT) |
| `once_cell` | `1.21.4` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/once_cell-1.21.4/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/once_cell-1.21.4/LICENSE-MIT) |
| `openssl-probe` | `0.2.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/openssl-probe-0.2.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/openssl-probe-0.2.1/LICENSE-MIT) |
| `pastey` | `0.2.3` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/pastey-0.2.3/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/pastey-0.2.3/LICENSE-MIT) |
| `percent-encoding` | `2.3.2` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/percent-encoding-2.3.2/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/percent-encoding-2.3.2/LICENSE-MIT) |
| `pin-project-lite` | `0.2.17` | Apache-2.0 OR MIT | [LICENSE-APACHE](third-party-licenses/pin-project-lite-0.2.17/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/pin-project-lite-0.2.17/LICENSE-MIT) |
| `pkg-config` | `0.3.33` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/pkg-config-0.3.33/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/pkg-config-0.3.33/LICENSE-MIT) |
| `potential_utf` | `0.1.5` | Unicode-3.0 | [LICENSE](third-party-licenses/potential_utf-0.1.5/LICENSE) |
| `pretty_assertions` | `1.4.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/pretty_assertions-1.4.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/pretty_assertions-1.4.1/LICENSE-MIT) |
| `proc-macro2` | `1.0.107` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/proc-macro2-1.0.107/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/proc-macro2-1.0.107/LICENSE-MIT) |
| `quinn` | `0.11.11` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/quinn-0.11.11/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/quinn-0.11.11/LICENSE-MIT) |
| `quinn-proto` | `0.11.16` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/quinn-proto-0.11.16/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/quinn-proto-0.11.16/LICENSE-MIT) |
| `quinn-udp` | `0.5.15` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/quinn-udp-0.5.15/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/quinn-udp-0.5.15/LICENSE-MIT) |
| `quote` | `1.0.47` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/quote-1.0.47/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/quote-1.0.47/LICENSE-MIT) |
| `r-efi` | `6.0.0` | MIT OR Apache-2.0 OR LGPL-2.1-or-later | [AUTHORS](third-party-licenses/r-efi-6.0.0/AUTHORS) |
| `rand` | `0.10.2` | MIT OR Apache-2.0 | [COPYRIGHT](third-party-licenses/rand-0.10.2/COPYRIGHT), [LICENSE-APACHE](third-party-licenses/rand-0.10.2/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/rand-0.10.2/LICENSE-MIT) |
| `rand_core` | `0.10.1` | MIT OR Apache-2.0 | [COPYRIGHT](third-party-licenses/rand_core-0.10.1/COPYRIGHT), [LICENSE-APACHE](third-party-licenses/rand_core-0.10.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/rand_core-0.10.1/LICENSE-MIT) |
| `rand_pcg` | `0.10.2` | MIT OR Apache-2.0 | [COPYRIGHT](third-party-licenses/rand_pcg-0.10.2/COPYRIGHT), [LICENSE-APACHE](third-party-licenses/rand_pcg-0.10.2/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/rand_pcg-0.10.2/LICENSE-MIT) |
| `ref-cast` | `1.0.26` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/ref-cast-1.0.26/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/ref-cast-1.0.26/LICENSE-MIT) |
| `ref-cast-impl` | `1.0.26` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/ref-cast-impl-1.0.26/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/ref-cast-impl-1.0.26/LICENSE-MIT) |
| `regex` | `1.13.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/regex-1.13.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/regex-1.13.1/LICENSE-MIT) |
| `regex-automata` | `0.4.18` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/regex-automata-0.4.18/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/regex-automata-0.4.18/LICENSE-MIT) |
| `regex-syntax` | `0.8.11` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/regex-syntax-0.8.11/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/regex-syntax-0.8.11/LICENSE-MIT), [LICENSE-UNICODE](third-party-licenses/regex-syntax-0.8.11/src/unicode_tables/LICENSE-UNICODE) |
| `reqwest` | `0.13.4` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/reqwest-0.13.4/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/reqwest-0.13.4/LICENSE-MIT) |
| `ring` | `0.17.14` | Apache-2.0 AND ISC | [LICENSE](third-party-licenses/ring-0.17.14/LICENSE), [LICENSE-BoringSSL](third-party-licenses/ring-0.17.14/LICENSE-BoringSSL), [LICENSE-other-bits](third-party-licenses/ring-0.17.14/LICENSE-other-bits), [LICENSE-APACHE](third-party-licenses/ring-0.17.14/src/polyfill/once_cell/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/ring-0.17.14/src/polyfill/once_cell/LICENSE-MIT), [LICENSE](third-party-licenses/ring-0.17.14/third_party/fiat/LICENSE) |
| `rmcp` | `3.1.2` | Apache-2.0 | [LICENSE](third-party-licenses/rmcp-3.1.2/upstream/LICENSE) |
| `rmcp-macros` | `3.1.2` | Apache-2.0 | [LICENSE](third-party-licenses/rmcp-macros-3.1.2/upstream/LICENSE) |
| `rustc-hash` | `2.1.3` | Apache-2.0 OR MIT | [LICENSE-APACHE](third-party-licenses/rustc-hash-2.1.3/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/rustc-hash-2.1.3/LICENSE-MIT) |
| `rustc_version` | `0.4.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/rustc_version-0.4.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/rustc_version-0.4.1/LICENSE-MIT) |
| `rustls` | `0.23.43` | Apache-2.0 OR ISC OR MIT | [LICENSE-APACHE](third-party-licenses/rustls-0.23.43/LICENSE-APACHE), [LICENSE-ISC](third-party-licenses/rustls-0.23.43/LICENSE-ISC), [LICENSE-MIT](third-party-licenses/rustls-0.23.43/LICENSE-MIT) |
| `rustls-native-certs` | `0.8.4` | Apache-2.0 OR ISC OR MIT | [LICENSE](third-party-licenses/rustls-native-certs-0.8.4/LICENSE), [LICENSE-APACHE](third-party-licenses/rustls-native-certs-0.8.4/LICENSE-APACHE), [LICENSE-ISC](third-party-licenses/rustls-native-certs-0.8.4/LICENSE-ISC), [LICENSE-MIT](third-party-licenses/rustls-native-certs-0.8.4/LICENSE-MIT) |
| `rustls-pki-types` | `1.15.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/rustls-pki-types-1.15.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/rustls-pki-types-1.15.1/LICENSE-MIT) |
| `rustls-platform-verifier` | `0.7.0` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/rustls-platform-verifier-0.7.0/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/rustls-platform-verifier-0.7.0/LICENSE-MIT) |
| `rustls-platform-verifier-android` | `0.1.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/rustls-platform-verifier-android-0.1.1/upstream/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/rustls-platform-verifier-android-0.1.1/upstream/LICENSE-MIT) |
| `rustls-webpki` | `0.103.13` | ISC | [LICENSE](third-party-licenses/rustls-webpki-0.103.13/LICENSE) |
| `rustversion` | `1.0.23` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/rustversion-1.0.23/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/rustversion-1.0.23/LICENSE-MIT) |
| `ryu` | `1.0.23` | Apache-2.0 OR BSL-1.0 | [LICENSE-APACHE](third-party-licenses/ryu-1.0.23/LICENSE-APACHE), [LICENSE-BOOST](third-party-licenses/ryu-1.0.23/LICENSE-BOOST) |
| `same-file` | `1.0.6` | Unlicense/MIT | [COPYING](third-party-licenses/same-file-1.0.6/COPYING), [LICENSE-MIT](third-party-licenses/same-file-1.0.6/LICENSE-MIT) |
| `schannel` | `0.1.29` | MIT | [LICENSE.md](third-party-licenses/schannel-0.1.29/LICENSE.md) |
| `schemars` | `1.2.2` | MIT | [LICENSE](third-party-licenses/schemars-1.2.2/LICENSE) |
| `schemars_derive` | `1.2.2` | MIT | [LICENSE](third-party-licenses/schemars_derive-1.2.2/LICENSE) |
| `security-framework` | `3.7.0` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/security-framework-3.7.0/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/security-framework-3.7.0/LICENSE-MIT) |
| `security-framework-sys` | `2.17.0` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/security-framework-sys-2.17.0/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/security-framework-sys-2.17.0/LICENSE-MIT) |
| `semver` | `1.0.28` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/semver-1.0.28/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/semver-1.0.28/LICENSE-MIT) |
| `serde` | `1.0.229` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/serde-1.0.229/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/serde-1.0.229/LICENSE-MIT) |
| `serde_core` | `1.0.229` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/serde_core-1.0.229/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/serde_core-1.0.229/LICENSE-MIT) |
| `serde_derive` | `1.0.229` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/serde_derive-1.0.229/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/serde_derive-1.0.229/LICENSE-MIT) |
| `serde_derive_internals` | `0.30.0` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/serde_derive_internals-0.30.0/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/serde_derive_internals-0.30.0/LICENSE-MIT) |
| `serde_json` | `1.0.151` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/serde_json-1.0.151/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/serde_json-1.0.151/LICENSE-MIT) |
| `serde_path_to_error` | `0.1.20` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/serde_path_to_error-0.1.20/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/serde_path_to_error-0.1.20/LICENSE-MIT) |
| `serde_urlencoded` | `0.7.1` | MIT/Apache-2.0 | [LICENSE-APACHE](third-party-licenses/serde_urlencoded-0.7.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/serde_urlencoded-0.7.1/LICENSE-MIT) |
| `sha2` | `0.10.9` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/sha2-0.10.9/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/sha2-0.10.9/LICENSE-MIT) |
| `shlex` | `2.0.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/shlex-2.0.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/shlex-2.0.1/LICENSE-MIT) |
| `signal-hook-registry` | `1.4.8` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/signal-hook-registry-1.4.8/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/signal-hook-registry-1.4.8/LICENSE-MIT) |
| `simd_cesu8` | `1.2.0` | Apache-2.0 OR MIT | [LICENSE-APACHE](third-party-licenses/simd_cesu8-1.2.0/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/simd_cesu8-1.2.0/LICENSE-MIT) |
| `simdutf8` | `0.1.5` | MIT OR Apache-2.0 | [LICENSE-Apache](third-party-licenses/simdutf8-0.1.5/LICENSE-Apache), [LICENSE-MIT](third-party-licenses/simdutf8-0.1.5/LICENSE-MIT) |
| `slab` | `0.4.12` | MIT | [LICENSE](third-party-licenses/slab-0.4.12/LICENSE) |
| `smallvec` | `1.15.2` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/smallvec-1.15.2/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/smallvec-1.15.2/LICENSE-MIT) |
| `socket2` | `0.6.5` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/socket2-0.6.5/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/socket2-0.6.5/LICENSE-MIT) |
| `sse-stream` | `0.2.5` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/sse-stream-0.2.5/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/sse-stream-0.2.5/LICENSE-MIT) |
| `stable_deref_trait` | `1.2.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/stable_deref_trait-1.2.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/stable_deref_trait-1.2.1/LICENSE-MIT) |
| `strsim` | `0.11.1` | MIT | [LICENSE](third-party-licenses/strsim-0.11.1/LICENSE) |
| `subtle` | `2.6.1` | BSD-3-Clause | [LICENSE](third-party-licenses/subtle-2.6.1/LICENSE) |
| `syn` | `2.0.119` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/syn-2.0.119/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/syn-2.0.119/LICENSE-MIT) |
| `syn` | `3.0.3` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/syn-3.0.3/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/syn-3.0.3/LICENSE-MIT) |
| `sync_wrapper` | `1.0.2` | Apache-2.0 | [LICENSE](third-party-licenses/sync_wrapper-1.0.2/LICENSE) |
| `synstructure` | `0.13.2` | MIT | [LICENSE](third-party-licenses/synstructure-0.13.2/LICENSE) |
| `system-configuration` | `0.7.0` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/system-configuration-0.7.0/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/system-configuration-0.7.0/LICENSE-MIT) |
| `system-configuration-sys` | `0.6.0` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/system-configuration-sys-0.6.0/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/system-configuration-sys-0.6.0/LICENSE-MIT) |
| `thiserror` | `2.0.20` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/thiserror-2.0.20/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/thiserror-2.0.20/LICENSE-MIT) |
| `thiserror-impl` | `2.0.20` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/thiserror-impl-2.0.20/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/thiserror-impl-2.0.20/LICENSE-MIT) |
| `tinystr` | `0.8.3` | Unicode-3.0 | [LICENSE](third-party-licenses/tinystr-0.8.3/LICENSE) |
| `tinyvec` | `1.12.0` | Zlib OR Apache-2.0 OR MIT | [LICENSE-APACHE.md](third-party-licenses/tinyvec-1.12.0/LICENSE-APACHE.md), [LICENSE-MIT.md](third-party-licenses/tinyvec-1.12.0/LICENSE-MIT.md), [LICENSE-ZLIB.md](third-party-licenses/tinyvec-1.12.0/LICENSE-ZLIB.md) |
| `tinyvec_macros` | `0.1.1` | MIT OR Apache-2.0 OR Zlib | [LICENSE-APACHE.md](third-party-licenses/tinyvec_macros-0.1.1/LICENSE-APACHE.md), [LICENSE-MIT.md](third-party-licenses/tinyvec_macros-0.1.1/LICENSE-MIT.md), [LICENSE-ZLIB.md](third-party-licenses/tinyvec_macros-0.1.1/LICENSE-ZLIB.md) |
| `tokio` | `1.53.1` | MIT | [LICENSE](third-party-licenses/tokio-1.53.1/LICENSE) |
| `tokio-macros` | `2.7.2` | MIT | [LICENSE](third-party-licenses/tokio-macros-2.7.2/LICENSE) |
| `tokio-rustls` | `0.26.4` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/tokio-rustls-0.26.4/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/tokio-rustls-0.26.4/LICENSE-MIT) |
| `tokio-stream` | `0.1.19` | MIT | [LICENSE](third-party-licenses/tokio-stream-0.1.19/LICENSE) |
| `tokio-util` | `0.7.19` | MIT | [LICENSE](third-party-licenses/tokio-util-0.7.19/LICENSE) |
| `tower` | `0.5.3` | MIT | [LICENSE](third-party-licenses/tower-0.5.3/LICENSE) |
| `tower-http` | `0.6.11` | MIT | [LICENSE](third-party-licenses/tower-http-0.6.11/LICENSE) |
| `tower-layer` | `0.3.3` | MIT | [LICENSE](third-party-licenses/tower-layer-0.3.3/LICENSE) |
| `tower-service` | `0.3.3` | MIT | [LICENSE](third-party-licenses/tower-service-0.3.3/LICENSE) |
| `tracing` | `0.1.44` | MIT | [LICENSE](third-party-licenses/tracing-0.1.44/LICENSE) |
| `tracing-attributes` | `0.1.31` | MIT | [LICENSE](third-party-licenses/tracing-attributes-0.1.31/LICENSE) |
| `tracing-core` | `0.1.36` | MIT | [LICENSE](third-party-licenses/tracing-core-0.1.36/LICENSE), [LICENSE](third-party-licenses/tracing-core-0.1.36/src/spin/LICENSE) |
| `try-lock` | `0.2.5` | MIT | [LICENSE](third-party-licenses/try-lock-0.2.5/LICENSE) |
| `typenum` | `1.20.1` | MIT OR Apache-2.0 | [LICENSE](third-party-licenses/typenum-1.20.1/LICENSE), [LICENSE-APACHE](third-party-licenses/typenum-1.20.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/typenum-1.20.1/LICENSE-MIT) |
| `unicode-ident` | `1.0.24` | (MIT OR Apache-2.0) AND Unicode-3.0 | [LICENSE-APACHE](third-party-licenses/unicode-ident-1.0.24/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/unicode-ident-1.0.24/LICENSE-MIT), [LICENSE-UNICODE](third-party-licenses/unicode-ident-1.0.24/LICENSE-UNICODE) |
| `untrusted` | `0.9.0` | ISC | [LICENSE.txt](third-party-licenses/untrusted-0.9.0/LICENSE.txt) |
| `url` | `2.5.8` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/url-2.5.8/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/url-2.5.8/LICENSE-MIT) |
| `utf8_iter` | `1.0.4` | Apache-2.0 OR MIT | [COPYRIGHT](third-party-licenses/utf8_iter-1.0.4/COPYRIGHT), [LICENSE-APACHE](third-party-licenses/utf8_iter-1.0.4/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/utf8_iter-1.0.4/LICENSE-MIT) |
| `uuid` | `1.24.0` | Apache-2.0 OR MIT | [LICENSE-APACHE](third-party-licenses/uuid-1.24.0/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/uuid-1.24.0/LICENSE-MIT) |
| `version_check` | `0.9.5` | MIT/Apache-2.0 | [LICENSE-APACHE](third-party-licenses/version_check-0.9.5/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/version_check-0.9.5/LICENSE-MIT) |
| `walkdir` | `2.5.0` | Unlicense/MIT | [COPYING](third-party-licenses/walkdir-2.5.0/COPYING), [LICENSE-MIT](third-party-licenses/walkdir-2.5.0/LICENSE-MIT) |
| `want` | `0.3.1` | MIT | [LICENSE](third-party-licenses/want-0.3.1/LICENSE) |
| `wasi` | `0.11.1+wasi-snapshot-preview1` | Apache-2.0 WITH LLVM-exception OR Apache-2.0 OR MIT | [LICENSE-APACHE](third-party-licenses/wasi-0.11.1+wasi-snapshot-preview1/LICENSE-APACHE), [LICENSE-Apache-2.0_WITH_LLVM-exception](third-party-licenses/wasi-0.11.1+wasi-snapshot-preview1/LICENSE-Apache-2.0_WITH_LLVM-exception), [LICENSE-MIT](third-party-licenses/wasi-0.11.1+wasi-snapshot-preview1/LICENSE-MIT) |
| `wasm-bindgen` | `0.2.127` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/wasm-bindgen-0.2.127/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/wasm-bindgen-0.2.127/LICENSE-MIT) |
| `wasm-bindgen-futures` | `0.4.77` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/wasm-bindgen-futures-0.4.77/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/wasm-bindgen-futures-0.4.77/LICENSE-MIT) |
| `wasm-bindgen-macro` | `0.2.127` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/wasm-bindgen-macro-0.2.127/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/wasm-bindgen-macro-0.2.127/LICENSE-MIT) |
| `wasm-bindgen-macro-support` | `0.2.127` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/wasm-bindgen-macro-support-0.2.127/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/wasm-bindgen-macro-support-0.2.127/LICENSE-MIT) |
| `wasm-bindgen-shared` | `0.2.127` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/wasm-bindgen-shared-0.2.127/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/wasm-bindgen-shared-0.2.127/LICENSE-MIT) |
| `wasm-streams` | `0.5.0` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/wasm-streams-0.5.0/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/wasm-streams-0.5.0/LICENSE-MIT) |
| `web-sys` | `0.3.104` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/web-sys-0.3.104/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/web-sys-0.3.104/LICENSE-MIT) |
| `web-time` | `1.1.0` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/web-time-1.1.0/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/web-time-1.1.0/LICENSE-MIT) |
| `webpki-root-certs` | `1.0.9` | CDLA-Permissive-2.0 | [LICENSE](third-party-licenses/webpki-root-certs-1.0.9/LICENSE) |
| `winapi-util` | `0.1.11` | Unlicense OR MIT | [COPYING](third-party-licenses/winapi-util-0.1.11/COPYING), [LICENSE-MIT](third-party-licenses/winapi-util-0.1.11/LICENSE-MIT) |
| `windows-core` | `0.62.2` | MIT OR Apache-2.0 | [license-apache-2.0](third-party-licenses/windows-core-0.62.2/license-apache-2.0), [license-mit](third-party-licenses/windows-core-0.62.2/license-mit) |
| `windows-implement` | `0.60.2` | MIT OR Apache-2.0 | [license-apache-2.0](third-party-licenses/windows-implement-0.60.2/license-apache-2.0), [license-mit](third-party-licenses/windows-implement-0.60.2/license-mit) |
| `windows-interface` | `0.59.3` | MIT OR Apache-2.0 | [license-apache-2.0](third-party-licenses/windows-interface-0.59.3/license-apache-2.0), [license-mit](third-party-licenses/windows-interface-0.59.3/license-mit) |
| `windows-link` | `0.2.1` | MIT OR Apache-2.0 | [license-apache-2.0](third-party-licenses/windows-link-0.2.1/license-apache-2.0), [license-mit](third-party-licenses/windows-link-0.2.1/license-mit) |
| `windows-registry` | `0.6.1` | MIT OR Apache-2.0 | [license-apache-2.0](third-party-licenses/windows-registry-0.6.1/license-apache-2.0), [license-mit](third-party-licenses/windows-registry-0.6.1/license-mit) |
| `windows-result` | `0.4.1` | MIT OR Apache-2.0 | [license-apache-2.0](third-party-licenses/windows-result-0.4.1/license-apache-2.0), [license-mit](third-party-licenses/windows-result-0.4.1/license-mit) |
| `windows-strings` | `0.5.1` | MIT OR Apache-2.0 | [license-apache-2.0](third-party-licenses/windows-strings-0.5.1/license-apache-2.0), [license-mit](third-party-licenses/windows-strings-0.5.1/license-mit) |
| `windows-sys` | `0.52.0` | MIT OR Apache-2.0 | [license-apache-2.0](third-party-licenses/windows-sys-0.52.0/license-apache-2.0), [license-mit](third-party-licenses/windows-sys-0.52.0/license-mit) |
| `windows-sys` | `0.61.2` | MIT OR Apache-2.0 | [license-apache-2.0](third-party-licenses/windows-sys-0.61.2/license-apache-2.0), [license-mit](third-party-licenses/windows-sys-0.61.2/license-mit) |
| `windows-targets` | `0.52.6` | MIT OR Apache-2.0 | [license-apache-2.0](third-party-licenses/windows-targets-0.52.6/license-apache-2.0), [license-mit](third-party-licenses/windows-targets-0.52.6/license-mit) |
| `windows_aarch64_gnullvm` | `0.52.6` | MIT OR Apache-2.0 | [license-apache-2.0](third-party-licenses/windows_aarch64_gnullvm-0.52.6/license-apache-2.0), [license-mit](third-party-licenses/windows_aarch64_gnullvm-0.52.6/license-mit) |
| `windows_aarch64_msvc` | `0.52.6` | MIT OR Apache-2.0 | [license-apache-2.0](third-party-licenses/windows_aarch64_msvc-0.52.6/license-apache-2.0), [license-mit](third-party-licenses/windows_aarch64_msvc-0.52.6/license-mit) |
| `windows_i686_gnu` | `0.52.6` | MIT OR Apache-2.0 | [license-apache-2.0](third-party-licenses/windows_i686_gnu-0.52.6/license-apache-2.0), [license-mit](third-party-licenses/windows_i686_gnu-0.52.6/license-mit) |
| `windows_i686_gnullvm` | `0.52.6` | MIT OR Apache-2.0 | [license-apache-2.0](third-party-licenses/windows_i686_gnullvm-0.52.6/license-apache-2.0), [license-mit](third-party-licenses/windows_i686_gnullvm-0.52.6/license-mit) |
| `windows_i686_msvc` | `0.52.6` | MIT OR Apache-2.0 | [license-apache-2.0](third-party-licenses/windows_i686_msvc-0.52.6/license-apache-2.0), [license-mit](third-party-licenses/windows_i686_msvc-0.52.6/license-mit) |
| `windows_x86_64_gnu` | `0.52.6` | MIT OR Apache-2.0 | [license-apache-2.0](third-party-licenses/windows_x86_64_gnu-0.52.6/license-apache-2.0), [license-mit](third-party-licenses/windows_x86_64_gnu-0.52.6/license-mit) |
| `windows_x86_64_gnullvm` | `0.52.6` | MIT OR Apache-2.0 | [license-apache-2.0](third-party-licenses/windows_x86_64_gnullvm-0.52.6/license-apache-2.0), [license-mit](third-party-licenses/windows_x86_64_gnullvm-0.52.6/license-mit) |
| `windows_x86_64_msvc` | `0.52.6` | MIT OR Apache-2.0 | [license-apache-2.0](third-party-licenses/windows_x86_64_msvc-0.52.6/license-apache-2.0), [license-mit](third-party-licenses/windows_x86_64_msvc-0.52.6/license-mit) |
| `writeable` | `0.6.3` | Unicode-3.0 | [LICENSE](third-party-licenses/writeable-0.6.3/LICENSE) |
| `yansi` | `1.0.1` | MIT OR Apache-2.0 | [LICENSE-APACHE](third-party-licenses/yansi-1.0.1/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/yansi-1.0.1/LICENSE-MIT) |
| `yoke` | `0.8.3` | Unicode-3.0 | [LICENSE](third-party-licenses/yoke-0.8.3/LICENSE) |
| `yoke-derive` | `0.8.2` | Unicode-3.0 | [LICENSE](third-party-licenses/yoke-derive-0.8.2/LICENSE) |
| `zerofrom` | `0.1.8` | Unicode-3.0 | [LICENSE](third-party-licenses/zerofrom-0.1.8/LICENSE) |
| `zerofrom-derive` | `0.1.7` | Unicode-3.0 | [LICENSE](third-party-licenses/zerofrom-derive-0.1.7/LICENSE) |
| `zeroize` | `1.9.0` | Apache-2.0 OR MIT | [LICENSE-APACHE](third-party-licenses/zeroize-1.9.0/LICENSE-APACHE), [LICENSE-MIT](third-party-licenses/zeroize-1.9.0/LICENSE-MIT) |
| `zerotrie` | `0.2.4` | Unicode-3.0 | [LICENSE](third-party-licenses/zerotrie-0.2.4/LICENSE) |
| `zerovec` | `0.11.6` | Unicode-3.0 | [LICENSE](third-party-licenses/zerovec-0.11.6/LICENSE) |
| `zerovec-derive` | `0.11.3` | Unicode-3.0 | [LICENSE](third-party-licenses/zerovec-derive-0.11.3/LICENSE) |
| `zmij` | `1.0.23` | MIT | [LICENSE-MIT](third-party-licenses/zmij-1.0.23/LICENSE-MIT) |
