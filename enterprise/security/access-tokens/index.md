# Organization access tokens





  
  
  
  


  <div
    class="not-prose summary-bar"
  >
    
      <div class="flex flex-wrap gap-1">
        <span class="font-bold">Subscription:</span>
        
          <span>Team</span>
          <span class="icon-svg">
            
            
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M30-240q-12.75 0-21.37-8.63Q0-257.25 0-270v-23q0-38.57 41.5-62.78Q83-380 150.38-380q12.16 0 23.39.5t22.23 2.15q-8 17.35-12 35.17-4 17.81-4 37.18v65H30Zm240 0q-12.75 0-21.37-8.63Q240-257.25 240-270v-35q0-32 17.5-58.5T307-410q32-20 76.5-30t96.5-10q53 0 97.5 10t76.5 30q32 20 49 46.5t17 58.5v35q0 12.75-8.62 21.37Q702.75-240 690-240H270Zm510 0v-65q0-19.86-3.5-37.43T765-377.27q11-1.73 22.17-2.23 11.17-.5 22.83-.5 67.5 0 108.75 23.77T960-293v23q0 12.75-8.62 21.37Q942.75-240 930-240H780ZM149.57-410q-28.57 0-49.07-20.56Q80-451.13 80-480q0-29 20.56-49.5Q121.13-550 150-550q29 0 49.5 20.5t20.5 49.93q0 28.57-20.5 49.07T149.57-410Zm660 0q-28.57 0-49.07-20.56Q740-451.13 740-480q0-29 20.56-49.5Q781.13-550 810-550q29 0 49.5 20.5t20.5 49.93q0 28.57-20.5 49.07T809.57-410ZM480-480q-50 0-85-35t-35-85q0-51 35-85.5t85-34.5q51 0 85.5 34.5T600-600q0 50-34.5 85T480-480Z"/></svg>
            
          </span>
        
          <span>Business</span>
          <span class="icon-svg">
            
            
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 -960 960 960"><path d="M80-180v-600q0-24.75 17.63-42.38Q115.25-840 140-840h270q24.75 0 42.38 17.62Q470-804.75 470-780v105h350q24.75 0 42.38 17.62Q880-639.75 880-615v435q0 24.75-17.62 42.37Q844.75-120 820-120H140q-24.75 0-42.37-17.63Q80-155.25 80-180Zm60 0h105v-105H140v105Zm0-165h105v-105H140v105Zm0-165h105v-105H140v105Zm0-165h105v-105H140v105Zm165 495h105v-105H305v105Zm0-165h105v-105H305v105Zm0-165h105v-105H305v105Zm0-165h105v-105H305v105Zm165 495h350v-435H470v105h80v60h-80v105h80v60h-80v105Zm185-270v-60h60v60h-60Zm0 165v-60h60v60h-60Z"/></svg>
            
          </span>
        
      </div>
    

    

    

    
  </div>



Organization access tokens (OATs) provide secure, programmatic access to Docker Hub for automated systems, CI/CD pipelines, and other business-critical tasks. Unlike personal access tokens tied to individual users, OATs are associated with your organization and can be managed by any organization owner.

> [!WARNING]
>
> Organization access tokens are incompatible with Docker Desktop, Image Access Management, and Registry Access Management. If you use these features, use [personal access tokens](/manuals/security/access-tokens.md) instead.

## Who should use organization access tokens?

Use OATs for automated systems that need Docker Hub access without depending on individual user accounts:

- CI/CD pipelines: Build and deployment systems that push and pull images
- Production systems: Applications that pull images during deployment
- Monitoring tools: Systems that need to check repository status or pull images
- Backup systems: Tools that periodically pull images for archival
- Integration services: Third-party tools that integrate with your Docker Hub repositories

## Key benefits

Benefits of using organization access tokens include:

- Organizational ownership: Not tied to individual users who might leave the company
- Shared management: All organization owners can create and manage OATs
- Separate usage limits: OATs have their own Docker Hub rate limits, not counting against personal accounts
- Better security audit: Track when tokens were last used and identify suspicious activity
- Granular permissions: Limit access to specific repositories and operations

## Prerequisites

To create and use organization access tokens, you must have:

- A Docker Team or Business subscription
- Owner permissions
- Repositories you want to grant access to

## Create an organization access token

Owners can create tokens with these limits:

- Team subscription: Up to 10 OATs per organization
- Business subscription: Up to 100 OATs per organization

Expired tokens count toward your total limit.

To create an OAT:

1. Sign in to [Docker Home](https://app.docker.com/) and select your
organization.
1. Select **Admin Console**, then **Access tokens**.
1. Select **Generate access token**.
1. Configure token details:
    - Label: Descriptive name indicating the token's purpose
    - Description (optional): Additional details
    - Expiration date: When the token should expire
1. Expand the **Repository** drop-down to set access permissions:
    1. Optional. Select **Read public repositories** for access to public repositories.
    1. Select **Add repository** and choose a repository from the drop-down.
    1. Set permissions for each repository: **Image Pull** or **Image Push**.
    1. Add up to 50 repositories as needed.
1. Optional. Configure organization management permissions by expanding the **Organization** drop-down and selecting the **Allow management access to this organization's resources**:
    - **Member Edit**: Edit members of the organization
    - **Member Read**: Read members of the organization
    - **Invite Edit**: Invite members to the organization
    - **Invite Read**: Read invites to the organization
    - **Group Edit**: Edit groups of the organization
    - **Group Read**: Read groups of the organization
1. Select **Generate token**. Copy the token that appears on the screen and save it. You won't be able to retrieve the token once you exit the screen.

> [!IMPORTANT]
>
> Treat organization access tokens like passwords. Store them securely in a credential manager and never commit them to source code repositories.

## Use organization access tokens

Sign in to the Docker CLI using your organization access token:

```console
$ docker login --username <YOUR_ORGANIZATION_NAME>
Password: [paste your OAT here]
```

When prompted for a password, enter your organization access token.

## Modify existing tokens

To manage existing tokens:

1. Sign in to [Docker Home](https://app.docker.com/) and select your
organization.
1. Select **Admin Console**, then **Access tokens**.
1. Select the actions menu in the token row, you can:
    - **Edit**
    - **Deactivate**
    - **Delete**
1. Select **Save** after making changes to a token.

## Migrate from service accounts

[Enhanced Service Account add-ons](/manuals/docker-hub/service-accounts.md)
are deprecated and no longer available for
new purchases as of December 10, 2024.

Organization access tokens provide a
modern, secure replacement with additional benefits:

| Feature | Service accounts | Organization access tokens |
|---------|------------------|----------------------------|
| Authentication | Username/password | Organization name + token |
| Cost | Tiered add-on pricing | Included with subscription |
| Management | Individual account-based | Organization owner managed |
| Repository access | Full account access | Granular repository permissions |
| Security | Basic password auth | Token-based with expiration |
| Rate limits | Separate tiered limits | Organization subscription limits |

### Migration steps

To migrate from service accounts to OATs, use the following steps:

1. Document current service accounts and their purposes.
1. Generate organization access tokens with appropriate repository permissions.
1. Replace service account credentials in your systems.
1. Validate all automated workflows work correctly.
1. Remove deprecated service account credentials.

## Organization access token best practices

- Regular token rotation: Set reasonable expiration dates and rotate tokens regularly to minimize security risks.
- Principle of least privilege: Grant only the minimum repository access and permissions needed for each use case.
- Monitor token usage: Regularly review when tokens were last used to identify unused or suspicious tokens.
- Secure storage: Store tokens in secure credential management systems, never in plain text or source code.
- Immediate revocation: Deactivate or delete tokens immediately if they're compromised or no longer needed.
