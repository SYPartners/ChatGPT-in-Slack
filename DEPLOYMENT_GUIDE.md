# ChatGPT in Slack - SYPartners Internal Documentation

## Table of Contents
1. [Overview](#overview)
2. [What is ChatGPT in Slack?](#what-is-chatgpt-in-slack)
3. [How Users Interact with the Bot](#how-users-interact-with-the-bot)
4. [Our Infrastructure](#our-infrastructure)
5. [Admin Access & Management](#admin-access--management)
6. [Configuration & Environment Variables](#configuration--environment-variables)
7. [Features & Capabilities](#features--capabilities)
8. [Maintenance & Troubleshooting](#maintenance--troubleshooting)
9. [Security & Compliance](#security--compliance)

---

## Overview

This document provides SYPartners administrators with information about our ChatGPT Slack integration, including how it works, where it's hosted, and how to manage it.

**Quick Facts:**
- **What**: AI-powered Slack bot using OpenAI's ChatGPT
- **Where**: Hosted on Render.com (primary) with EC2 backup
- **Repository**: [github.com/SYPartners/ChatGPT-in-Slack](https://github.com/SYPartners/ChatGPT-in-Slack)
- **Based On**: Open-source project by [@seratch](https://github.com/seratch/ChatGPT-in-Slack)

---

## What is ChatGPT in Slack?

ChatGPT in Slack is an AI assistant that allows our team to interact with OpenAI's ChatGPT models directly within Slack. It provides:

| Capability | Description |
|------------|-------------|
| **AI Conversations** | Natural language interactions with GPT-3.5, GPT-4, and newer models |
| **Context Awareness** | Remembers conversation history within threads |
| **Document Generation** | Creates emails, reports, and other business documents |
| **Image Generation** | Creates images using DALL-E 3 |
| **Language Support** | Automatic translation to user's Slack language |
| **Privacy Controls** | Optional redaction of sensitive information |

---

## How Users Interact with the Bot

Our team members can use ChatGPT in three ways:

### 1. Channel Conversations
- **How**: @mention the bot in any channel
- **Use Case**: Team collaboration, shared problem-solving
- **Privacy**: Visible to all channel members

### 2. Direct Messages
- **How**: Send a DM to the ChatGPT bot
- **Use Case**: Private queries, sensitive topics
- **Privacy**: Completely private

### 3. Home Tab Features
- **How**: Click ChatGPT in Slack sidebar → Home tab
- **Available Actions**:
  - Proofreading text
  - Generating images
  - Creating image variations
  - Free-form prompts
  - Viewing configuration

---

## Our Infrastructure

### Primary: Render.com Deployment

| Component | Details |
|-----------|---------|
| **Platform** | Render.com |
| **Service Name** | `chatgpt-in-slack` |
| **Region** | Virginia, USA |
| **Architecture** | Web service + Redis |
| **Health Check** | `/healthz` endpoint |
| **Auto-Deploy** | Enabled from GitHub main branch |

### How Render Deployment Works:
1. Code changes pushed to GitHub `main` branch
2. Render automatically detects and builds
3. Runs health checks before going live
4. Zero-downtime deployments

### Backup: EC2 Instance

| Component | Details |
|-----------|---------|
| **Instance** | t2.micro |
| **Location** | AWS SYPartners Account |
| **Access** | SSH with `sypartners.pem` |
| **Status** | Backup/fallback option |

**EC2 SSH Access** (if needed):
```bash
ssh -i "sypartners.pem" ubuntu@ec2-54-82-29-43.compute-1.amazonaws.com
```

---

## Admin Access & Management

### Render Dashboard

**Access**: Log into Render.com with admin credentials

**What You Can Do**:
| Task | Location in Render |
|------|-------------------|
| View logs | Services → chatgpt-in-slack → Logs |
| Check metrics | Services → chatgpt-in-slack → Metrics |
| Update env vars | Services → chatgpt-in-slack → Environment |
| Restart service | Services → chatgpt-in-slack → Manual Deploy |
| View deploys | Services → chatgpt-in-slack → Events |

### Slack App Management

**Access**: [api.slack.com/apps](https://api.slack.com/apps) → ChatGPT app

**What You Can Do**:
| Task | Location |
|------|----------|
| View installations | OAuth & Permissions |
| Update permissions | OAuth & Permissions → Scopes |
| Regenerate tokens | Basic Information → App Credentials |
| View usage | App Home → Analytics |

### GitHub Repository

**Access**: [github.com/SYPartners/ChatGPT-in-Slack](https://github.com/SYPartners/ChatGPT-in-Slack)

**What You Can Do**:
- View code and configuration
- Make updates (auto-deploys to Render)
- Review deployment history
- Track issues

---

## Configuration & Environment Variables

### Where Variables Are Stored

All sensitive configuration is stored in **Render Dashboard → Environment tab** (not in code).

### Key Configuration Variables

| Variable | Purpose | Where to Find Value |
|----------|---------|-------------------|
| `SLACK_APP_TOKEN` | Socket Mode connection | Slack App → Basic Information |
| `SLACK_BOT_TOKEN` | Bot authentication | Slack App → OAuth & Permissions |
| `OPENAI_API_KEY` | OpenAI API access | OpenAI Platform → API Keys |
| `REDIS_URL` | Cache connection | Auto-provided by Render |

### Current Model Configuration

| Setting | Current Value | Notes |
|---------|---------------|-------|
| **Chat Model** | `gpt-4o` | Can be changed to `gpt-3.5-turbo` for cost savings |
| **Image Model** | `dall-e-3` | For image generation |
| **Temperature** | `1.0` | Controls creativity (0-2) |
| **Timeout** | `60` seconds | API call timeout |

### Feature Flags

| Feature | Variable | Current Status |
|---------|----------|----------------|
| Language Translation | `USE_SLACK_LANGUAGE` | Enabled |
| Markdown Conversion | `TRANSLATE_MARKDOWN` | Enabled |
| Data Redaction | `REDACTION_ENABLED` | Enabled |
| Image Sharing | `IMAGE_FILE_ACCESS_ENABLED` | Enabled |

---

## Features & Capabilities

### Available Models

Our deployment supports these OpenAI models:

| Model | Use Case | Cost |
|-------|----------|------|
| `gpt-3.5-turbo` | Quick responses, simple tasks | $ |
| `gpt-4` | Complex reasoning | $$$ |
| `gpt-4o` | Optimized GPT-4 (current default) | $$ |
| `gpt-4.1` family | Latest features, large context | $$$ |
| `dall-e-3` | Image generation | $$ |

### Slack Features

Users can access these features:

| Feature | How to Access | Description |
|---------|---------------|-------------|
| **Chat** | @mention or DM | Regular conversation |
| **Summarize Thread** | Right-click message → Apps → Summarize | Get thread summary |
| **Translate Message** | Right-click message → Apps → Translate | Translate to user's language |
| **Proofread** | Home tab button | Grammar and style check |
| **Generate Image** | Home tab button | Create images from text |

---

## Maintenance & Troubleshooting

### Common Issues & Solutions

| Issue | Solution | Where to Check |
|-------|----------|----------------|
| Bot not responding | 1. Check Render status<br>2. Verify env vars<br>3. Check Slack connection | Render logs |
| Slow responses | 1. Check OpenAI status<br>2. Increase timeout<br>3. Switch to faster model | OpenAI status page |
| High costs | 1. Review usage in OpenAI<br>2. Switch to GPT-3.5<br>3. Set usage limits | OpenAI dashboard |
| Auth errors | 1. Verify API keys<br>2. Check token expiration<br>3. Regenerate if needed | Render env vars |

### Monitoring Checklist

**Daily**:
- [ ] Check Render dashboard for errors
- [ ] Monitor OpenAI usage/costs

**Weekly**:
- [ ] Review logs for unusual patterns
- [ ] Check Slack app analytics

**Monthly**:
- [ ] Review and rotate API keys
- [ ] Audit user permissions
- [ ] Update dependencies if needed

### How to Restart the Service

**On Render**:
1. Go to Render Dashboard
2. Navigate to chatgpt-in-slack service
3. Click "Manual Deploy" → "Deploy"

**On EC2 (backup)**:
```bash
# SSH into server
ssh -i "sypartners.pem" ubuntu@ec2-54-82-29-43.compute-1.amazonaws.com

# Find and kill current process
ps -ef | grep 'python.* main.*.py' | grep -v grep | awk '{print $2}' | xargs kill

# Start new instance
cd /path/to/ChatGPT-in-Slack
git pull origin main
source .venv/bin/activate
pip install -r requirements.txt
nohup python main.py &
```

---

## Security & Compliance

### Data Protection

| Measure | Implementation |
|---------|----------------|
| **API Keys** | Stored only in Render, never in code |
| **Redaction** | Enabled for emails, phones, SSNs, credit cards |
| **Access Control** | Limited to authorized Slack workspace |
| **Encryption** | HTTPS for all communications |

### Compliance Considerations

- **Data Residency**: Hosted in US-East (Virginia)
- **OpenAI Usage**: Subject to OpenAI's data usage policies
- **Slack Data**: Governed by Slack's enterprise agreement
- **Logs**: Retained for 7 days on Render

### Security Contacts

| System | Contact |
|--------|---------|
| **Render** | Admin account holder |
| **Slack App** | Workspace admin |
| **OpenAI** | API key owner |
| **GitHub** | Repository admin |

---

## Additional Resources

- **Original Project**: [github.com/seratch/ChatGPT-in-Slack](https://github.com/seratch/ChatGPT-in-Slack)
- **Our Fork**: [github.com/SYPartners/ChatGPT-in-Slack](https://github.com/SYPartners/ChatGPT-in-Slack)
- **Render Status**: [status.render.com](https://status.render.com)
- **OpenAI Status**: [status.openai.com](https://status.openai.com)
- **Slack API Status**: [status.slack.com](https://status.slack.com)

## Credits

This deployment is based on the excellent open-source work by [@seratch](https://github.com/seratch). The original project is MIT licensed. 