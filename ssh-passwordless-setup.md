# SSH Passwordless Login Setup

## Overview
Guide for setting up passwordless SSH authentication using public key cryptography.

## Prerequisites
- SSH key pair already generated (public and private key)
- Access to the remote server (either via password or another user with elevated privileges)

## Quick Setup Steps

### 1. Verify Local SSH Keys
```bash
ls -la ~/.ssh/*.pub
```

### 2. Configure SSH Config
Edit `~/.ssh/config` to add host configuration:
```
Host <hostname-alias>
    HostName <ip-or-hostname>
    User <username>
    IdentityFile ~/.ssh/<private-key-file>
    IdentitiesOnly yes
```

### 3. Copy Public Key to Remote Server

**Method 1: Using ssh-copy-id (requires password access)**
```bash
ssh-copy-id -i ~/.ssh/<key-name> user@hostname
```

**Method 2: Manual copy via existing access**
```bash
cat ~/.ssh/<key-name>.pub | ssh <existing-access> \
  "mkdir -p /home/<user>/.ssh && \
   cat >> /home/<user>/.ssh/authorized_keys && \
   chmod 700 /home/<user>/.ssh && \
   chmod 600 /home/<user>/.ssh/authorized_keys && \
   chown -R <user>:<user> /home/<user>/.ssh"
```

### 4. Test Connection
```bash
ssh -o BatchMode=yes <hostname-alias> "echo 'Success!'"
```

## Common Issues & Solutions

### Issue: Permission denied (publickey)

**Possible Causes:**
1. **Home directory permissions too permissive**
   - Check: `ls -ld /home/<user>`
   - Fix: `chmod 755 /home/<user>`
   - SSH requires home directory NOT writable by group/others

2. **Wrong home directory ownership**
   - Check: `ls -ld /home/<user>`
   - Fix: `chown <user>:<user> /home/<user>`

3. **SSH directory permissions incorrect**
   - `~/.ssh` should be `700` (drwx------)
   - `~/.ssh/authorized_keys` should be `600` (-rw-------)
   - Fix:
     ```bash
     chmod 700 ~/.ssh
     chmod 600 ~/.ssh/authorized_keys
     ```

4. **Key not in authorized_keys**
   - Verify: `cat ~/.ssh/authorized_keys` on remote server
   - The public key should match local `cat ~/.ssh/<key>.pub`

### Debugging Connection Issues
```bash
# Verbose SSH connection to see what's happening
ssh -vvv <hostname-alias> whoami 2>&1 | grep -E "(Offering|Permission denied)"
```

## Security Best Practices

1. **Private key permissions**: `chmod 600 ~/.ssh/<private-key>`
2. **Never share private keys**: Only `.pub` files should be copied to servers
3. **Use IdentitiesOnly yes**: Prevents trying all keys in ssh-agent
4. **Limit key scope**: Use different keys for different servers/purposes

## Example Real-World Setup

```bash
# Step 1: Configure ~/.ssh/config
Host my-server
    HostName 192.168.1.100
    User myuser
    IdentityFile ~/.ssh/id_rsa_myserver
    IdentitiesOnly yes

# Step 2: Copy key using existing privileged access (e.g., root)
cat ~/.ssh/id_rsa_myserver.pub | ssh root@192.168.1.100 \
  "mkdir -p /home/myuser/.ssh && \
   cat >> /home/myuser/.ssh/authorized_keys && \
   chmod 700 /home/myuser/.ssh && \
   chmod 600 /home/myuser/.ssh/authorized_keys && \
   chown -R myuser:myuser /home/myuser/.ssh && \
   chown myuser:myuser /home/myuser && \
   chmod 755 /home/myuser"

# Step 3: Test passwordless login
ssh my-server whoami
```

## Permission Requirements Summary

| Path | Permissions | Ownership | Why |
|------|-------------|-----------|-----|
| `/home/<user>` | 755 (drwxr-xr-x) | user:user | SSH rejects if writable by others |
| `~/.ssh/` | 700 (drwx------) | user:user | Protects private keys |
| `~/.ssh/authorized_keys` | 600 (-rw-------) | user:user | Prevents unauthorized modifications |
| `~/.ssh/<private-key>` | 600 (-rw-------) | user:user | SSH refuses to use if too permissive |

## Troubleshooting Checklist

- [ ] Public key exists locally
- [ ] Private key has correct permissions (600)
- [ ] SSH config has correct User, HostName, IdentityFile
- [ ] Public key added to remote `~/.ssh/authorized_keys`
- [ ] Remote home directory owned by target user
- [ ] Remote home directory permissions are 755 or more restrictive
- [ ] Remote `~/.ssh` permissions are 700
- [ ] Remote `authorized_keys` permissions are 600
- [ ] Can connect to server via other means (password/other user)

## References
- Created: 2026-01-20
- Based on: SSH passwordless setup best practices
