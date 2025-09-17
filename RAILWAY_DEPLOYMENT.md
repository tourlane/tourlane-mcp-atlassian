# Railway Deployment Guide

This guide explains how to deploy the MCP Atlassian server to Railway.

## Quick Deployment Steps

1. **Connect your GitHub repository to Railway**
   - Go to [Railway](https://railway.app)
   - Click "Start a New Project" → "Deploy from GitHub repo"
   - Select this repository

2. **Railway will automatically detect the Dockerfile and deploy**
   - The `railway.toml` file configures the deployment
   - The `Dockerfile` includes all necessary setup

## Environment Variables

### Required Environment Variables (Set in Railway Dashboard)

#### Transport Configuration (Already set by default)
- `TRANSPORT=sse` (Server-Sent Events transport)
- `HOST=0.0.0.0` (Listen on all interfaces)  
- `PORT=8000` (Railway will override this automatically)

#### Atlassian Configuration (You need to add these)
For Jira integration:
```
JIRA_URL=https://your-domain.atlassian.net
JIRA_USERNAME=your-email@domain.com
JIRA_API_TOKEN=your-api-token
```

For Confluence integration:
```
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_USERNAME=your-email@domain.com
CONFLUENCE_API_TOKEN=your-api-token
```

#### OAuth Configuration (Optional - for enhanced security)
```
ATLASSIAN_OAUTH_ENABLE=true
ATLASSIAN_OAUTH_CLIENT_ID=your-oauth-client-id
ATLASSIAN_OAUTH_CLIENT_SECRET=your-oauth-client-secret
```

### How to Set Environment Variables in Railway

1. Go to your Railway project dashboard
2. Click on your service
3. Go to the "Variables" tab
4. Click "New Variable" and add each environment variable
5. Redeploy the service after adding variables

## Health Check

Once deployed, Railway will provide a URL like `https://your-app-name.railway.app`

Test the deployment:
- Health check: `https://your-app-name.railway.app/healthz`
- MCP SSE endpoint: `https://your-app-name.railway.app/sse`

## Troubleshooting

### Build Issues
- Check the "Deployments" tab in Railway for build logs
- Ensure all required files are committed to your repository

### Runtime Issues  
- Check the "Logs" tab in Railway for runtime errors
- Verify environment variables are set correctly
- Ensure Atlassian credentials are valid

### Port Issues
- Railway automatically assigns and maps ports
- The `EXPOSE 8000` in Dockerfile tells Railway which port to use
- Don't hardcode ports in your application - use the `PORT` environment variable

## Security Notes

- Never commit API tokens or secrets to your repository
- Use Railway's environment variables for all sensitive configuration
- Consider using OAuth for production deployments
- The server runs as a non-root user for security

## Local Testing

To test the same configuration locally:
```bash
docker build -t mcp-atlassian .
docker run -p 8000:8000 -e TRANSPORT=sse -e JIRA_URL=your-url mcp-atlassian
```