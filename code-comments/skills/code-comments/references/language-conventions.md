# Language conventions

Checked against primary documentation on 2026-10-02. Follow the repository's
established documentation tool and supported version. These are conventions,
not empirical evidence that a particular format improves comprehension. Read
only the relevant section; check current official docs when a tag or behavior
is uncertain. Other languages use the same evidence-first workflow with their
own local conventions.

## Go

[Go Doc Comments](https://go.dev/doc/comment): place doc comments directly before
the declaration. Give a package one useful package introduction, rather than
duplicating it in each file. Document exported declarations using sentences
that name the symbol. Explain meaningful zero values, units, error behavior,
ownership, and concurrency guarantees when relevant. Keep unexported comments
selective. Use Go documentation links and examples in the repository's style;
run `gofmt` and relevant existing checks. Preserve `//go:` and build directives.

This carries forward Gommenter's focus on accurate contracts and local rationale.

## Python

[PEP 257](https://peps.python.org/pep-0257/): use docstrings for public modules,
classes, and functions as local practice requires. Start with a concise summary;
add details needed to use the API. Match the existing Sphinx, Google, NumPy, or
other format rather than switching styles. Document behavior and meaningful
exceptions without reproducing the signature. A docstring becomes `__doc__`;
changing it may affect introspection, snapshots, or executable doctest examples.
Run relevant existing checks and doctests if affected. Preserve encoding,
type-check, lint, and formatter directives.

## JavaScript and TypeScript

Use the existing JSDoc or TSDoc toolchain. In typed code, avoid duplicating types
unless the documentation generator requires it; explain semantic constraints
instead. [TSDoc's `@remarks`](https://tsdoc.org/pages/tags/remarks/) separates a
brief summary from deeper API detail. Use supported tags and actual parameters,
return values, errors, and examples. Preserve lint directives, bundler purity
annotations, source-map comments, and type-check pragmas. Check with the
repository's type checker, linter, and doc build when relevant.

## Rust

Use the repository's rustdoc conventions, including `///` for items and `//!`
for containing modules. Explain meaningful ownership, error, panic, and safety
requirements from evidence. [Rustdoc documentation
tests](https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html)
may execute code blocks; run the affected existing documentation tests. Do not
mark examples `ignore` or weaken their assertions to obtain a pass.

## Java

[Oracle's Javadoc guide](https://www.oracle.com/technical-resources/articles/java/javadoc-tool.html)
describes API documentation as a caller-facing contract. Describe meaningful
parameters, results, exceptions, and limits; check `@param`, `@return`,
`@throws`, and links against the declaration and implementation. Match the
project's supported Javadoc version; the guide's age does not establish support
for newer tags. Use the existing Javadoc/doclint checks where configured.

## C#

[C# XML documentation
tags](https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/recommended-tags):
use valid XML and accurate `summary`, `param`, `returns`, `exception`, and
`remarks` information where applicable. Check references and names with the
existing compiler/doc generator. Describe semantic requirements rather than
filling tags with repeated names.

## C, C++, shell, SQL, and configuration

Use the existing local documentation format, such as Doxygen when already
configured. Comment ownership, lifetime, units, error signals, and relevant
operational assumptions. Preserve preprocessor-related markers, interpreter
lines, shell/lint directives, SQL hints, and configuration directives. Inspect
the actual parser or tool before treating comment-looking text as inert.
Do not adopt a documentation tool or add dependencies for a comment task.
