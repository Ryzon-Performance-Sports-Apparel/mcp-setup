import { ProxyOAuthServerProvider } from "@modelcontextprotocol/sdk/server/auth/providers/proxyProvider.js";
import { OAuthClientInformationFull } from "@modelcontextprotocol/sdk/shared/auth.js";
import { AuthInfo } from "@modelcontextprotocol/sdk/server/auth/types.js";

const GOOGLE_CLIENT_ID = process.env.OAUTH_CLIENT_ID!;
const GOOGLE_CLIENT_SECRET = process.env.OAUTH_CLIENT_SECRET!;
const ALLOWED_DOMAIN = process.env.OAUTH_ALLOWED_DOMAIN || "ryzon.net";

export function createGoogleOAuthProvider() {
  const provider = new ProxyOAuthServerProvider({
    endpoints: {
      authorizationUrl: "https://accounts.google.com/o/oauth2/v2/auth",
      tokenUrl: "https://oauth2.googleapis.com/token",
      revocationUrl: "https://oauth2.googleapis.com/revoke",
    },

    getClient: async (clientId: string) => {
      if (clientId !== GOOGLE_CLIENT_ID) return undefined;

      return {
        client_id: GOOGLE_CLIENT_ID,
        client_secret: GOOGLE_CLIENT_SECRET,
        client_id_issued_at: 0,
        redirect_uris: [
          "https://claude.ai/api/mcp/auth_callback",
          "https://claude.com/api/mcp/auth_callback",
        ],
        grant_types: ["authorization_code", "refresh_token"],
        response_types: ["code"],
        token_endpoint_auth_method: "client_secret_post",
        scope: "openid email",
      } as OAuthClientInformationFull;
    },

    verifyAccessToken: async (token: string): Promise<AuthInfo> => {
      const res = await fetch(
        `https://oauth2.googleapis.com/tokeninfo?access_token=${token}`
      );

      if (!res.ok) {
        const body = await res.text();
        console.error("Google tokeninfo failed:", res.status, body);
        throw new Error("Invalid or expired Google access token");
      }

      const info = (await res.json()) as Record<string, string>;

      if (info.aud !== GOOGLE_CLIENT_ID) {
        console.error(`aud mismatch: got ${info.aud}, expected ${GOOGLE_CLIENT_ID}`);
        throw new Error("Token was not issued for this application");
      }

      const emailDomain = info.email?.split("@")[1];
      if (!emailDomain || emailDomain !== ALLOWED_DOMAIN) {
        console.error(`domain rejected: ${emailDomain || "no email in token"}`);
        throw new Error(`Access restricted to @${ALLOWED_DOMAIN} accounts`);
      }

      console.log(`Verified token for ${info.email}`);

      return {
        token,
        clientId: GOOGLE_CLIENT_ID,
        scopes: ["openid", "email"],
        expiresAt: Math.floor(Date.now() / 1000) + parseInt(info.expires_in || "3600", 10),
        extra: {
          email: info.email,
        },
      };
    },
  });

  const originalAuthorize = provider.authorize.bind(provider);
  provider.authorize = async (client, params, res) => {
    params.scopes = ["openid", "email"];
    return originalAuthorize(client, params, res);
  };

  return provider;
}
