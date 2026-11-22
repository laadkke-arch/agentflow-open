### Proposal Details

Concurrent map writes are a fairly common problem that people run into.  It tends to get into production environments without being detected by testing.  When it occurs it triggers a fatal error, although it doesn't seem to be as severe of a problem to warrant being fatal.  I propose that it be changed to a panic.

```
func mapassign_fast64(t *maptype, h *hmap, key uint64) unsafe.Pointer {
	if h == nil {
		panic(plainError("assignment to entry in nil map"))
	}
	if raceenabled {
		callerpc := getcallerpc()
		racewritepc(unsafe.Pointer(h), callerpc, abi.FuncPCABIInternal(mapassign_fast64))
	}
	if h.flags&hashWriting != 0 {
-		fatal("concurrent map writes")
+		panic(plainError("concurrent map writes"))
	}
```

Obviously the map access should be wrapped in a mutex, but it is an easy mistake to make (especially with large teams).  The call to `fatal` makes the blast radius of the bug rather large for what is likely a recoverable error.   An API request should be able to return a 500 status code rather for this issue.

I understand it could be considered a breaking change, thus you might be wary of such a change.  There's no difference for code that lacks a recover.  Code with a recover will start getting a new kind of panic where the service was previously crashing, that is preferable in 90% of cases.

Is there any reason this was originally set to call `fatal` instead of `panic`?