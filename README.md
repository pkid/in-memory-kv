# in-memory-kv

## branch solution1

- simple in-memory dictionary to store KV pairs
- not working if >= 2 instances, since each pod/container has own dictionary

## branch solution2

- share state using a file
- sync from file to memory
- eventual consistency

