# OpenAPI Specification v3.2.0: Highlights and Changes

**Source:** [OpenAPI Initiative](https://www.openapis.org/)
**Date:** January 24, 2026

## Summary

OpenAPI Specification (OAS) v3.2.0 introduces significant enhancements to modern API description, focusing on better support for streaming data, complex organizational needs, and accurate HTTP method modeling. This release builds upon v3.1 to address the evolving landscape of AI, IoT, and large-scale API ecosystems.

## Key Features & Improvements

### 1. Advanced Tagging & Organization
One of the most requested features, **Multipurpose Tags**, now supports:
-   **Nesting:** Tags can now have a `parent` field, allowing for hierarchical organization.
-   **Classification:** A `kind` field enables taxonomy creation.
-   **Summaries:** Short descriptions for quick scanning.

This allows for much more sophisticated grouping of operations in generated documentation and SDKs.

### 2. Streaming Data Support
Acknowledging the rise of real-time applications (Chat, AI, IoT), v3.2.0 adds robust support for streaming media types:
-   Native support for `text/event-stream` (Server-Sent Events), `application/jsonl`, and `application/json-seq`.
-   **`itemSchema` Keyword:** Explicitly describes the type of individual elements within a stream, removing ambiguity.

### 3. Enhanced HTTP Methods
-   **QUERY Method:** Built-in support for the `QUERY` HTTP method, allowing for safe, idempotent complex queries with a request body (distinct from `POST`).
-   **`additionalOperations`:** A formalized mechanism to document non-standard HTTP verbs (e.g., `LINK`, `UNLINK`) without breaking validation.

### 4. Security Updates
-   **Device Flow:** Official support for the OAuth 2.0 Device Authorization Flow, crucial for inputs-constrained devices like Smart TVs.
-   Updated metadata fields for OAuth 2 servers.

### 5. Precision & Clarity
-   **Path Templating:** Now formally defined using **ABNF**, ensuring consistency in how tools parse paths like `/users/{id}`.
-   **Example Objects:** New distinction between `dataValue` (structured data) and `serializedValue` (wire format), essential for complex encodings.
-   **XML Support:** Refined with `nodeType` fields for explicit mapping, deprecating some older, ambiguous attributes.

## Conclusion

OpenAPI v3.2.0 represents a mature step forward, addressing specific pain points in API design while embracing modern patterns like streaming and complex querying. It provides tool builders and API designers with the precision needed for the next generation of interoperable software.
