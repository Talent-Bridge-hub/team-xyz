# Watch Backend Logs

## View Live Logs

Run this command in a terminal to see backend logs in real-time:

```bash
tail -f /tmp/backend.log
```

## Test the View Report Button

1. **Refresh your browser** (Ctrl+Shift+R)
2. **Open Browser Console** (F12)
3. **Click "View Report"** on session ID 40 (Software Engineer)
4. **Watch both**:
   - Browser console for `[HISTORY]` messages
   - Backend logs in terminal for `[GET_SESSION_DETAILS]` messages

## What You Should See

### In Browser Console:
```
[HISTORY] Loading session details for session 40
[HISTORY] Session details loaded: {...}
[HISTORY] Modal should now be visible
```

### In Backend Logs (`tail -f /tmp/backend.log`):
```
INFO: [GET_SESSION_DETAILS] Fetching session 40 for user X
INFO: [GET_SESSION_DETAILS] Session fetched. Tuple length: 10, Data: (...)
INFO: [GET_SESSION_DETAILS] Fetching Q&A records for session 40
INFO: [GET_SESSION_DETAILS] Fetched 3 Q&A records
INFO: [GET_SESSION_DETAILS] Processing Q&A record 1/3, Record length: 17
INFO: [GET_SESSION_DETAILS] Processing Q&A record 2/3, Record length: 17
INFO: [GET_SESSION_DETAILS] Processing Q&A record 3/3, Record length: 17
```

## If You See Errors

If backend logs show:
```
ERROR: tuple index out of range
```

Look for the log line BEFORE the error:
- If it says "Session fetched. Tuple length: X" → shows session query worked
- If it says "Processing Q&A record X/Y, Record length: Z" → shows which record caused the error

Share the exact log output and I'll fix it! 🔧
