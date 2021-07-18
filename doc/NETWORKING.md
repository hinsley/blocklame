Each client maintains a list of known node IP addresses from the network.

Nodes are pruned from this list if they are found to "lie;" i.e., provide invalid data.

The only function nodes need to allow requests about is block information.

Querying for blocks should be done individually by index.

Broadcasts: Whenever I find a new block, I broadcast it out to everybody in my known node list. They all check that it's valid, and if it is, they extend their blockchains. If I send out a valid n+2 block and everyone else has only an n block, they all ask me to fill in the gap (n+1) first.

Handling disputes: Any time a client receives a broadcasted block which is newer than the newest block in the local ledger, this broadcasted block goes into a local queue alongside a reference to the broadcaster. The broadcaster is the polled repeatedly for preceding blocks (which are in turn checked for continuity on a case-by-case basis) until the broadcaster contradicts himself, block #0 is provided, or continuity with the local ledger is achieved.

Block broadcasts are triggered by either mining a new block or receiving a new block via unsolicited broadcast.
When receiving a new block from another node, we broadcast it out to everyone else after checking it for validity.

2 REST routes: /query and /issue

E.g.,
`/query?index=n`
`/issue` with POST data (sender endpoint and block data)
