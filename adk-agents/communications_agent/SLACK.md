
## Slack Bot

The communications_agent currently uses a Slack Bot (configured [here](https://api.slack.com/apps/A094FCEKSV7/app-home)) to send private messages to users in the Slack workspace qaware-test.slack.com

It has the following manifest:

```
{
    "display_information": {
        "name": "PaaL Comms Agent",
        "description": "A small demo agent to send mock insurance offers to users",
        "background_color": "#662966"
    },
    "features": {
        "bot_user": {
            "display_name": "Paal Test",
            "always_online": false
        }
    },
    "oauth_config": {
        "scopes": {
            "bot": [
                "chat:write",
                "im:read",
                "users:read"
            ]
        }
    },
    "settings": {
        "org_deploy_enabled": false,
        "socket_mode_enabled": false,
        "token_rotation_enabled": false
    }
}
```