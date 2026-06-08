# Understanding OAuth 2.0

**Date:** June 08, 2026

## Overview

OAuth 2.0 is an authorization framework that allows a client (app) to obtain limited access (tokens) to a resource server on behalf of a resource owner (user). This is achieved using an authorization server to issue tokens. <citation src="1,2"></citation>

## Key Actors

- **Resource Owner:** The user.
- **Client:** The application requesting access.
- **Authorization Server:** Issues authorization grants and tokens.
- **Resource Server:** Hosts protected APIs and accepts access tokens. <citation src="1"></citation>

## Core Concepts

- **Authorization Grant:** A credential representing the resource owner’s permission (there are several grant types).
- **Access Token:** A short-lived credential the client presents to the resource server (usually a bearer token).
- **Refresh Token:** A long-lived token used to obtain new access tokens without user interaction. <citation src="1,2"></citation>

## Main Grant Types (Flows)

- **Authorization Code** (recommended for web & native apps): Involves a browser-based redirect to the auth server, yielding an authorization code, followed by a server-side token exchange. This is safe because tokens travel server-to-server. Use with PKCE for public clients. <citation src="1,2,5"></citation>
- **Authorization Code + PKCE:** Adds a `code_challenge` and `code_verifier` to prevent code interception. This is required for many clients under modern best practices. <citation src="2,5"></citation>
- **Client Credentials** (machine-to-machine): The client authenticates with its own credentials to get tokens for its own resources (no user involved). <citation src="1,5"></citation>
- **Device Code:** Used for devices without browsers or with limited input, where the user completes authorization on another device. <citation src="2"></citation>
- **Refresh Token Grant:** Exchanges a refresh token for a new access token when the current access token expires. <citation src="1"></citation>

### Deprecated Flows

- **Implicit:** Tokens are returned in URL fragments.
- **Resource Owner Password Credentials:** The client collects the user's password directly.

Both are discouraged and removed in OAuth 2.1 due to security risks. <citation src="1,5"></citation>

## Security Considerations & Best Practices

- Always use TLS.
- Prefer Authorization Code + PKCE for apps that cannot keep secrets.
- Use short-lived access tokens and rotate refresh tokens (or use sender-constrained tokens).
- Perform exact `redirect_uri` matching and validate the `state` parameter to prevent CSRF.
- Never place bearer tokens in URLs (e.g., as a query string parameter). <citation src="1,5,2"></citation>

## Typical HTTP Examples

### Authorization Request (Browser Redirect)
`GET /authorize?response_type=code&client_id=...&redirect_uri=...&scope=...&state=...` <citation src="1"></citation>

### Token Exchange (Server POST)
`POST /token grant_type=authorization_code&code=...&redirect_uri=...`
(The client authenticates) → Returns `access_token`, `token_type`, `expires_in`, and optionally `refresh_token`. <citation src="1"></citation>

## Implementation Resources

Use RFC 6749 for the protocol details, `oauth.net` for practical guidance and extensions (like PKCE, device flow, and OAuth 2.1 updates), and adhere to current security BCPs (Best Current Practices) when implementing. <citation src="1,2,5"></citation>

## References

1. RFC 6749
2. oauth.net
5. Modern Security BCPs
