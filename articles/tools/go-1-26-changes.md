# Go 1.26: Key Changes and Features

**Date:** July 6, 2026

Go 1.26 was released on **February 10, 2026**, bringing significant updates to the language, compiler, runtime, and standard library. This article outlines the major changes introduced in this release.

## Language Changes

*   **Updated `new` Function:** The built-in `new` function has been updated to support expressions, allowing you to specify an initial value (e.g., `p := new(42)`).

## Garbage Collector & Runtime

*   **"Green Tea" Garbage Collector:** The release introduced the new "Green Tea" Garbage Collector.
*   **Reduced cgo Overhead:** Improvements to reduce cgo overhead, leading to better performance in many applications.

## Standard Library Additions

Three new packages were added to the standard library:
*   `crypto/hpke`
*   `crypto/mlkem/mlkemtest`
*   `testing/cryptotest`

## Experimental Features

*   **Architecture-Specific SIMD:** A new experimental `simd/archsimd` package was introduced. It can be enabled via `GOEXPERIMENT=simd` to access architecture-specific SIMD operations.

## Tooling & Optimizations

*   **`go fix` Tool Improvements:** Various enhancements made to the `go fix` tool.
*   **Performance Optimizations:** Applied to `fmt.Errorf` and `io.ReadAll`.

## Maintenance Releases

Following the initial release, several minor point releases have been issued to address security and bug fixes:
*   **Go 1.26.1 (March 2026):** Included security fixes for `crypto/x509` and other components.
*   **Go 1.26.2 (April 2026):** Included additional security and bug fixes.
*   **Go 1.26.4 (June 2026):** One of the latest supported minor versions.

## References

*   [Official Go 1.26 Release Notes](https://go.dev/doc/go1.26)
